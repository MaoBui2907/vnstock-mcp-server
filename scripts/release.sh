#!/bin/bash
# Release script for vnstock-mcp-server

set -e

# Get version from pyproject.toml
VERSION=$(grep -E '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

if [ -z "$VERSION" ]; then
    echo "❌ Could not extract version from pyproject.toml"
    exit 1
fi

echo "🚀 Preparing release for vnstock-mcp-server v$VERSION"

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "⚠️  Warning: You're not on the main branch (current: $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Release cancelled"
        exit 1
    fi
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Working directory is not clean. Please commit or stash changes first."
    git status --short
    exit 1
fi

# Check if tag already exists
if git tag -l | grep -q "^v$VERSION$"; then
    echo "❌ Tag v$VERSION already exists"
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
if command -v uv &> /dev/null; then
    uv run pytest
else
    python -m pytest
fi

# Create and push tag
echo "🏷️  Creating and pushing tag v$VERSION..."
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

echo "✅ Tag v$VERSION created and pushed!"
echo "🎉 GitHub Actions will now build and publish the package to PyPI"
echo "📖 Check the release at: https://github.com/maobui/vnstock-mcp-server/releases"
