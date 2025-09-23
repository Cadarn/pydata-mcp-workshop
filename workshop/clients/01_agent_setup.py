"""
Exercise 1: MCP Agent Setup

In this exercise, you'll complete the basic setup of an MCP client using PydanticAI.
This demonstrates the core integration between MCP servers and AI agents.

🎯 Learning Goals:
- Understand MCPServerStdio connection setup
- Learn how to integrate MCP servers with PydanticAI agents

🛠️ TODO: Complete the two missing pieces in the initialize() method
"""

import asyncio
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from rich.console import Console

from solution.clients.config import validate_environment

console = Console()


class MCPClientExercise:
    def __init__(self):
        self.agent: Agent | None = None
        self.server: MCPServerStdio | None = None

    # TODO: Fill this in
    async def initialize(self) -> bool:
        try:
            # Get the Wikipedia server path
            server_path = (
                Path(__file__).parent.parent / "servers" / "wikipedia_server.py"
            )

            # TODO 1: Create MCPServerStdio connection
            # Hint: Use "uv" as command, with args=["run", "python", str(server_path)]
            self.server = None  # Replace this line with your implementation

            # TODO 2: Create Agent with the server as a toolset
            # Hint: Use model="openai:gpt-4o-mini" and toolsets=[self.server]
            self.agent = None  # Replace this line with your implementation
            return True

        except Exception as e:
            console.print(f"❌ Failed to initialize: {e}")
            return False

    async def test_connection(self):
        if not self.agent:
            console.print("❌ Agent not initialized")
            return

        console.print("🔍 Testing agent connection...")

        # Test with a simple query that should use Wikipedia
        async with self.agent:
            try:
                result = await self.agent.run("What is Python programming language?")
                console.print(f"✅ Agent response: {result.output[:100]}...")
            except Exception as e:
                console.print(f"❌ Test failed: {e}")


async def main():
    console.print("[bold blue]Exercise 1: MCP Agent Setup[/bold blue]")
    console.print("Complete the TODOs in the initialize() method\n")

    if not validate_environment():
        console.print(
            "\n💡 Make sure you have OPENAI_API_KEY set and the Wikipedia server available!"
        )
        return
    client = MCPClientExercise()

    if await client.initialize():
        await client.test_connection()
    else:
        console.print("❌ Setup failed. Check your TODO implementations!")


if __name__ == "__main__":
    asyncio.run(main())
