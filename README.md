# VNStock MCP Server

An MCP server exposing tools to access Vietnam stock market data built on top of `vnstock` and `mcp`.

## Installation

### Install from PyPI (Recommended)
```bash
pip install vnstock-mcp-server
```

### Install from source
```bash
git clone https://github.com/maobui/vnstock-mcp-server.git
cd vnstock-mcp-server
uv sync
```

## Prerequisites
- Python 3.10+
- uv (install with `pip install uv` or see `https://docs.astral.sh/uv/`)

## Quick Start

### Run the MCP server
```bash
# If installed from PyPI
vnstock-mcp-server

# If installed from source with uv
uv run python -m vnstock_mcp.server
```

The server uses `FastMCP` and will be ready to accept connections from MCP clients.

## MCP client integration

### Cursor / Cline example
Add a server entry in your MCP configuration:

```json
{
  "mcpServers": {
    "vnstock": {
      "command": "vnstock-mcp-server"
    }
  }
}
```

If installed from source:
```json
{
  "mcpServers": {
    "vnstock": {
      "command": "uv",
      "args": ["run", "python", "-m", "vnstock_mcp.server"],
      "env": {}
    }
  }
}
```

### Claude Desktop example
In MCP server settings:
- Command: `vnstock-mcp-server`
- Args: (leave empty)

## Development

### Install with uv (for development)
```bash
# From the project root
uv sync

# Include dev dependencies (for tests and coverage)
uv sync --group dev
```

### Testing with uv
```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest test/test_company_tools.py

# Run with coverage (HTML)
uv run pytest --cov=src/vnstock_mcp --cov-report=html
# Open report:
#   ./htmlcov/index.html
```

### Building and Publishing

#### Build locally
```bash
# Using the build script
./scripts/build.sh

# Or manually
python -m build
```

#### Create a release
```bash
# Update version in pyproject.toml first, then:
./scripts/release.sh
```

This will:
1. Run tests
2. Create and push a git tag
3. Trigger GitHub Actions to build and publish to PyPI

## Troubleshooting
- Module not found with `uv run`:
  - Ensure `uv sync` completed successfully in the project root.
  - Verify Python version: `python --version` and `uv python list`.
- MCP client cannot connect:
  - Confirm the client configuration matches the installation method
  - Check client logs for detailed errors.
- Command `vnstock-mcp-server` not found:
  - Ensure the package is installed: `pip list | grep vnstock-mcp-server`
  - Try reinstalling: `pip install --upgrade vnstock-mcp-server`

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests: `uv run pytest`
6. Submit a pull request

## Changelog

### v1.0.0
- Initial release
- Full Vietnam stock market data access via MCP
- Support for company data, financial statements, quotes, and more