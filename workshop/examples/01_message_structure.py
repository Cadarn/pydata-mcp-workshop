"""
Workshop: MCP Message Structure Examples

Complete the TODOs to understand the JSON-RPC message format used in MCP communication.
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
                        # TODO: Add the input schema for two number parameters
                        # Hint: Use JSON Schema format with:
                        # - "type": "object"
                        # - "properties": dict with parameter definitions
                        # - "required": list of required parameter names
                        # Each property should have "type" and "description"
                    }
                }
            ]
        }
    }


def create_tool_call_request(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Create a tool invocation request."""
    # TODO: Complete the tool call request structure
    # Hint: Follow JSON-RPC 2.0 format with method "tools/call"
    # Include tool name and arguments in params
    return {
        "jsonrpc": "2.0",
        "id": 2,
        # TODO: Add method and params
    }


def create_tool_call_response(result: Any) -> dict[str, Any]:
    """Create a successful tool call response."""
    # TODO: Complete the response structure
    # Hint: Include result with content array containing text response
    pass


def create_error_response(error_code: int, error_message: str) -> dict[str, Any]:
    """Create an error response."""
    # TODO: Complete the error response structure
    # Hint: Use "error" field instead of "result" with code and message
    pass


def test_message_structures():
    """Test the message structure functions."""
    print("=== Testing MCP Message Structures ===\n")
    
    # Test tool discovery
    print("1. Tool Discovery Request:")
    discovery_request = create_tool_discovery_request()
    print(json.dumps(discovery_request, indent=2))
    
    print("\n2. Tool Discovery Response:")
    # TODO: Uncomment when you've completed the function
    # discovery_response = create_tool_discovery_response()
    # print(json.dumps(discovery_response, indent=2))
    
    # TODO: Test tool call request and response
    # TODO: Test error response


if __name__ == "__main__":
    test_message_structures()