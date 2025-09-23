"""
Make sure an MCP server is running in a streaming fashion:
uv run fastmcp run solution/examples/03_pydata_server.py  --with httpx --transport http
"""

import asyncio
from fastmcp import Client

async def discover_server_capabilities():
    """Connect to MCP server and discover all available capabilities."""
    client = Client("http://localhost:8000/mcp")

    async with client:
        print("🔍 Discovering MCP Server Capabilities...")
        print("=" * 50)

        # List all available tools
        try:
            tools = await client.list_tools()
            print("\n📧 Available Tools:")
            print("-" * 20)
            if tools:
                for tool in tools:
                    print(f"  • {tool.name}")
                    if hasattr(tool, 'description') and tool.description:
                        print(f"    Description: {tool.description}")
                    print()
            else:
                print("  No tools available")
        except Exception as e:
            print(f"  Error listing tools: {e}")

        # List all available resources
        try:
            resources = await client.list_resources()
            print("\n📚 Available Resources:")
            print("-" * 22)
            if resources:
                for resource in resources:
                    print(f"  • URI: {resource.uri}")
                    if hasattr(resource, 'name') and resource.name:
                        print(f"    Name: {resource.name}")
                    if hasattr(resource, 'description') and resource.description:
                        print(f"    Description: {resource.description}")
                    if hasattr(resource, 'mime_type') and resource.mime_type:
                        print(f"    MIME Type: {resource.mime_type}")
                    print()
            else:
                print("  No resources available")
        except Exception as e:
            print(f"  Error listing resources: {e}")

        # List all available prompts
        try:
            prompts = await client.list_prompts()
            print("\n💬 Available Prompts:")
            print("-" * 21)
            if prompts:
                for prompt in prompts:
                    print(f"  • {prompt.name}")
                    if hasattr(prompt, 'description') and prompt.description:
                        print(f"    Description: {prompt.description}")
                    if hasattr(prompt, 'arguments') and prompt.arguments:
                        print(f"    Arguments: {[arg.name for arg in prompt.arguments]}")
                    print()
            else:
                print("  No prompts available")
        except Exception as e:
            print(f"  Error listing prompts: {e}")

        print("✅ Discovery complete!")

if __name__ == "__main__":
    asyncio.run(discover_server_capabilities())