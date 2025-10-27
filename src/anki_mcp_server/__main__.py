#!/usr/bin/env python3
"""CLI entry point for Anki MCP Server."""

import argparse
import sys
import os


# Set port from command line before importing server
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Anki MCP Server - MCP server for Anki flashcard integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="AnkiConnect port (default: 8765)",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Validate port
    if not 1 <= args.port <= 65535:
        print("Error: Port must be between 1 and 65535", file=sys.stderr)
        sys.exit(1)

    # Set port via environment variable for client
    os.environ["ANKI_CONNECT_PORT"] = str(args.port)

    # Import and run FastMCP server
    from anki_mcp_server.server_fastmcp import mcp

    mcp.run()


if __name__ == "__main__":
    main()
