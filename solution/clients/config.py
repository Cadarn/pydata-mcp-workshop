"""
Configuration utilities for the Wikipedia Research Assistant CLI.

This module handles environment validation, path resolution,
and configuration management for the MCP client.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Template
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from rich.console import Console
from rich.panel import Panel

load_dotenv()

console = Console()


def get_openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY")


def test_ollama_env_variables() -> bool:
    required_vars = ["OLLAMA_MODEL", "OLLAMA_BASE_URL"]
    vars_set = [os.getenv(var) is not None for var in required_vars]
    return all(vars_set)


def get_ollama_model() -> OpenAIChatModel:
    model_ollama = OpenAIChatModel(
        model_name=os.getenv("OLLAMA_MODEL"),
        provider=OllamaProvider(base_url=os.getenv("OLLAMA_BASE_URL") + "/v1"),
    )
    return model_ollama


def get_project_root() -> Path:
    current = Path(__file__).resolve()

    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent

    return Path.cwd()


def get_wikipedia_server_path() -> Path:
    project_root = get_project_root()
    server_path = project_root / "solution" / "servers" / "wikipedia_server.py"

    if not server_path.exists():
        raise FileNotFoundError(f"Wikipedia server not found at {server_path}")

    return server_path


def validate_environment() -> bool:
    errors = []

    api_key = get_openai_api_key()
    if not api_key:
        if not test_ollama_env_variables():
            errors.append(
                "OLLAMA_MODEL and OLLAMA_BASE_URL environment variables are not set"
            )
            errors.append("OPENAI_API_KEY environment variable is not set")
    elif len(api_key) < 10:
        errors.append("OPENAI_API_KEY appears to be invalid (too short)")

    try:
        server_path = get_wikipedia_server_path()
        if not server_path.is_file():
            errors.append(f"Wikipedia server file not found: {server_path}")
    except FileNotFoundError as e:
        errors.append(str(e))

    if errors:
        console.print(
            Panel(
                "\n".join([f"❌ {error}" for error in errors]),
                title="❌ Environment Validation Failed",
                style="red",
            )
        )
        return False

    return True


def load_template(template_name: str, **kwargs) -> str:
    project_root = get_project_root()
    template_path = project_root / "solution" / "clients" / "templates" / template_name

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found at {template_path}")

    template_content = template_path.read_text()
    template = Template(template_content)

    return template.render(**kwargs)


def get_system_prompt() -> str:
    return load_template("system_template.j2")


def get_welcome_message(server_name: str) -> str:
    return load_template(
        "welcome_template.j2",
        server_name=server_name,
    )


def get_info_message() -> str:
    return load_template("info_template.j2")


def get_error_help_message() -> str:
    return load_template("error_help_template.j2")


def get_agent_config() -> dict:
    return {
        "model": "openai:gpt-4o-mini" if get_openai_api_key() else get_ollama_model(),
        "system_prompt": get_system_prompt(),
        "timeout": 30,
    }
