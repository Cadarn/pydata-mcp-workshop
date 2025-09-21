"""
Advanced Wikipedia MCP Server Workshop

Complete the TODOs to build a fully functional advanced MCP server.
"""

import logging
import requests

import wikipediaapi
from fastmcp import Context, FastMCP

logger = logging.getLogger(__name__)

wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="MCP-Wikipedia-Advanced-Workshop/1.0 (educational-purpose)",
)

mcp = FastMCP("Wikipedia Advanced Workshop Server")


def search_wikipedia_articles(query: str, limit: int = 8) -> list[str]:
    """Search Wikipedia articles by keyword.

    Args:
        query: Search query string
        limit: Maximum number of results to return

    Returns:
        List of article titles matching the query
    """
    try:
        search_url = "https://api.wikimedia.org/core/v1/wikipedia/en/search/page"
        params = {"q": query.strip(), "limit": limit}

        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        titles = [page["title"] for page in data.get("pages", [])]

        return titles

    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching Wikipedia: {e}")
        return []


def get_article_summary_basic(title: str, sentences: int = 3) -> str:
    """Get a basic summary of a Wikipedia article.

    Args:
        title: Wikipedia article title
        sentences: Number of sentences in summary

    Returns:
        Article summary text
    """
    try:
        page = wiki.page(title.strip())

        if not page.exists():
            return f"Article '{title}' not found"

        summary = page.summary
        if not summary:
            return f"No summary available for '{title}'"

        # Split into sentences and limit
        sentences_list = [s.strip() for s in summary.split(".") if s.strip()]
        limited_sentences = sentences_list[:sentences]

        result = ". ".join(limited_sentences)
        if result and not result.endswith("."):
            result += "."

        return result

    except Exception as e:
        logger.error(f"Error getting summary for {title}: {e}")
        return f"Error retrieving summary for '{title}'"


# NOTE: Using Context requires the function to be async
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
    # TODO: Add input validation - check if title is empty or whitespace only
    # HINT: Use title.strip() and check if it's truthy

    await ctx.info(f"Creating enhanced summary for: {title}")

    # TODO: Get the Wikipedia page and check if it exists
    # HINT: Use wiki.page(title.strip()) and check page.exists()

    # TODO: Get the raw text from the page
    # HINT: Use page.text

    # TODO: Use ctx.sample() to enhance the summary
    # HINT: Call ctx.sample() with a prompt asking to make the text more concise and engaging

    # TODO: Log success and return the enhanced summary

    # EXERCISE: Remove this pass and implement the function
    pass


# NOTE: Using Context requires the function to be async
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
    # TODO: Validate query input
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    await ctx.info(f"Interactive search for: {query}")

    # TODO: Search for Wikipedia articles using the helper function
    search_results = # Add code here
    if not search_results:
        return f"No Wikipedia articles found for '{query}'"

    # TODO: Handle single result case
    # HINT: If len(search_results) == 1, use get_article_summary_basic() and return

    # TODO: Create options text holding the titles of all search results
    # HINT: Use enumerate() to create numbered list like "1. Title\n2. Title\n..."

    # TODO: Request user to select an article
    # HINT: result = ctx.elicit(... Your options can go here...)

    # TODO: Process user selection and return a summary of the article
    #   Try title matching first: if user_input.lower() in title.lower()
    #   Fall back to number selection: int(user_input) for 1-based indexing
    # HINT: if result.action == "accept": checks if user input had a successful response
    #   

    # EXERCISE: Remove this pass and implement the interactive logic
    pass


# NOTE: Using Context requires the function to be async
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
    # TODO: Input validation
    # HINT: Check if not title or not title.strip() -> ValueError
    # HINT: Check if max_length < 100 or max_length > 10000 -> ValueError

    await ctx.info(f"Retrieving content for: {title}")
    # TODO: Report initial progress (0%)
    # HINT: await ctx.report_progress(...)

    # TODO: Check if there's any page content

    # TODO: Report progress after getting content (50%)

    # TODO: Truncate the content to our max_length variable
    # TODO: Report progress 75% after truncation logic
    
    # TODO: Report final progress (100%) and log completion
    # HINT: ctx.report_progress and ctx.info are your friends here

    # EXERCISE: Remove this pass and implement the function
    pass




if __name__ == "__main__":
    print(f"Starting advanced Wikipedia MCP server '{mcp.name}'...")
    print("\nAdvanced Features to Implement:")
    print("- smart_summarize: AI-enhanced summaries using ctx.sample()")
    print("- interactive_search: User disambiguation via ctx.elicit()")
    print("- get_article_with_progress: Context logging and progress reporting")
    print("\nServer will run on stdio transport for MCP clients to connect.")


    mcp.run()

