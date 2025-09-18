"""
Solution: MCP Message Structure Examples

This module demonstrates the JSON-RPC message format used in MCP communication.
"""

import json
from typing import Any


def create_tool_discovery_request() -> dict[str, Any]:
    """Create a standard MCP tool discovery request."""
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }


def create_tool_discovery_response() -> dict[str, Any]:
    """Create a complete tool discovery response with proper schema."""
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "tools": [
                {
                    "name": "add_numbers",
                    "description": "Add two numbers together",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "number",
                                "description": "First number"
                            },
                            "b": {
                                "type": "number",
                                "description": "Second number"
                            }
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "multiply_numbers",
                    "description": "Multiply two numbers together",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "number",
                                "description": "First number"
                            },
                            "b": {
                                "type": "number",
                                "description": "Second number"
                            }
                        },
                        "required": ["a", "b"]
                    }
                }
            ]
        }
    }


def create_tool_call_request(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Create a tool invocation request."""
    return {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }


def create_tool_call_response(result: Any) -> dict[str, Any]:
    """Create a successful tool call response."""
    return {
        "jsonrpc": "2.0",
        "id": 2,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": str(result)
                }
            ]
        }
    }


def create_error_response(error_code: int, error_message: str) -> dict[str, Any]:
    """Create an error response."""
    return {
        "jsonrpc": "2.0",
        "id": 2,
        "error": {
            "code": error_code,
            "message": error_message
        }
    }


if __name__ == "__main__":
    # Demonstrate the message flow
    print("=== MCP Message Examples ===\n")
    
    # Tool discovery
    print("1. Tool Discovery Request:")
    print(json.dumps(create_tool_discovery_request(), indent=2))
    
    print("\n2. Tool Discovery Response:")
    print(json.dumps(create_tool_discovery_response(), indent=2))
    
    # Tool invocation
    print("\n3. Tool Call Request:")
    call_request = create_tool_call_request("add_numbers", {"a": 5, "b": 3})
    print(json.dumps(call_request, indent=2))
    
    print("\n4. Tool Call Response:")
    print(json.dumps(create_tool_call_response(8), indent=2))
    
    # Error handling
    print("\n5. Error Response:")
    error_response = create_error_response(-32602, "Invalid params: division by zero")
    print(json.dumps(error_response, indent=2))