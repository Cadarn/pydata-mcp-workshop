#!/usr/bin/env python3
"""
Test script for Wikipedia MCP Server (Solution)

This script launches the Wikipedia MCP server as a subprocess and tests
it by sending MCP protocol messages to verify all functionality is working.
"""

import subprocess
import json
import sys
import time
import os
from typing import Dict, Any, List


def send_mcp_request(process: subprocess.Popen, request: Dict[str, Any]) -> Dict[str, Any]:
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
    print("🧪 Testing Wikipedia MCP Server (Solution)...")

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

        # Test 4: Test get_article_summary tool
        if any(tool.get('name') == 'get_article_summary' for tool in tools):
            print("📄 Testing get_article_summary tool...")
            summary_request = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "get_article_summary",
                    "arguments": {
                        "title": "Artificial intelligence",
                        "sentences": 2
                    }
                }
            }

            response = send_mcp_request(process, summary_request)
            if 'result' in response:
                results = response['result'].get('content', [])
                if results and isinstance(results[0].get('text'), str):
                    summary = json.loads(results[0]['text'])
                    print(f"✅ Summary: {summary[:100]}...")
                else:
                    print(f"⚠️  Unexpected summary response format: {response}")
            else:
                print(f"❌ Summary failed: {response}")

        # Test 5: Test get_article_content tool
        if any(tool.get('name') == 'get_article_content' for tool in tools):
            print("📖 Testing get_article_content tool...")
            content_request = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "get_article_content",
                    "arguments": {
                        "title": "Python (programming language)",
                        "max_length": 500
                    }
                }
            }

            response = send_mcp_request(process, content_request)
            if 'result' in response:
                results = response['result'].get('content', [])
                if results and isinstance(results[0].get('text'), str):
                    content = json.loads(results[0]['text'])
                    print(f"✅ Content length: {len(content)} chars")
                else:
                    print(f"⚠️  Unexpected content response format: {response}")
            else:
                print(f"❌ Content failed: {response}")

        # Test 6: Test get_article_info tool
        if any(tool.get('name') == 'get_article_info' for tool in tools):
            print("ℹ️  Testing get_article_info tool...")
            info_request = {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {
                    "name": "get_article_info",
                    "arguments": {
                        "title": "Python (programming language)"
                    }
                }
            }

            response = send_mcp_request(process, info_request)
            if 'result' in response:
                results = response['result'].get('content', [])
                if results and isinstance(results[0].get('text'), str):
                    info = json.loads(results[0]['text'])
                    print(f"✅ Article info: {info.get('title')} - {info.get('content_length', 0)} chars")
                else:
                    print(f"⚠️  Unexpected info response format: {response}")
            else:
                print(f"❌ Info failed: {response}")

        print("\n🎉 All MCP server tests completed!")

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