"""Basic smoke tests for anki-mcp-server."""

import pytest

from anki_mcp_server import __version__
from anki_mcp_server.client import AnkiClient
from anki_mcp_server.resources import ResourceHandler
from anki_mcp_server.server import AnkiMcpServer
from anki_mcp_server.tools import ToolHandler


def test_version():
    """Test version is set."""
    assert __version__ == "0.1.0"


def test_anki_client_init():
    """Test AnkiClient can be instantiated."""
    client = AnkiClient()
    assert client.url == "http://localhost:8765"
    assert client.timeout == 30.0


def test_anki_client_custom_port():
    """Test AnkiClient with custom port."""
    client = AnkiClient(url="http://localhost:8080")
    assert client.url == "http://localhost:8080"


def test_tool_handler_init():
    """Test ToolHandler can be instantiated."""
    client = AnkiClient()
    handler = ToolHandler(client)
    assert handler.client == client


def test_tool_handler_get_tool_list():
    """Test ToolHandler returns tool list."""
    client = AnkiClient()
    handler = ToolHandler(client)
    tools = handler.get_tool_list()
    assert len(tools) == 11
    tool_names = [t.name for t in tools]
    assert "list_decks" in tool_names
    assert "create_note" in tool_names
    assert "batch_create_notes" in tool_names


def test_resource_handler_init():
    """Test ResourceHandler can be instantiated."""
    client = AnkiClient()
    handler = ResourceHandler(client)
    assert handler.client == client
    assert handler.cache_expiry == 300


def test_resource_handler_get_resource_list():
    """Test ResourceHandler returns resource list."""
    client = AnkiClient()
    handler = ResourceHandler(client)
    resources = handler.get_resource_list()
    assert len(resources) == 1
    assert str(resources[0].uri) == "anki://decks/all"


def test_resource_handler_get_resource_templates():
    """Test ResourceHandler returns resource templates."""
    client = AnkiClient()
    handler = ResourceHandler(client)
    templates = handler.get_resource_templates()
    assert len(templates) == 4
    uris = [t.uriTemplate for t in templates]
    assert "anki://note-types/{modelName}" in uris
    assert "anki://decks/all" in uris


def test_anki_mcp_server_init():
    """Test AnkiMcpServer can be instantiated."""
    server = AnkiMcpServer()
    assert server.port == 8765
    assert isinstance(server.client, AnkiClient)
    assert isinstance(server.tool_handler, ToolHandler)
    assert isinstance(server.resource_handler, ResourceHandler)


def test_anki_mcp_server_custom_port():
    """Test AnkiMcpServer with custom port."""
    server = AnkiMcpServer(port=8080)
    assert server.port == 8080
    assert server.client.url == "http://localhost:8080"
