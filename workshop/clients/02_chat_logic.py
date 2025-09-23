"""
Exercise 2: Chat Interface Logic

In this exercise, you'll implement the core conversation flow for an MCP-powered CLI.
This builds on Exercise 1 by adding interactive chat capabilities.

🎯 Learning Goals:
- Understand conversation flow with message history
- Learn how to handle user input in typer
- See how PydanticAI manages conversation state

🛠️ TODO: Complete the missing pieces in the chat_loop() method
"""

import asyncio
from datetime import datetime
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.messages import ModelMessage
from pydantic_ai.run import AgentRunResult
from rich.console import Console

from solution.clients.config import validate_environment

console = Console()


class ChatClientExercise:
    def __init__(self):
        self.agent: Agent | None = None
        self.server: MCPServerStdio | None = None
        self.last_result: AgentRunResult | None = None
        self.session_start_time: datetime = datetime.now()

    async def initialize(self) -> bool:
        try:
            server_path = (
                Path(__file__).parent.parent / "servers" / "wikipedia_server.py"
            )

            self.server = MCPServerStdio(
                "uv",
                args=["run", "python", str(server_path)],
                timeout=30.0,
            )

            self.agent = Agent(
                model="openai:gpt-4o-mini",
                toolsets=[self.server],
                system_prompt="You are a helpful research assistant with access to Wikipedia. "
                "Provide informative and accurate responses using the available tools.",
            )

            console.print("✅ MCP Agent initialized successfully!")
            return True

        except Exception as e:
            console.print(f"❌ Failed to initialize: {e}")
            return False

    def get_message_history(self) -> list[ModelMessage]:
        if self.last_result is not None:
            return self.last_result.new_messages()
        return []

    # TODO: Fill this in
    async def chat_loop(self):
        if not self.agent:
            console.print("❌ Agent not initialized")
            return

        console.print(
            f"[green]🤖 Research Assistant started at {self.session_start_time.strftime('%H:%M:%S')}[/green]"
        )
        console.print("[dim]Type 'quit', 'exit', or 'q' to end the session[/dim]\n")

        async with self.agent:
            while True:
                try:
                    # TODO 1: Get user input
                    # Hint: Use console.input() with a nice prompt like "[cyan]You:[/cyan] "
                    user_input = None  # Replace this line with your implementation

                    user_input = user_input.strip() if user_input else ""
                    if not user_input:
                        continue

                    # TODO 2: Handle quit commands
                    # Hint: Check if user_input.lower() is in ["quit", "exit", "q"]
                    # If so, print a goodbye message and break from the loop
                    # Your code here

                    console.print("[dim]🔍 Thinking...[/dim]")

                    # TODO 3: Run the agent with conversation history
                    # Hint: Use await self.agent.run() with user_input and message_history parameter
                    # See PydanticAI docs: https://ai.pydantic.dev/message-history/#using-messages-as-input-for-further-agent-runs                    # Store the result in self.last_result
                    message_history = self.get_message_history()
                    result = None  # Replace this line with your implementation
                    self.last_result = result

                    # Display the response
                    console.print(
                        f"[bold green]Assistant:[/bold green] {result.output}"
                    )
                    console.print()

                except KeyboardInterrupt:
                    console.print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    console.print(f"❌ Error: {e}")
                    console.print("Please try again.\n")

    async def cleanup(self):
        if self.server:
            try:
                console.print("🧹 Cleaning up...")
            except Exception as e:
                console.print(f"⚠️ Warning during cleanup: {e}")


async def main():
    console.print("[bold blue]Exercise 2: Chat Interface Logic[/bold blue]")
    console.print("Complete the TODOs in the chat_loop() method\n")

    if not validate_environment():
        console.print(
            "\n💡 Make sure you have OPENAI_API_KEY set and the Wikipedia server available!"
        )
        return

    client = ChatClientExercise()

    try:
        if await client.initialize():
            await client.chat_loop()
        else:
            console.print(
                "❌ Setup failed. Make sure the Wikipedia server is available!"
            )
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
