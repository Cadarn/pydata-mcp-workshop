"""
Exercise 3: Polish

In this exercise, you'll add error handling and formatting (because nobody
likes an ugly UI) to create a CLI experience using the existing templates and configuration.

🎯 Learning Goals:
- Implement proper error handling for LLM applications
- Use Rich for terminal output formatting
- Leverage existing Jinja templates and configuration system

🛠️ TODO: Complete the missing pieces for error handling and Rich formatting
"""

import asyncio

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.messages import ModelMessage
from pydantic_ai.run import AgentRunResult
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from solution.clients.config import (
    get_agent_config,
    get_welcome_message,
    get_wikipedia_server_path,
    validate_environment,
)

console = Console()


class ProductionChatClient:
    def __init__(self):
        self.agent: Agent | None = None
        self.server: MCPServerStdio | None = None
        self.last_result: AgentRunResult | None = None
        self.server_name: str = "MCP Wikipedia Server"

    async def initialize(self) -> bool:
        try:
            config = get_agent_config()
            server_path = get_wikipedia_server_path()

            self.server = MCPServerStdio(
                "uv",
                args=["run", "python", str(server_path)],
                timeout=config["timeout"],
            )

            self.agent = Agent(
                model=config["model"],
                toolsets=[self.server],
                system_prompt=config["system_prompt"],
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

        welcome_text = get_welcome_message(server_name=self.server_name)
        console.print(Panel(welcome_text, title="Welcome"))
        console.print()

        async with self.agent:
            while True:
                try:
                    user_input = console.input("[cyan]You:[/cyan] ").strip()
                    if not user_input:
                        continue

                    if user_input.lower() in ["quit", "exit", "q"]:
                        console.print("👋 Thanks for using the Research Assistant!")
                        break

                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console,
                        transient=True,
                    ) as progress:
                        task = progress.add_task(
                            "🔍 Processing your request...", total=None
                        )

                        # TODO 1: Add proper try-except error handling around agent.run()
                        # Hint: Catch exceptions and update progress description accordingly
                        # See PydanticAI docs: https://ai.pydantic.dev/agents/#running-agents
                        message_history = self.get_message_history()

                        try:
                            result = await self.agent.run(
                                user_input, message_history=message_history
                            )
                            progress.update(task, description="✅ Request complete")
                            self.last_result = result
                        except Exception as e:
                            progress.update(task, description="❌ Request failed")
                            raise e

                    console.print()

                    # TODO 2: Format the response with a Rich Panel
                    # Hint: Use Panel() with title="Assistant", padding=(1, 2)
                    # See Rich Panel docs: https://rich.readthedocs.io/en/stable/panel.html
                    console.print(
                        result.output
                    )  # Replace this line with Panel formatting

                    console.print()

                except KeyboardInterrupt:
                    console.print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    console.print(f"❌ Error processing request: {e}")
                    console.print(
                        "Please try rephrasing your question or check your connection.\n"
                    )

    async def cleanup(self):
        """Clean up resources with proper error handling."""
        if self.server:
            try:
                console.print("🧹 Cleaning up resources...")
            except Exception as e:
                console.print(f"⚠️ Warning during cleanup: {e}")


async def main():
    console.print("[bold blue]Exercise 3: Production Polish[/bold blue]")
    console.print("Complete the TODOs for error handling and Rich formatting\n")

    if not validate_environment():
        console.print(
            "\n💡 Make sure you have OPENAI_API_KEY set and the Wikipedia server available!"
        )
        return

    client = ProductionChatClient()

    try:
        if await client.initialize():
            await client.chat_loop()
        else:
            console.print("❌ Setup failed. Check your environment configuration!")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n👋 Session interrupted. Goodbye!")
