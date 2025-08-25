from .app import mcp

# Import tools so they register via decorators
from . import tools_text  # noqa: F401
from .tools_render import render_pdf_page  # noqa: F401


def run() -> None:
    """Run the MCP server over stdio."""
    mcp.run_stdio()
