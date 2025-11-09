# Quick Start Guide

Get up and running with DIY Helper MCP Servers in 5 minutes.

## Prerequisites

- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/settings/keys))

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/diy-helper-mcp-servers.git
cd diy-helper-mcp-servers
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set your API key**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

## Quick Test

### Option 1: Run Tests
```bash
# Test both MCP servers
./run_all_tests.sh

# Or test individually
python tests/test_building_codes.py
python tests/test_material_server.py
```

### Option 2: Web Interface (Recommended!)
```bash
python test_web_interface.py
```

Then open: http://localhost:5000

Try asking:
- "What are kitchen outlet requirements?"
- "Search for 12 gauge wire"
- "Calculate wire needed for 50 foot run"

### Option 3: Claude Desktop (Mac/Windows only)

1. Find your config file:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add your servers:
```json
{
  "mcpServers": {
    "building-codes": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["/full/path/to/src/building_codes_server/server.py"]
    },
    "material-specs": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["/full/path/to/src/material_specs_server/server.py"]
    }
  }
}
```

3. Restart Claude Desktop

4. Ask: "What tools do you have access to?"

## What's Included

### Building Codes Server
- 6 sample codes (electrical, plumbing, structural)
- NEC, IRC, IPC code sections
- Code search and lookup
- Compliance checking

### Material Specs Server
- 12+ mock products from Home Depot
- Product search with pricing
- 7 material calculators:
  - Wire quantity
  - Outlet requirements
  - Tile needs
  - Paint calculation
  - Deck lumber
  - PEX piping
  - And more!
- Shopping list generator
- Alternative product finder

## Next Steps

1. **Expand the code database**: Add more codes to `src/building_codes_server/codes.json`
2. **Add more products**: Expand `src/material_specs_server/suppliers/home_depot.py`
3. **Integrate real APIs**: Replace mock data with Home Depot/UpCodes APIs
4. **Build the web app**: Use `test_web_interface.py` as a starting point

## Troubleshooting

**"ModuleNotFoundError: No module named 'src'"**
- Make sure you're running from the project root
- Check that `__init__.py` files exist in all directories

**"ANTHROPIC_API_KEY not set"**
- Run: `export ANTHROPIC_API_KEY='your-key'`
- Or add to `.env` file

**"No module named 'mcp'"**
- Run: `pip install mcp`

**Port 5000 already in use**
- Change port in `test_web_interface.py`: `app.run(debug=True, port=5001)`

## Support

- Documentation: See [README.md](README.md)
- Issues: https://github.com/YOUR_USERNAME/diy-helper-mcp-servers/issues
- Demo queries: See [demo_queries.md](demo_queries.md)