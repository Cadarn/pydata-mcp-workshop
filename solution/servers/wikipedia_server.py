"""
Solution: Wikipedia Search & Summarization MCP Server

This server provides Wikipedia search and content retrieval capabilities
through MCP tools, demonstrating real-world API integration.
"""

from mcp.server.fastmcp import FastMCP
import wikipediaapi
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("Wikipedia Server")

# Initialize Wikipedia API client
wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="MCP-Wikipedia-Server/1.0 (educational-purpose)",
)


@mcp.tool()
def search_wikipedia(query: str, limit: int = 5) -> list[str]:
    """Search Wikipedia articles by keyword.

    Args:
        query: Search query string
        limit: Maximum number of results to return (default: 5, max: 10)

    Returns:
        List of article titles matching the query

    Raises:
        ValueError: If query is empty or limit is invalid
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    if limit < 1 or limit > 10:
        raise ValueError("Limit must be between 1 and 10")

    try:
        # Use Wikimedia Core API for search
        search_url = "https://api.wikimedia.org/core/v1/wikipedia/en/search/page"
        params = {"q": query.strip(), "limit": limit}
        headers = {
            "User-Agent": "MCP-Wikipedia-Server/1.0 (educational-purpose)",
            "Accept": "application/json",
        }

        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        titles = [page["title"] for page in data.get("pages", [])]

        logger.info(f"Found {len(titles)} results for query: {query}")
        return titles

    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching Wikipedia: {e}")
        raise ValueError(f"Failed to search Wikipedia: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during search: {e}")
        raise ValueError(f"Search failed: {str(e)}")


@mcp.tool()
def get_article_summary(title: str, sentences: int = 3) -> str:
    """Get a brief summary of a Wikipedia article.

    Args:
        title: Wikipedia article title
        sentences: Number of sentences in summary (default: 3, max: 10)

    Returns:
        Article summary text

    Raises:
        ValueError: If title is empty or article doesn't exist
    """
    if not title or not title.strip():
        raise ValueError("Article title cannot be empty")

    if sentences < 1 or sentences > 10:
        raise ValueError("Sentences must be between 1 and 10")

    try:
        page = wiki.page(title.strip())

        if not page.exists():
            raise ValueError(f"Article '{title}' not found on Wikipedia")

        # Get summary with requested sentence count
        summary = page.summary

        if not summary:
            raise ValueError(f"No summary available for article '{title}'")

        # Split into sentences and limit
        sentences_list = [s.strip() for s in summary.split(".") if s.strip()]
        limited_sentences = sentences_list[:sentences]

        result = ". ".join(limited_sentences)
        if result and not result.endswith("."):
            result += "."

        logger.info(f"Retrieved summary for: {title}")
        return result

    except Exception as e:
        if "not found" in str(e).lower():
            raise
        logger.error(f"Error retrieving summary for {title}: {e}")
        raise ValueError(f"Failed to get article summary: {str(e)}")


@mcp.tool()
def get_article_content(title: str, max_length: int = 2000) -> str:
    """Get the full content of a Wikipedia article (truncated if necessary).

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

    try:
        page = wiki.page(title.strip())

        if not page.exists():
            raise ValueError(f"Article '{title}' not found on Wikipedia")

        content = page.text

        if not content:
            raise ValueError(f"No content available for article '{title}'")

        # Truncate if necessary
        if len(content) > max_length:
            # Find a good breaking point (end of sentence or paragraph)
            truncated = content[:max_length]

            # Try to break at sentence end
            last_period = truncated.rfind(".")
            last_newline = truncated.rfind("\n")

            break_point = max(last_period, last_newline)
            if break_point > max_length * 0.8:  # Only use if reasonably close to limit
                content = content[: break_point + 1] + "\n\n[Content truncated...]"
            else:
                content = truncated + "...\n\n[Content truncated...]"

        logger.info(f"Retrieved content for: {title} ({len(content)} chars)")
        return content

    except Exception as e:
        if "not found" in str(e).lower():
            raise
        logger.error(f"Error retrieving content for {title}: {e}")
        raise ValueError(f"Failed to get article content: {str(e)}")


@mcp.tool()
def get_article_info(title: str) -> dict:
    """Get basic information about a Wikipedia article.

    Args:
        title: Wikipedia article title

    Returns:
        Dictionary containing article metadata

    Raises:
        ValueError: If title is empty or article doesn't exist
    """
    if not title or not title.strip():
        raise ValueError("Article title cannot be empty")

    try:
        page = wiki.page(title.strip())

        if not page.exists():
            raise ValueError(f"Article '{title}' not found on Wikipedia")

        info = {
            "title": page.title,
            "url": page.fullurl,
            "summary_length": len(page.summary),
            "content_length": len(page.text),
            "categories": list(page.categories.keys())[:10],  # Limit categories
            "links_count": len(page.links),
        }

        logger.info(f"Retrieved info for: {title}")
        return info

    except Exception as e:
        if "not found" in str(e).lower():
            raise
        logger.error(f"Error retrieving info for {title}: {e}")
        raise ValueError(f"Failed to get article info: {str(e)}")


def test_server():
    """Test all server functions."""
    print("Testing Wikipedia MCP Server...")

    try:
        # Test search
        print("\n1. Testing search...")
        search_results = search_wikipedia("artificial intelligence", 3)
        print(f"Search results: {search_results}")

        # Test summary
        if search_results:
            print(f"\n2. Testing summary for '{search_results[0]}'...")
            summary = get_article_summary(search_results[0], 2)
            print(f"Summary: {summary[:200]}...")

            # Test content
            print(f"\n3. Testing content for '{search_results[0]}'...")
            content = get_article_content(search_results[0], 500)
            print(f"Content length: {len(content)} chars")
            print(f"Content preview: {content[:100]}...")

            # Test info
            print(f"\n4. Testing article info...")
            info = get_article_info(search_results[0])
            print(f"Article info: {info}")

        # Test error cases
        print("\n5. Testing error handling...")
        try:
            search_wikipedia("")
        except ValueError as e:
            print(f"✓ Empty search error: {e}")

        try:
            get_article_summary("NonExistentArticle123456")
        except ValueError as e:
            print(f"✓ Missing article error: {e}")

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    print(f"Starting Wikipedia MCP server '{mcp.name}'...")
    print("Server will run on stdio transport for MCP clients to connect.")
    mcp.run()

