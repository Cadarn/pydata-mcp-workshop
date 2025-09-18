#!/usr/bin/env python3
"""
Test script for Wikipedia MCP Server

This script launches the Wikipedia MCP server as a subprocess and tests
it by sending MCP protocol messages to verify it's working correctly.
"""

import subprocess
import json
import sys
import time
import os
from typing import Any


def send_mcp_request(process: subprocess.Popen, request: dict[str, Any]) -> dict[str, Any]:
    """Send an MCP request to the server and get the response."""
    request_line = json.dumps(request) + '\n'
    process.stdin.write(request_line.encode())
    process.stdin.flush()

    # Read response
    response_line = process.stdout.readline().decode().strip()
    if not response_line:
        raise Exception("No response from server")

    return json.loads(response_line)


def test_wikipedia_server():
    """Test the Wikipedia MCP server by launching it and sending requests."""
    print("🧪 Testing Wikipedia MCP Server...")

    # Start the server process
    server_script = os.path.join(os.path.dirname(__file__), 'wikipedia_server.py')

    try:
        print("📡 Starting MCP server...")
        process = subprocess.Popen(
            [sys.executable, server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False  # We'll handle encoding ourselves
        )

        # Give the server a moment to start
        time.sleep(1)

        # Test 1: Initialize MCP connection
        print("🔌 Testing MCP initialization...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        response = send_mcp_request(process, init_request)
        print(f"✅ Initialize response: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")

        # Test 2: List available tools
        print("🛠️  Testing tool listing...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        response = send_mcp_request(process, list_tools_request)
        tools = response.get('result', {}).get('tools', [])
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.get('name')}: {tool.get('description', 'No description')}")

        # Test 3: Test search_wikipedia tool
        if any(tool.get('name') == 'search_wikipedia' for tool in tools):
            print("🔍 Testing search_wikipedia tool...")
            search_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "search_wikipedia",
                    "arguments": {
                        "query": "artificial intelligence",
                        "limit": 3
                    }
                }
            }

            response = send_mcp_request(process, search_request)
            if 'result' in response:
                results = response['result'].get('content', [])
                if results and isinstance(results[0].get('text'), str):
                    search_results = json.loads(results[0]['text'])
                    print(f"✅ Search results: {search_results}")
                else:
                    print(f"⚠️  Unexpected search response format: {response}")
            else:
                print(f"❌ Search failed: {response}")

        print("\n🎉 MCP server test completed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        if 'process' in locals():
            stderr_output = process.stderr.read().decode()
            if stderr_output:
                print(f"Server stderr: {stderr_output}")

    finally:
        # Clean up
        if 'process' in locals():
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()


if __name__ == "__main__":
    test_wikipedia_server()