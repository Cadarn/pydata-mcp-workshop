"""
Solution: Complete Math Operations MCP Server

This module implements a full-featured math calculator using FastMCP.
"""

from fastmcp import FastMCP
from typing import Union


# Create MCP server with metadata
mcp = FastMCP(
    name="Math Calculator Server",
    description="A comprehensive math calculator supporting basic arithmetic operations"
)


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
def subtract_numbers(a: float, b: float) -> float:
    """Subtract the second number from the first.
    
    Args:
        a: Number to subtract from
        b: Number to subtract
        
    Returns:
        Difference of the two numbers
    """
    return a - b


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


@mcp.tool()
def divide_numbers(a: float, b: float) -> Union[float, str]:
    """Divide the first number by the second.
    
    Args:
        a: Dividend (number to be divided)
        b: Divisor (number to divide by)
        
    Returns:
        Quotient of the division or error message
        
    Raises:
        ValueError: When attempting to divide by zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.tool()
def power_numbers(base: float, exponent: float) -> float:
    """Raise base to the power of exponent.
    
    Args:
        base: The base number
        exponent: The power to raise the base to
        
    Returns:
        Result of base raised to exponent
    """
    return base ** exponent


@mcp.tool()
def sqrt_number(number: float) -> Union[float, str]:
    """Calculate the square root of a number.
    
    Args:
        number: Number to calculate square root of
        
    Returns:
        Square root of the number
        
    Raises:
        ValueError: When attempting to take square root of negative number
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return number ** 0.5


@mcp.tool()
def modulo_numbers(a: float, b: float) -> Union[float, str]:
    """Calculate the remainder when a is divided by b.
    
    Args:
        a: Dividend
        b: Divisor
        
    Returns:
        Remainder of a divided by b
        
    Raises:
        ValueError: When attempting to use zero as divisor
    """
    if b == 0:
        raise ValueError("Cannot calculate modulo with zero divisor")
    return a % b


def test_server():
    """Test all server functions."""
    print("Testing Math Calculator Server...")
    
    # Test all operations
    test_cases = [
        ("add_numbers", (5.0, 3.0), 8.0),
        ("subtract_numbers", (10.0, 4.0), 6.0),
        ("multiply_numbers", (4.0, 7.0), 28.0),
        ("divide_numbers", (15.0, 3.0), 5.0),
        ("power_numbers", (2.0, 3.0), 8.0),
        ("sqrt_number", (16.0,), 4.0),
        ("modulo_numbers", (17.0, 5.0), 2.0),
    ]
    
    for func_name, args, expected in test_cases:
        func = globals()[func_name]
        result = func(*args)
        status = "✓" if result == expected else "✗"
        print(f"{status} {func_name}{args} = {result} (expected {expected})")
    
    # Test error cases
    print("\nTesting error cases:")
    try:
        divide_numbers(5.0, 0.0)
        print("✗ Division by zero should raise error")
    except ValueError as e:
        print(f"✓ Division by zero error: {e}")
    
    try:
        sqrt_number(-4.0)
        print("✗ Square root of negative should raise error")
    except ValueError as e:
        print(f"✓ Square root negative error: {e}")


if __name__ == "__main__":
    # Test the server
    test_server()
    
    print(f"\nServer '{mcp.name}' ready with {len(mcp.list_tools())} tools:")
    for tool in mcp.list_tools():
        print(f"  - {tool.name}: {tool.description}")
    
    # Run the server
    print("\nStarting MCP server...")
    mcp.run()