"""
Advanced Wikipedia MCP Server Features

This module demonstrates FastMCP's advanced capabilities:
- LLM sampling for enhanced summaries (ctx.sample)
- Interactive elicitation for disambiguation (ctx.elicit)
- Context integration for progress reporting and logging

Educational code showing next-level MCP server patterns.
"""

import logging

import wikipediaapi
from fastmcp import Context, FastMCP

from solution.servers.wikipedia_server import get_article_summary, search_wikipedia

logger = logging.getLogger(__name__)

wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="MCP-Wikipedia-Advanced/1.0 (educational-purpose)",
)

mcp = FastMCP("Wikipedia Advanced Server")


@mcp.tool()
async def smart_summarize(title: str, ctx: Context) -> str:
    """Get an AI-enhanced summary of a Wikipedia article.

    Uses ctx.sample() to leverage the client's LLM for better summaries.

    Args:
        title: Wikipedia article title

    Returns:
        AI-enhanced article summary

    Raises:
        ValueError: If title is empty or article doesn't exist
    """
    await ctx.info(f"Creating enhanced summary for: {title}")

    page = wiki.page(title.strip())
    if not page.exists():
        raise ValueError(f"Article '{title}' not found on Wikipedia")

    raw_text = page.text

    enhanced = await ctx.sample(
        f"Make this Wikipedia summary more concise and engaging while preserving key facts:\n\n{raw_text}",
        max_tokens=800,
    )

    await ctx.info(f"Enhanced summary created for: {title}")
    return enhanced.text


@mcp.tool()
async def interactive_search(query: str, ctx: Context) -> str:
    """Search Wikipedia with interactive disambiguation.

    Uses ctx.elicit() for user interaction during tool execution.

    Args:
        query: Search query string

    Returns:
        Summary of user-selected article or cancellation message

    Raises:
        ValueError: If query is empty
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    await ctx.info(f"Interactive search for: {query}")

    search_results = search_wikipedia.fn(query, limit=8)

    if not search_results:
        return f"No Wikipedia articles found for '{query}'"

    if len(search_results) == 1:
        await ctx.info("Only one result found, retrieving summary...")
        return get_article_summary.fn(search_results[0])

    options_text = "\n".join(
        [f"{i + 1}. {title}" for i, title in enumerate(search_results)]
    )

    result = await ctx.elicit(
        f"Found {len(search_results)} Wikipedia articles for '{query}':\n\n{options_text}\n\nWhich article would you like?",
        response_type=str,
    )

    if result.action == "accept":
        user_input = result.data.strip()

        # Try to match by title first (partial match)
        for title in search_results:
            if user_input.lower() in title.lower():
                await ctx.info(f"User selected by title match: {title}")
                return get_article_summary.fn(title)

        # Fall back to number selection
        try:
            choice_num = int(user_input)
            if 1 <= choice_num <= len(search_results):
                selected_title = search_results[choice_num - 1]
                await ctx.info(f"User selected by number: {selected_title}")
                return get_article_summary.fn(selected_title)
        except ValueError:
            pass

        return f"Invalid selection '{user_input}'. Please enter a title name or number 1-{len(search_results)}."
    else:
        return "Search cancelled or invalid selection."


@mcp.tool()
async def get_article_with_progress(
    ctx: Context, title: str, max_length: int = 2000
) -> str:
    """Get article content with progress reporting.

    Demonstrates Context integration for progress reporting and logging.

    Args:
        title: Wikipedia article title
        max_length: Maximum content length in characters (default: 2000, max: 10000)

    Returns:
        Article content text (truncated if longer than max_length)

    Raises:
        ValueError: If title is empty or article doesn't exist
    """
    if not title or not title.strip():
        raise ValueError("Article title cannot be empty")

    if max_length < 100 or max_length > 10000:
        raise ValueError("max_length must be between 100 and 10000")

    await ctx.info(f"Retrieving content for: {title}")
    await ctx.report_progress(0, 100)

    page = wiki.page(title.strip())

    if not page.exists():
        raise ValueError(f"Article '{title}' not found on Wikipedia")

    await ctx.report_progress(25, 100)
    content = page.text

    if not content:
        raise ValueError(f"No content available for article '{title}'")

    await ctx.report_progress(50, 100)

    # Truncate if necessary
    if len(content) > max_length:
        await ctx.info(f"Content is {len(content)} chars, truncating to {max_length}")
        await ctx.report_progress(75, 100)

        truncated = content[:max_length]
        last_period = truncated.rfind(".")
        last_newline = truncated.rfind("\n")

        break_point = max(last_period, last_newline)
        if break_point > max_length * 0.8:
            content = content[: break_point + 1] + "\n\n[Content truncated...]"
        else:
            content = truncated + "...\n\n[Content truncated...]"

    await ctx.report_progress(100, 100)
    await ctx.info(f"Retrieved content for: {title} ({len(content)} chars)")
    return content


if __name__ == "__main__":
    print(f"Starting advanced Wikipedia MCP server '{mcp.name}'...")
    print("\nAdvanced Features Demonstrated:")
    print("- smart_summarize: AI-enhanced summaries using ctx.sample()")
    print("- interactive_search: User disambiguation via ctx.elicit()")
    print("- get_article_with_progress: Context logging and progress reporting")
    print("\nServer will run on stdio transport for MCP clients to connect.")
    mcp.run()
