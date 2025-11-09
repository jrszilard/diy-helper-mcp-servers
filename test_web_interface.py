"""
Web-based testing interface for MCP servers
Run this and open in your browser to test Claude + MCP integration
"""

from flask import Flask, render_template, request, jsonify
import asyncio
import os
from anthropic import Anthropic
from pathlib import Path
import sys

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.building_codes_server.code_database import CodeDatabase
from src.material_specs_server.product_database import ProductDatabase
from src.material_specs_server.calculators import MaterialCalculator

app = Flask(__name__)

# Initialize MCP server databases
code_db = CodeDatabase()
product_db = ProductDatabase()
calc = MaterialCalculator()

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_available_tools():
    """Define all MCP tools for Claude"""
    return [
        {
            "name": "search_building_codes",
            "description": "Search building codes by query and jurisdiction. Returns relevant code sections with citations.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'kitchen outlet spacing')"
                    },
                    "jurisdiction": {
                        "type": "string",
                        "description": "Jurisdiction (default: National)",
                        "default": "National"
                    },
                    "code_type": {
                        "type": "string",
                        "enum": ["electrical", "plumbing", "structural", "mechanical", "general"],
                        "description": "Type of code"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_code_section",
            "description": "Get specific code section by reference (e.g., 'NEC 210.52(A)(1)')",
            "input_schema": {
                "type": "object",
                "properties": {
                    "section_reference": {
                        "type": "string",
                        "description": "Code section reference"
                    },
                    "jurisdiction": {
                        "type": "string",
                        "default": "National"
                    }
                },
                "required": ["section_reference"]
            }
        },
        {
            "name": "search_materials",
            "description": "Search for building materials and get current pricing",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product search query"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["electrical", "plumbing", "lumber", "flooring", "hardware"]
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "ZIP code for local availability"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price filter"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "calculate_wire_needed",
            "description": "Calculate electrical wire quantity needed",
            "input_schema": {
                "type": "object",
                "properties": {
                    "circuit_length_feet": {
                        "type": "number",
                        "description": "Circuit length in feet"
                    },
                    "num_circuits": {
                        "type": "integer",
                        "default": 1
                    }
                },
                "required": ["circuit_length_feet"]
            }
        },
        {
            "name": "calculate_outlets_needed",
            "description": "Calculate number of outlets needed per NEC code",
            "input_schema": {
                "type": "object",
                "properties": {
                    "room_perimeter_feet": {
                        "type": "number",
                        "description": "Room perimeter in feet"
                    },
                    "room_type": {
                        "type": "string",
                        "enum": ["living", "kitchen", "bathroom", "garage"]
                    }
                },
                "required": ["room_perimeter_feet", "room_type"]
            }
        },
        {
            "name": "calculate_tile_needed",
            "description": "Calculate tile quantity needed",
            "input_schema": {
                "type": "object",
                "properties": {
                    "area_sq_ft": {
                        "type": "number",
                        "description": "Area in square feet"
                    },
                    "tile_width_inches": {
                        "type": "number",
                        "default": 12
                    },
                    "tile_height_inches": {
                        "type": "number",
                        "default": 12
                    }
                },
                "required": ["area_sq_ft"]
            }
        }
    ]


