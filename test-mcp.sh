#!/bin/bash
# Test MCP Server with Inspector

echo "Starting MCP Inspector..."
echo "This will open a web interface at http://localhost:5173"
echo ""
echo "You can test all tools and resources there!"

npx @modelcontextprotocol/inspector uv --directory /Users/michaelkrech/_work/anki-tutor run anki-mcp-server
