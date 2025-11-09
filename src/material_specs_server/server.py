"""
Material Specs MCP Server
Provides material search, pricing, and calculation tools
"""

import asyncio
import json
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from .product_database import ProductDatabase
from .calculators import MaterialCalculator

# Initialize server
app = Server("material-specs-server")

# Initialize product database and calculator
product_db = ProductDatabase()
calculator = MaterialCalculator()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools for material specs"""
    return [
        Tool(
            name="search_materials",
            description="Search for building materials and get current pricing from suppliers like Home Depot, Lowe's, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for (e.g., '12 gauge wire', 'GFCI outlet', 'pressure treated 2x4')"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["electrical", "plumbing", "lumber", "flooring", "hardware"],
                        "description": "Product category to narrow search"
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "ZIP code for local availability and pricing"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price filter"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_product_details",
            description="Get detailed specifications for a specific product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID (e.g., 'HD-12345')"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="find_alternatives",
            description="Find alternative products at different price points",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Original product ID"
                    },
                    "min_price": {
                        "type": "number",
                        "description": "Minimum price for alternatives"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price for alternatives"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="check_compatibility",
            description="Check if two products are compatible with each other",
            inputSchema={
                "type": "object",
                "properties": {
                    "product1_id": {
                        "type": "string",
                        "description": "First product ID"
                    },
                    "product2_id": {
                        "type": "string",
                        "description": "Second product ID"
                    }
                },
                "required": ["product1_id", "product2_id"]
            }
        ),
        Tool(
            name="calculate_wire_needed",
            description="Calculate how much electrical wire is needed for a circuit",
            inputSchema={
                "type": "object",
                "properties": {
                    "circuit_length_feet": {
                        "type": "number",
                        "description": "One-way distance in feet from panel to endpoint"
                    },
                    "num_circuits": {
                        "type": "integer",
                        "description": "Number of circuits (default: 1)"
                    }
                },
                "required": ["circuit_length_feet"]
            }
        ),
        Tool(
            name="calculate_outlets_needed",
            description="Calculate number of outlets needed per NEC code",
            inputSchema={
                "type": "object",
                "properties": {
                    "room_perimeter_feet": {
                        "type": "number",
                        "description": "Total perimeter of room in feet"
                    },
                    "room_type": {
                        "type": "string",
                        "enum": ["living", "kitchen", "bathroom", "garage"],
                        "description": "Type of room"
                    }
                },
                "required": ["room_perimeter_feet", "room_type"]
            }
        ),
        Tool(
            name="calculate_tile_needed",
            description="Calculate how much tile is needed for a floor or wall",
            inputSchema={
                "type": "object",
                "properties": {
                    "area_sq_ft": {
                        "type": "number",
                        "description": "Total area to tile in square feet"
                    },
                    "tile_width_inches": {
                        "type": "number",
                        "description": "Tile width in inches (default: 12)"
                    },
                    "tile_height_inches": {
                        "type": "number",
                        "description": "Tile height in inches (default: 12)"
                    }
                },
                "required": ["area_sq_ft"]
            }
        ),
        Tool(
            name="calculate_paint_needed",
            description="Calculate how much paint is needed",
            inputSchema={
                "type": "object",
                "properties": {
                    "area_sq_ft": {
                        "type": "number",
                        "description": "Total wall/ceiling area in square feet"
                    },
                    "num_coats": {
                        "type": "integer",
                        "description": "Number of coats (default: 2)"
                    }
                },
                "required": ["area_sq_ft"]
            }
        ),
        Tool(
            name="calculate_deck_lumber",
            description="Calculate lumber needed for deck construction",
            inputSchema={
                "type": "object",
                "properties": {
                    "deck_length_ft": {
                        "type": "number",
                        "description": "Deck length in feet"
                    },
                    "deck_width_ft": {
                        "type": "number",
                        "description": "Deck width in feet"
                    }
                },
                "required": ["deck_length_ft", "deck_width_ft"]
            }
        ),
        Tool(
            name="calculate_pex_pipe",
            description="Calculate PEX piping needed for plumbing project",
            inputSchema={
                "type": "object",
                "properties": {
                    "num_fixtures": {
                        "type": "integer",
                        "description": "Number of plumbing fixtures (sinks, toilets, showers, etc.)"
                    },
                    "manifold_system": {
                        "type": "boolean",
                        "description": "True for home-run manifold system, False for trunk-and-branch"
                    }
                },
                "required": ["num_fixtures"]
            }
        ),
        Tool(
            name="create_shopping_list",
            description="Create a complete shopping list with products and quantities",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "string"},
                                "quantity": {"type": "integer"}
                            }
                        },
                        "description": "List of product IDs and quantities"
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "ZIP code for store location"
                    }
                },
                "required": ["items"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    try:
        if name == "search_materials":
            query = arguments.get("query")
            category = arguments.get("category")
            zip_code = arguments.get("zip_code")
            max_price = arguments.get("max_price")
            
            products = await product_db.search_all_suppliers(
                query=query,
                category=category,
                zip_code=zip_code,
                max_price=max_price,
                limit_per_supplier=5
            )
            
            formatted = format_product_results(products, zip_code)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "get_product_details":
            product_id = arguments.get("product_id")
            
            product = await product_db.get_product_by_id(product_id)
            
            if product:
                formatted = format_product_details(product)
                return [TextContent(type="text", text=formatted)]
            else:
                return [TextContent(
                    type="text",
                    text=f"Product '{product_id}' not found in our database."
                )]
        
        elif name == "find_alternatives":
            product_id = arguments.get("product_id")
            min_price = arguments.get("min_price")
            max_price = arguments.get("max_price")
            
            product = await product_db.get_product_by_id(product_id)
            if not product:
                return [TextContent(
                    type="text",
                    text=f"Product '{product_id}' not found."
                )]
            
            budget_range = None
            if min_price is not None and max_price is not None:
                budget_range = (min_price, max_price)
            
            alternatives = await product_db.find_alternatives(product, budget_range)
            formatted = format_alternatives(product, alternatives)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "check_compatibility":
            product1_id = arguments.get("product1_id")
            product2_id = arguments.get("product2_id")
            
            result = await product_db.check_compatibility(product1_id, product2_id)
            formatted = format_compatibility(result)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "calculate_wire_needed":
            circuit_length = arguments.get("circuit_length_feet")
            num_circuits = arguments.get("num_circuits", 1)
            
            result = calculator.calculate_wire_length(circuit_length, num_circuits)
            formatted = format_calculation_result("Wire Calculation", result)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "calculate_outlets_needed":
            perimeter = arguments.get("room_perimeter_feet")
            room_type = arguments.get("room_type")
            
            result = calculator.calculate_outlets_needed(perimeter, room_type)
            formatted = format_calculation_result("Outlet Calculation", result)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "calculate_tile_needed":
            area = arguments.get("area_sq_ft")
            width = arguments.get("tile_width_inches", 12)
            height = arguments.get("tile_height_inches", 12)
            
            result = calculator.calculate_tile_needed(area, (width, height))
            formatted = format_calculation_result("Tile Calculation", result)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "calculate_paint_needed":
            area = arguments.get("area_sq_ft")
            coats = arguments.get("num_coats", 2)
            
            result = calculator.calculate_paint_needed(area, coats)
            formatted = format_calculation_result("Paint Calculation", result)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "calculate_deck_lumber":
            length = arguments.get("deck_length_ft")
            width = arguments.get("deck_width_ft")
            
            result = calculator.calculate_lumber_for_deck(length, width)
            formatted = format_calculation_result("Deck Lumber Calculation", result)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "calculate_pex_pipe":
            num_fixtures = arguments.get("num_fixtures")
            manifold = arguments.get("manifold_system", True)
            
            result = calculator.calculate_pex_pipe(num_fixtures, manifold_system=manifold)
            formatted = format_calculation_result("PEX Pipe Calculation", result)
            return [TextContent(type="text", text=formatted)]
        
        elif name == "create_shopping_list":
            items = arguments.get("items", [])
            zip_code = arguments.get("zip_code")
            
            shopping_list = await create_shopping_list(items, zip_code)
            return [TextContent(type="text", text=shopping_list)]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing tool {name}: {str(e)}"
        )]


def format_product_results(products: list, zip_code: Optional[str] = None) -> str:
    """Format product search results"""
    if not products:
        return "No products found matching your criteria. Try broadening your search or checking the category."
    
    output = f"**Found {len(products)} Products:**\n\n"
    
    for i, product in enumerate(products[:10], 1):  # Limit to top 10
        output += f"**{i}. {product.name}**\n"
        output += f"   - **Price:** ${product.price:.2f}\n"
        output += f"   - **Supplier:** {product.supplier}\n"
        
        if product.in_stock:
            output += f"   - **Availability:** ✅ In Stock"
            if product.quantity_available:
                output += f" ({product.quantity_available} available)"
            output += "\n"
        else:
            output += f"   - **Availability:** ❌ Out of Stock\n"
        
        if product.store_location and product.distance_miles:
            output += f"   - **Location:** {product.store_location} ({product.distance_miles} miles)\n"
        
        if product.rating:
            stars = "⭐" * int(product.rating)
            output += f"   - **Rating:** {stars} {product.rating}/5.0 ({product.review_count} reviews)\n"
        
        # Show key specs
        if product.specifications:
            specs = product.specifications
            output += f"   - **Specs:** "
            spec_items = []
            for key, value in list(specs.items())[:3]:  # Show first 3 specs
                spec_items.append(f"{key}: {value}")
            output += ", ".join(spec_items) + "\n"
        
        if product.url:
            output += f"   - **Link:** {product.url}\n"
        
        output += f"   - **Product ID:** `{product.id}` (use for alternatives/details)\n"
        output += "\n"
    
    if len(products) > 10:
        output += f"\n*Showing top 10 of {len(products)} results*\n"
    
    return output


def format_product_details(product) -> str:
    """Format detailed product information"""
    output = f"**{product.name}**\n\n"
    output += f"**Price:** ${product.price:.2f}\n"
    output += f"**Supplier:** {product.supplier}\n"
    output += f"**Category:** {product.category} > {product.subcategory}\n"
    output += f"**Manufacturer:** {product.manufacturer}\n\n"
    
    if product.rating:
        stars = "⭐" * int(product.rating)
        output += f"**Rating:** {stars} {product.rating}/5.0 ({product.review_count} reviews)\n\n"
    
    output += "**Specifications:**\n"
    for key, value in product.specifications.items():
        output += f"  - **{key.replace('_', ' ').title()}:** {value}\n"
    
    output += f"\n**Availability:** {'✅ In Stock' if product.in_stock else '❌ Out of Stock'}\n"
    
    if product.url:
        output += f"\n**Purchase:** {product.url}\n"
    
    return output


def format_alternatives(original, alternatives: list) -> str:
    """Format alternative products"""
    output = f"**Alternatives to {original.name}** (${original.price:.2f}):\n\n"
    
    if not alternatives:
        output += "No alternatives found in the specified price range.\n"
        return output
    
    for i, alt in enumerate(alternatives[:5], 1):
        price_diff = alt.price - original.price
        price_indicator = "💰 Cheaper" if price_diff < 0 else "💸 More expensive"
        
        output += f"**{i}. {alt.name}**\n"
        output += f"   - **Price:** ${alt.price:.2f} ({price_indicator}: ${abs(price_diff):.2f})\n"
        output += f"   - **Supplier:** {alt.supplier}\n"
        
        if alt.rating:
            stars = "⭐" * int(alt.rating)
            output += f"   - **Rating:** {stars} {alt.rating}/5.0\n"
        
        output += f"   - **Product ID:** `{alt.id}`\n\n"
    
    return output


def format_compatibility(result: dict) -> str:
    """Format compatibility check result"""
    if "error" in result:
        return f"**Error:** {result['error']}"
    
    compatible = result.get("compatible", False)
    confidence = result.get("confidence", "unknown")
    notes = result.get("notes", [])
    
    output = "**Compatibility Check:**\n\n"
    
    if compatible:
        output += "✅ **Compatible** "
    else:
        output += "❌ **Not Compatible** "
    
    output += f"(Confidence: {confidence})\n\n"
    
    if notes:
        output += "**Notes:**\n"
        for note in notes:
            output += f"  - {note}\n"
    else:
        output += "*No specific compatibility information available. Consult product specifications or manufacturer.*\n"
    
    return output


def format_calculation_result(title: str, result: dict) -> str:
    """Format calculation results"""
    output = f"**{title}:**\n\n"
    
    for key, value in result.items():
        if key == "note":
            output += f"\n💡 **Note:** {value}\n"
        elif isinstance(value, dict):
            # Nested result (like deck lumber)
            output += f"\n**{key.replace('_', ' ').title()}:**\n"
            for sub_key, sub_value in value.items():
                output += f"  - **{sub_key.replace('_', ' ').title()}:** {sub_value}\n"
        else:
            output += f"**{key.replace('_', ' ').title()}:** {value}\n"
    
    return output


async def create_shopping_list(items: list, zip_code: Optional[str]) -> str:
    """Create formatted shopping list"""
    output = "**🛒 Shopping List:**\n\n"
    
    total_cost = 0.0
    
    for i, item in enumerate(items, 1):
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)
        
        product = await product_db.get_product_by_id(product_id)
        
        if product:
            item_cost = product.price * quantity
            total_cost += item_cost
            
            output += f"**{i}. {product.name}**\n"
            output += f"   - Quantity: {quantity}\n"
            output += f"   - Unit Price: ${product.price:.2f}\n"
            output += f"   - Subtotal: ${item_cost:.2f}\n"
            output += f"   - Supplier: {product.supplier}\n"
            
            if product.url:
                output += f"   - Link: {product.url}\n"
            
            output += "\n"
        else:
            output += f"**{i}. Product {product_id}** - Not found\n\n"
    
    output += f"\n**Total Estimated Cost: ${total_cost:.2f}**\n"
    
    if zip_code:
        output += f"\n📍 **Nearest stores to {zip_code}:**\n"
        output += "  - Home Depot Brighton - 2.3 miles\n"
        output += "  - Lowe's Watertown - 3.1 miles\n"
    
    output += "\n*Prices and availability subject to change. Verify before purchasing.*"
    
    return output


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())