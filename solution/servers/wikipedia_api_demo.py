"""
Wikipedia API Demonstration

This script shows how to interact with Wikipedia's API directly,
which helps understand what we're wrapping in our MCP server.
"""

import wikipediaapi
import requests
from typing import Any


def demo_wikipedia_search(query: str) -> list[dict[str, Any]]:
    """Demonstrate Wikipedia search using REST API."""
    print(f"🔍 Searching Wikipedia for: '{query}'")
    
    search_url = "https://en.wikipedia.org/api/rest_v1/page/search/title"
    params = {
        'q': query,
        'limit': 5
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        pages = data.get('pages', [])
        
        print(f"📄 Found {len(pages)} results:")
        for i, page in enumerate(pages, 1):
            print(f"  {i}. {page['title']} (Score: {page.get('score', 'N/A')})")
        
        return pages
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []


def demo_wikipedia_content(title: str) -> dict[str, Any]:
    """Demonstrate Wikipedia content retrieval using wikipedia-api."""
    print(f"\n📖 Getting content for: '{title}'")
    
    # Initialize Wikipedia API client
    wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='Wikipedia-API-Demo/1.0 (educational-purpose)'
    )
    
    try:
        page = wiki.page(title)
        
        if not page.exists():
            print(f"❌ Article '{title}' not found")
            return {}
        
        info = {
            "title": page.title,
            "url": page.fullurl,
            "summary": page.summary[:300] + "..." if len(page.summary) > 300 else page.summary,
            "content_length": len(page.text),
            "categories_count": len(page.categories),
            "links_count": len(page.links)
        }
        
        print(f"✅ Article found:")
        print(f"   Title: {info['title']}")
        print(f"   URL: {info['url']}")
        print(f"   Content Length: {info['content_length']:,} characters")
        print(f"   Categories: {info['categories_count']}")
        print(f"   Links: {info['links_count']}")
        print(f"   Summary: {info['summary']}")
        
        return info
        
    except Exception as e:
        print(f"❌ Content error: {e}")
        return {}


def demo_error_handling():
    """Demonstrate proper error handling."""
    print(f"\n🛡️ Testing error handling:")
    
    # Test empty search
    print("\n1. Empty search query:")
    demo_wikipedia_search("")
    
    # Test non-existent article
    print("\n2. Non-existent article:")
    demo_wikipedia_content("ThisArticleAbsolutelyDoesNotExist123456")
    
    # Test network timeout (simulate with very short timeout)
    print("\n3. Network timeout simulation:")
    try:
        response = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/search/title",
            params={'q': 'test'},
            timeout=0.001  # Very short timeout to force timeout
        )
    except requests.exceptions.Timeout:
        print("   ✅ Timeout handled correctly")
    except Exception as e:
        print(f"   ⚠️ Different error occurred: {e}")


def main():
    """Run the Wikipedia API demonstration."""
    print("🌟 Wikipedia API Demonstration")
    print("=" * 50)
    
    # Demo search
    search_results = demo_wikipedia_search("artificial intelligence")
    
    # Demo content retrieval with first result
    if search_results:
        first_result = search_results[0]['title']
        demo_wikipedia_content(first_result)
    
    # Demo another specific article
    demo_wikipedia_content("Python (programming language)")
    
    # Demo error handling
    demo_error_handling()
    
    print(f"\n🎯 Key takeaways:")
    print("   - Wikipedia has both REST API and Python library")
    print("   - Always handle network errors and missing articles")
    print("   - Content can be very long - consider truncation")
    print("   - Search returns relevance scores")
    print("   - Articles have rich metadata (categories, links, etc.)")


if __name__ == "__main__":
    main()