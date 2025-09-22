"""
MCP Research Assistant CLI

A generic CLI application that uses PydanticAI with MCP
to provide research assistance through a chat interface.
Works with any MCP server by dynamically discovering available tools.
"""

import asyncio
import sys
from datetime import datetime

import typer
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse
from pydantic_ai.run import AgentRunResult
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from solution.clients.config import (
    get_agent_config,
    get_error_help_message,
    get_info_message,
    get_welcome_message,
    get_wikipedia_server_path,
    validate_environment,
)

console = Console()

app = typer.Typer(
    name="mcp-research",
    help="🔍 MCP Research Assistant - Intelligent research using MCP and PydanticAI",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


class ChatMessage:
    def __init__(self, role: str, content: str, timestamp: datetime | None = None):
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now()

    @staticmethod
    def convert_messages_for_display(
        messages: list[ModelMessage],
    ) -> list["ChatMessage"]:
        """Convert PydanticAI ModelMessage objects to ChatMessage objects for display."""
        display_messages = []

        for message in messages:
            if isinstance(message, ModelRequest):
                for part in message.parts:
                    if hasattr(part, "content") and part.content:
                        if part.__class__.__name__ == "UserPromptPart":
                            display_messages.append(
                                ChatMessage(
                                    role="user",
                                    content=part.content,
                                    timestamp=getattr(
                                        part, "timestamp", datetime.now()
                                    ),
                                )
                            )
            elif isinstance(message, ModelResponse):
                content_parts = []
                for part in message.parts:
                    if hasattr(part, "content") and part.content:
                        if part.__class__.__name__ == "TextPart":
                            content_parts.append(part.content)

                if content_parts:
                    display_messages.append(
                        ChatMessage(
                            role="assistant",
                            content=" ".join(content_parts),
                            timestamp=getattr(message, "timestamp", datetime.now()),
                        )
                    )

        return display_messages


class MCPResearchAssistant:
    def __init__(self):
        self.agent: Agent | None = None
        self.server: MCPServerStdio | None = None
        self.server_name: str = "MCP Server"
        self.last_result: AgentRunResult | None = None
        self.session_start_time: datetime = datetime.now()

    async def initialize(self) -> bool:
        try:
            config = get_agent_config()
            server_path = get_wikipedia_server_path()

            # NOTE: Hard locked to Wikipedia Server for purposes of this demo.
            # Can change this to dynamically load n servers through some config file.
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

            console.print("✅ MCP Server connected successfully")
            return True

        except Exception as e:
            console.print(f"❌ Failed to initialize: {e}")
            return False

    def get_message_history_for_next_run(self) -> list[ModelMessage]:
        if self.last_result is not None:
            return self.last_result.new_messages()
        return []

    def display_chat_history(self) -> None:
        if not self.last_result:
            console.print("📝 No chat history yet")
            return

        all_messages = self.last_result.all_messages()
        display_messages = ChatMessage.convert_messages_for_display(all_messages)

        if not display_messages:
            console.print("📝 No chat history yet")
            return

        table = Table(
            title=f"Chat History (Session started: {self.session_start_time.strftime('%H:%M:%S')})"
        )
        table.add_column("Time", style="dim", width=8)
        table.add_column("Role", style="bold", width=10)
        table.add_column("Message", style="white")

        for msg in display_messages:
            role_color = "cyan" if msg.role == "user" else "green"
            time_str = msg.timestamp.strftime("%H:%M:%S")

            content = msg.content
            if len(content) > 80:
                content = content[:77] + "..."

            table.add_row(
                time_str, f"[{role_color}]{msg.role.title()}[/{role_color}]", content
            )

        console.print(table)

    async def chat_session(self):
        if not self.agent:
            console.print("❌ Agent not initialized")
            return

        welcome_text = get_welcome_message(
            server_name=self.server_name,
        )

        console.print(Panel(welcome_text))
        console.print()

        async with self.agent:
            while True:
                try:
                    user_input = console.input("[cyan]You:[/cyan] ").strip()
                    user_input_lower = user_input.lower()

                    if user_input_lower in ["quit", "exit", "q"]:
                        console.print("👋 Thanks for using MCP Research Assistant!")
                        break

                    if user_input_lower in ["history", "hist", "h"]:
                        self.display_chat_history()
                        console.print()
                        continue

                    if user_input_lower in ["clear", "clear history", "reset"]:
                        self.last_result = None
                        console.print("🗑️  Chat history cleared")
                        console.print()
                        continue

                    if not user_input:
                        continue

                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console,
                        transient=True,
                    ) as progress:
                        task = progress.add_task(
                            "🔍 Processing your request...", total=None
                        )

                        try:
                            message_history = self.get_message_history_for_next_run()
                            result = await self.agent.run(
                                user_input, message_history=message_history
                            )
                            progress.update(task, description="✅ Request complete")

                            self.last_result = result

                        except Exception as e:
                            progress.update(task, description="❌ Request failed")
                            raise e

                    console.print()
                    console.print(
                        Panel(
                            result.output,
                            title="[bold green]Assistant[/bold green]",
                            padding=(1, 2),
                        )
                    )
                    console.print()

                except KeyboardInterrupt:
                    console.print("\n👋 Goodbye!")
                    break

                except Exception as e:
                    console.print(f"\n❌ Error processing your request: {e}")
                    console.print(
                        "Please try rephrasing your question or check your connection.\n"
                    )

    async def cleanup(self):
        if self.server:
            try:
                console.print("🧹 Cleaning up resources...")
            except Exception as e:
                console.print(f"⚠️  Warning during cleanup: {e}")


async def run_session():
    assistant = MCPResearchAssistant()

    try:
        if await assistant.initialize():
            await assistant.chat_session()
        else:
            console.print("❌ Failed to start research assistant")
            raise typer.Exit(1)
    finally:
        await assistant.cleanup()


@app.command()
def chat():
    if not validate_environment():
        console.print(f"\n{get_error_help_message()}")
        raise typer.Exit(1)

    try:
        asyncio.run(run_session())
    except KeyboardInterrupt:
        console.print("\n👋 Session interrupted. Goodbye!")
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}")
        raise typer.Exit(1)


@app.command()
def info():
    info_text = get_info_message()
    console.print(Panel(info_text))


def main():
    try:
        app()
    except Exception as e:
        console.print(f"❌ Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
