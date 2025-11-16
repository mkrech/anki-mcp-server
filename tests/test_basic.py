"""Basic smoke tests for anki-mcp-server."""

import pytest

from anki_mcp_server import __version__
from anki_mcp_server.client import AnkiClient
from anki_mcp_server.resources import ResourceHandler


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
