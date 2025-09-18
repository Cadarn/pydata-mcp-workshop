"""
Workshop: Wikipedia Search & Summarization MCP Server

Complete the TODOs to build a Wikipedia MCP server that provides
search and content retrieval capabilities.
"""

from fastmcp import FastMCP
import wikipediaapi
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server with appropriate name and description
mcp = FastMCP("Wikipedia Server")

# Initialize Wikipedia API client
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='MCP-Wikipedia-Workshop/1.0 (educational-purpose)'
)


@mcp.tool()
def search_wikipedia(query: str, limit: int = 5) -> list[str]:
    """Search Wikipedia articles by keyword.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return (default: 5, max: 10)
        
    Returns:
        list of article titles matching the query
        
    Raises:
        ValueError: If query is empty or limit is invalid
    """
    # TODO: Add input validation
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    if limit < 1 or limit > 10:
        raise ValueError("Limit must be between 1 and 10")
    
    try:
        # Use Wikipedia's REST API for search
        search_url = "https://en.wikipedia.org/api/rest_v1/page/search/title"
        params = {
            'q': query.strip(),
            'limit': limit
        }
        
        # TODO: Make HTTP request with timeout
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()

        # TODO: Extract titles from response
        data = response.json()
        titles = [page['title'] for page in data.get('pages', [])]

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
    # TODO: Add input validation
    if not title or not title.strip():
        raise ValueError("Article title cannot be empty")

    if sentences < 1 or sentences > 10:
        raise ValueError("Sentences must be between 1 and 10")

    try:
        # TODO: Get Wikipedia page and check if it exists
        page = wiki.page(title.strip())

        if not page.exists():
            raise ValueError(f"Article '{title}' not found on Wikipedia")

        # TODO: Process summary - EXERCISE FOR ATTENDEES
        # HINT: You need to:
        # 1. Get page.summary
        # 2. Split into sentences (split by '.')
        # 3. Take only first 'sentences' number of them
        # 4. Join back together with '. ' and add final '.'

        # REMOVE THIS PASS AND IMPLEMENT:
        pass
        
    except Exception as e:
        if "not found" in str(e).lower():
            raise
        logger.error(f"Error retrieving summary for {title}: {e}")
        raise ValueError(f"Failed to get article summary: {str(e)}")


# TODO: Implement get_article_content function
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
    # TODO: MAIN EXERCISE - Implement this entire function
    # Use the pattern from get_article_summary as a guide
    #
    # Step 1: Input validation
    #   - title not empty
    #   - max_length between 100-10000
    #
    # Step 2: Get and validate Wikipedia page
    #   - wiki.page(title.strip())
    #   - check page.exists()
    #
    # Step 3: Get and process content
    #   - page.text for full content
    #   - if len(content) > max_length: truncate smartly
    #   - find good breaking point (sentence/paragraph end)
    #   - add truncation message

    # Your implementation here:
    pass


# TODO: (BONUS) Implement get_article_info function
# This should return a dictionary with article metadata:
# - title, url, summary_length, content_length, categories, links_count


if __name__ == "__main__":
    print(f"Starting Wikipedia MCP server '{mcp.name}'...")
    print("Server will run on stdio transport for MCP clients to connect.")
    mcp.run()