# DIY Helper MCP Servers

Model Context Protocol (MCP) servers for the DIY Helper platform. Provides building code lookups, material specifications, and manufacturer guide access for real-time consultation support.

## Servers

### Building Codes Server
Provides access to residential building codes including:
- NEC (National Electrical Code)
- IRC (International Residential Code)
- IPC (International Plumbing Code)

**Tools:**
- `search_building_codes` - Natural language code search
- `get_code_section` - Retrieve specific code sections
- `check_code_compliance` - Verify scenario compliance
- `list_code_categories` - Browse available codes

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/diy-helper-mcp-servers.git
cd diy-helper-mcp-servers
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Usage

### Running the Building Codes Server
```bash
python src/building_codes_server/server.py
```

### Using with Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "building-codes": {
      "command": "python",
      "args": ["/path/to/diy-helper-mcp-servers/src/building_codes_server/server.py"],
      "env": {
        "CODE_DATABASE_PATH": "/path/to/codes.json"
      }
    }
  }
}
```

### Using Programmatically
```python
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters

# Initialize MCP client
server_params = StdioServerParameters(
    command="python",
    args=["src/building_codes_server/server.py"]
)

async with ClientSession(server_params) as session:
    # Initialize connection
    await session.initialize()
    
    # List available tools
    tools = await session.list_tools()
    
    # Call a tool
    result = await session.call_tool(
        "search_building_codes",
        {"query": "outlet spacing in living room", "jurisdiction": "National"}
    )
    print(result)
```

## Development

### Adding New Codes

Edit `src/building_codes_server/codes.json`:
```json
{
  "id": "unique-id",
  "code_ref": "CODE SECTION",
  "title": "Code Title",
  "category": "electrical|plumbing|structural|mechanical|general",
  "jurisdiction": "National|State|City",
  "summary": "Plain English summary",
  "source": "Official source citation",
  "common_questions": ["question 1", "question 2"],
  "notes": "Additional context",
  "related_codes": ["RELATED-1", "RELATED-2"]
}
```

### Running Tests
```bash
pytest tests/
```

## Roadmap

- [ ] Vector search integration (Pinecone/pgvector)
- [ ] Material specs server
- [ ] Manufacturer guides server
- [ ] Jurisdictional code amendments
- [ ] Image analysis for code compliance
- [ ] Cost estimation tools

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

- Documentation: [docs/setup.md](docs/setup.md)
- Issues: https://github.com/yourusername/diy-helper-mcp-servers/issues
- Email: support@yourplatform.com