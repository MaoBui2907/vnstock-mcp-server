#!/bin/bash
# Build script for vnstock-mcp-server

set -e

echo "🔧 Building vnstock-mcp-server..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
uv add --group dev build twine

# Build the package
echo "🏗️  Building package..."
uv run python -m build

# Check the built package
echo "✅ Checking built package..."
uv run twine check dist/*

echo "🎉 Build completed successfully!"
echo "📁 Built files:"
ls -la dist/

echo ""
echo "To test install locally:"
echo "  uv pip install dist/vnstock_mcp_server-*.whl"
echo ""
echo "To upload to TestPyPI:"
echo "  uv run twine upload --repository testpypi dist/*"
echo ""
echo "To upload to PyPI:"
echo "  uv run twine upload dist/*"
