"""
Workshop: Math Operations MCP Server

Complete the TODOs to implement a full-featured math calculator using FastMCP.
"""

from mcp.server.fastmcp import FastMCP
from typing import Union


# TODO: Create MCP server with proper name and description
mcp = FastMCP("Math Calculator Server")


@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    return a + b


@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of the two numbers
    """
    return a * b


# TODO: Implement divide_numbers function
@mcp.tool()
def divide_numbers(a: float, b: float) -> Union[float, str]:
    """Divide the first number by the second.
    
    Args:
        a: Dividend (number to be divided)
        b: Divisor (number to divide by)
        
    Returns:
        Quotient of the division
        
    Raises:
        ValueError: When attempting to divide by zero
    """
    # TODO: Add division by zero check
    # TODO: Implement division operation
    pass


# TODO: Implement power_numbers function
@mcp.tool()
def power_numbers(base: float, exponent: float) -> float:
    """Raise base to the power of exponent.
    
    Args:
        base: The base number
        exponent: The power to raise the base to
        
    Returns:
        Result of base raised to exponent
    """
    # TODO: Implement power operation (hint: use ** operator)
    pass


# TODO: (BONUS) Implement subtract_numbers function
# Hint: Follow the same pattern as add_numbers


# TODO: (BONUS) Implement sqrt_number function
# Hint: Check for negative numbers and use ** 0.5


def test_server():
    """Test your server implementations."""
    print("Testing Math Calculator Server...")
    
    # Test basic operations
    print(f"Addition: 5 + 3 = {add_numbers(5.0, 3.0)}")
    print(f"Multiplication: 4 * 7 = {multiply_numbers(4.0, 7.0)}")
    
    # TODO: Test your implemented functions
    # print(f"Division: 15 / 3 = {divide_numbers(15.0, 3.0)}")
    # print(f"Power: 2 ^ 3 = {power_numbers(2.0, 3.0)}")
    
    # TODO: Test error cases
    # try:
    #     divide_numbers(5.0, 0.0)
    # except ValueError as e:
    #     print(f"Division by zero error: {e}")


if __name__ == "__main__":
    # Test the server
    test_server()
    
    print(f"\nServer '{mcp.name}' ready with {len(mcp.list_tools())} tools:")
    for tool in mcp.list_tools():
        print(f"  - {tool.name}: {tool.description}")
    
    # TODO: Uncomment when ready to run the server
    # print("\nStarting MCP server...")
    # mcp.run()