async def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute MCP tool and return result"""
    
    try:
        if tool_name == "search_building_codes":
            results = await code_db.search(
                query=tool_input.get("query"),
                jurisdiction=tool_input.get("jurisdiction", "National"),
                code_type=tool_input.get("code_type"),
                top_k=3
            )
            
            if not results:
                return "No relevant codes found."
            
            output = "**Building Codes Found:**\n\n"
            for i, result in enumerate(results, 1):
                output += f"{i}. **{result['title']}** ({result['code_ref']})\n"
                output += f"   - {result['summary']}\n"
                output += f"   - Source: {result['source']}\n\n"
            
            return output
        
        elif tool_name == "get_code_section":
            section = await code_db.get_section(
                tool_input.get("section_reference"),
                tool_input.get("jurisdiction", "National")
            )
            
            if not section:
                return f"Code section {tool_input.get('section_reference')} not found."
            
            output = f"**{section['title']}**\n\n"
            output += f"**Reference:** {section['code_ref']}\n"
            output += f"**Summary:** {section['summary']}\n"
            output += f"**Source:** {section['source']}\n"
            
            return output
        
        elif tool_name == "search_materials":
            products = await product_db.search_all_suppliers(
                query=tool_input.get("query"),
                category=tool_input.get("category"),
                zip_code=tool_input.get("zip_code"),
                max_price=tool_input.get("max_price"),
                limit_per_supplier=5
            )
            
            if not products:
                return "No products found."
            
            output = f"**Found {len(products)} Products:**\n\n"
            for i, product in enumerate(products[:5], 1):
                output += f"{i}. **{product.name}**\n"
                output += f"   - Price: ${product.price:.2f}\n"
                output += f"   - Supplier: {product.supplier}\n"
                output += f"   - In Stock: {'Yes' if product.in_stock else 'No'}\n"
                if product.rating:
                    output += f"   - Rating: {product.rating}/5.0\n"
                output += "\n"
            
            return output
        
        elif tool_name == "calculate_wire_needed":
            result = calc.calculate_wire_length(
                tool_input.get("circuit_length_feet"),
                tool_input.get("num_circuits", 1)
            )
            
            output = "**Wire Calculation:**\n\n"
            output += f"- Base feet needed: {result['base_feet']} ft\n"
            output += f"- With 15% waste: {result['with_waste']:.1f} ft\n"
            output += f"- Recommended to buy: {result['recommended_feet']} ft\n"
            output += f"\n💡 {result['note']}\n"
            
            return output
        
        elif tool_name == "calculate_outlets_needed":
            result = calc.calculate_outlets_needed(
                tool_input.get("room_perimeter_feet"),
                tool_input.get("room_type")
            )
            
            output = "**Outlet Calculation:**\n\n"
            output += f"- Outlets needed: {result['outlets_needed']}\n"
            output += f"- Room type: {result['room_type']}\n"
            output += f"- Code reference: {result['code_reference']}\n"
            output += f"\n💡 {result['note']}\n"
            
            return output
        
        elif tool_name == "calculate_tile_needed":
            result = calc.calculate_tile_needed(
                tool_input.get("area_sq_ft"),
                (tool_input.get("tile_width_inches", 12), tool_input.get("tile_height_inches", 12))
            )
            
            output = "**Tile Calculation:**\n\n"
            output += f"- Area to cover: {result['area_sq_ft']} sq ft\n"
            output += f"- Tile size: {result['tile_size']}\n"
            output += f"- Tiles needed: {result['tiles_needed']}\n"
            output += f"- Cases to buy: {result['cases_needed']}\n"
            output += f"- Total coverage: {result['total_coverage_sq_ft']} sq ft\n"
            output += f"\n💡 {result['note']}\n"
            
            return output
        
        else:
            return f"Unknown tool: {tool_name}"
    
    except Exception as e:
        return f"Error executing tool: {str(e)}"


async def chat_with_claude(user_message: str, conversation_history: list):
    """Send message to Claude with MCP tools available"""
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Call Claude with tools
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        tools=get_available_tools(),
        messages=conversation_history
    )
    
    # Process tool calls if any
    while response.stop_reason == "tool_use":
        # Extract tool calls
        tool_results = []
        assistant_content = []
        
        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_name = content_block.name
                tool_input = content_block.input
                
                print(f"🔧 Claude is calling tool: {tool_name}")
                print(f"   Input: {tool_input}")
                
                # Execute the tool
                tool_result = await execute_tool(tool_name, tool_input)
                
                # Store tool use block as dict (JSON serializable)
                assistant_content.append({
                    "type": "tool_use",
                    "id": content_block.id,
                    "name": tool_name,
                    "input": tool_input
                })
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": tool_result
                })
            elif content_block.type == "text":
                # Store text block as dict (JSON serializable)
                assistant_content.append({
                    "type": "text",
                    "text": content_block.text
                })
        
        # Add assistant's response with tool use to history (as serializable dicts)
        conversation_history.append({
            "role": "assistant",
            "content": assistant_content
        })
        
        # Add tool results to history
        conversation_history.append({
            "role": "user",
            "content": tool_results
        })
        
        # Continue conversation with tool results
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            tools=get_available_tools(),
            messages=conversation_history
        )
    
    # Extract final text response
    final_response = ""
    assistant_content = []
    
    for content_block in response.content:
        if hasattr(content_block, 'text'):
            final_response += content_block.text
            assistant_content.append({
                "type": "text",
                "text": content_block.text
            })
        elif content_block.type == "text":
            final_response += content_block.text
            assistant_content.append({
                "type": "text",
                "text": content_block.text
            })
    
    # Add final response to history (as serializable dict)
    conversation_history.append({
        "role": "assistant",
        "content": assistant_content if assistant_content else final_response
    })
    
    return final_response, conversation_history


@app.route('/')
def index():
    """Render chat interface"""
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '')
    conversation_history = data.get('history', [])
    
    # Run async chat function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        response, updated_history = loop.run_until_complete(
            chat_with_claude(user_message, conversation_history)
        )
        
        return jsonify({
            'response': response,
            'history': updated_history
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full error to console
        return jsonify({
            'error': str(e)
        }), 500
    
    finally:
        loop.close()


if __name__ == '__main__':
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ERROR: ANTHROPIC_API_KEY not set!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("Get your key at: https://console.anthropic.com/settings/keys\n")
    else:
        print("\n✅ Starting MCP Test Web Interface...")
        print("Open your browser to: http://localhost:5000")
        print("Press Ctrl+C to stop\n")
        app.run(debug=True, port=5000)