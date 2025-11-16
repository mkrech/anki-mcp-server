"""Anki MCP Server - MCP server for Anki flashcard integration."""

__version__ = "0.1.0"

from anki_mcp_server.client import AnkiClient

__all__ = ["AnkiClient", "__version__"]
