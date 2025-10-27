"""Anki MCP Server implementation."""

import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from anki_mcp_server.client import AnkiClient, AnkiConnectError
from anki_mcp_server.resources import ResourceHandler
from anki_mcp_server.tools import ToolHandler

logger = logging.getLogger(__name__)


class AnkiMcpServer:
    """MCP server for Anki integration.

    Provides tools and resources for interacting with Anki via AnkiConnect.

    Args:
        port: AnkiConnect port (default: 8765)
    """

    def __init__(self, port: int = 8765):
        self.port = port
        self.client = AnkiClient(url=f"http://localhost:{port}")
        self.tool_handler = ToolHandler(self.client)
        self.resource_handler = ResourceHandler(self.client)
        self.server = Server("anki-mcp-server")
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP request handlers."""

        @self.server.list_tools()
        async def list_tools():
            """List available tools."""
            await self._check_connection()
            return self.tool_handler.get_tool_list()

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            """Execute a tool."""
            await self._check_connection()
            try:
                return await self.tool_handler.execute_tool(name, arguments)
            except ValueError as e:
                return [TextContent(type="text", text=f"Error: {e}")]
            except AnkiConnectError as e:
                return [TextContent(type="text", text=f"Anki Error: {e}")]

        @self.server.list_resources()
        async def list_resources():
            """List available resources."""
            await self._check_connection()
            return self.resource_handler.get_resource_list()

        @self.server.list_resource_templates()
        async def list_resource_templates():
            """List available resource templates."""
            await self._check_connection()
            return self.resource_handler.get_resource_templates()

        @self.server.read_resource()
        async def read_resource(uri: str):
            """Read a resource."""
            await self._check_connection()
            try:
                content = await self.resource_handler.read_resource(uri)
                return TextContent(type="text", text=content)
            except ValueError as e:
                return TextContent(type="text", text=f"Error: {e}")
            except AnkiConnectError as e:
                return TextContent(type="text", text=f"Anki Error: {e}")

    async def _check_connection(self) -> None:
        """Verify Anki is running."""
        try:
            await self.client.check_connection()
        except AnkiConnectError:
            raise RuntimeError(
                "Failed to connect to Anki. Please ensure:\n"
                "1. Anki is running\n"
                "2. AnkiConnect add-on is installed\n"
                f"3. AnkiConnect is listening on port {self.port}"
            )

    async def run(self) -> None:
        """Run the MCP server with stdio transport."""
        logger.info("Starting Anki MCP server on stdio")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )

    async def cleanup(self) -> None:
        """Clean up resources."""
        await self.client.close()
