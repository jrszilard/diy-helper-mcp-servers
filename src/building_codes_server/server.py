"""
Building Codes MCP Server
Provides building code lookup and search functionality for DIY consultations
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio
from .code_database import CodeDatabase
from .vector_search import search_codes

# Initialize server
app = Server("building-codes-server")

# Initialize code database
code_db = CodeDatabase()

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools for building code lookup
    """
    return [
        Tool(
            name="search_building_codes",
            description="Search building codes by natural language query. Returns relevant code sections with citations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language question about building codes (e.g., 'outlet spacing in kitchen')"
                    },
                    "jurisdiction": {
                        "type": "string",
                        "description": "State or city (e.g., 'California', 'New York City', 'National')",
                        "default": "National"
                    },
                    "code_type": {
                        "type": "string",
                        "enum": ["electrical", "plumbing", "structural", "mechanical", "general"],
                        "description": "Type of code to search",
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_code_section",
            description="Retrieve specific code section by exact reference (e.g., 'NEC 210.52', 'IRC R311.7')",
            inputSchema={
                "type": "object",
                "properties": {
                    "section_reference": {
                        "type": "string",
                        "description": "Exact code section reference (e.g., 'NEC 210.52(A)(1)', 'IRC R502.3.1')"
                    },
                    "jurisdiction": {
                        "type": "string",
                        "description": "Jurisdiction for code (default: National)",
                        "default": "National"
                    }
                },
                "required": ["section_reference"]
            }
        ),
        Tool(
            name="check_code_compliance",
            description="Check if a described scenario complies with building codes",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario": {
                        "type": "string",
                        "description": "Description of the building scenario to check (e.g., 'outlets 18 inches apart in living room')"
                    },
                    "jurisdiction": {
                        "type": "string",
                        "description": "Jurisdiction to check against",
                        "default": "National"
                    }
                },
                "required": ["scenario"]
            }
        ),
        Tool(
            name="list_code_categories",
            description="List all available code categories and common questions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls from Claude
    """
    
    if name == "search_building_codes":
        query = arguments.get("query")
        jurisdiction = arguments.get("jurisdiction", "National")
        code_type = arguments.get("code_type")
        
        # Search the code database
        results = await code_db.search(
            query=query,
            jurisdiction=jurisdiction,
            code_type=code_type,
            top_k=3
        )
        
        # Format results
        formatted_results = format_code_results(results)
        
        return [TextContent(
            type="text",
            text=formatted_results
        )]
    
    elif name == "get_code_section":
        section_ref = arguments.get("section_reference")
        jurisdiction = arguments.get("jurisdiction", "National")
        
        # Get specific section
        section = await code_db.get_section(section_ref, jurisdiction)
        
        if section:
            formatted = format_code_section(section)
            return [TextContent(type="text", text=formatted)]
        else:
            return [TextContent(
                type="text",
                text=f"Code section '{section_ref}' not found in database for {jurisdiction}. This may be a valid code section that we haven't indexed yet. Recommend consulting local building department or current code book."
            )]
    
    elif name == "check_code_compliance":
        scenario = arguments.get("scenario")
        jurisdiction = arguments.get("jurisdiction", "National")
        
        # Search for relevant codes
        relevant_codes = await code_db.search(
            query=scenario,
            jurisdiction=jurisdiction,
            top_k=3
        )
        
        # Analyze compliance
        compliance_check = analyze_compliance(scenario, relevant_codes)
        
        return [TextContent(type="text", text=compliance_check)]
    
    elif name == "list_code_categories":
        categories = code_db.get_categories()
        return [TextContent(
            type="text",
            text=json.dumps(categories, indent=2)
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


def format_code_results(results: list) -> str:
    """Format search results into readable text"""
    if not results:
        return "No relevant code sections found. This may be an uncommon scenario or outside typical residential codes. Recommend consulting with a licensed professional."
    
    output = "**Relevant Building Codes:**\n\n"
    
    for i, result in enumerate(results, 1):
        output += f"**{i}. {result['title']}** ({result['code_ref']})\n"
        output += f"   - **Summary:** {result['summary']}\n"
        output += f"   - **Jurisdiction:** {result['jurisdiction']}\n"
        output += f"   - **Source:** {result['source']}\n"
        
        if result.get('notes'):
            output += f"   - **Notes:** {result['notes']}\n"
        
        output += "\n"
    
    output += "\n*Note: Always verify with local building department as jurisdictions may have amendments.*"
    
    return output


def format_code_section(section: dict) -> str:
    """Format a specific code section"""
    output = f"**{section['title']}**\n\n"
    output += f"**Reference:** {section['code_ref']}\n"
    output += f"**Summary:** {section['summary']}\n"
    
    if section.get('full_text'):
        output += f"\n**Code Text:**\n{section['full_text']}\n"
    
    if section.get('related_codes'):
        output += f"\n**Related Codes:** {', '.join(section['related_codes'])}\n"
    
    output += f"\n**Source:** {section['source']}"
    
    return output


def analyze_compliance(scenario: str, relevant_codes: list) -> str:
    """Analyze if scenario complies with codes"""
    output = f"**Compliance Check for:** {scenario}\n\n"
    
    if not relevant_codes:
        output += "⚠️ **Unable to determine compliance** - no relevant codes found in database.\n"
        output += "Recommend consulting a licensed professional for this scenario."
        return output
    
    output += "**Applicable Codes:**\n\n"
    
    for code in relevant_codes:
        output += f"- {code['title']} ({code['code_ref']})\n"
        output += f"  Requirement: {code['summary']}\n\n"
    
    output += "\n**Assessment:**\n"
    output += "Based on the codes above, verify that your scenario meets these requirements. "
    output += "If uncertain, consult with a licensed professional before proceeding.\n\n"
    output += "*This is guidance only and not a substitute for professional inspection or approval.*"
    
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