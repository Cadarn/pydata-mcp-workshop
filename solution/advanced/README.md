# Advanced Wikipedia MCP Server

This directory contains examples of FastMCP's advanced features, building on the
basic Wikipedia server from the workshop.

## Advanced Features Demonstrated

### 1. LLM Sampling (`ctx.sample()`)

**Tool**: `smart_summarize`

Shows how a server can ask the client's LLM for help during tool execution.

```python
@mcp.tool()
async def smart_summarize(title: str, ctx: Context) -> str:
    # Get raw Wikipedia summary
    page = wiki.page(title.strip())
    if not page.exists():
        raise ValueError(f"Article '{title}' not found on Wikipedia")

    raw_text = page.text

    # Use client's LLM to summarise the wikipedia article
    enhanced = await ctx.sample(
        f"Make this Wikipedia summary more concise and engaging while preserving key facts:\n\n{raw_text}",
        max_tokens=800,
    )

    await ctx.info(f"Enhanced summary created for: {title}")
    return enhanced.text
```

**Use case**: When you want to leverage the client's LLM to enhance or process
data.

### 2. Interactive Elicitation (`ctx.elicit()`)

**Tool**: `interactive_search`

Shows how a server can ask the user questions during tool execution.

```python
@mcp.tool()
async def interactive_search(query: str, ctx: Context) -> str:
    search_results = search_wikipedia(query, limit=8)

    if len(search_results) > 1:
        # Show titles and ask user to choose
        options_text = "\n".join([f"{i+1}. {title}" for i, title in enumerate(search_results)])

        result = await ctx.elicit(
            f"Found {len(search_results)} articles:\n\n{options_text}\n\nWhich article would you like?",
            response_type=str
        )

        if result.action == "accept":
            user_input = result.data.strip()

            # Users can type either:
            # 1. Part of the title name: "programming" -> "Python (programming language)"
            # 2. A number: "2" -> second article in list

            # Try title match first
            for title in search_results:
                if user_input.lower() in title.lower():
                    return get_summary(title)

            # Fall back to number selection
            try:
                choice_num = int(user_input)
                if 1 <= choice_num <= len(search_results):
                    return get_summary(search_results[choice_num - 1])
            except ValueError:
                pass
```

**Use case**: Disambiguation, confirmation prompts, or gathering additional
input during tool execution.

### 3. Context Integration

**Tool**: `get_article_with_progress`

Shows logging and progress reporting capabilities.

```python
@mcp.tool()
async def get_article_with_progress(title: str, ctx: Context) -> str:
    await ctx.info(f"Retrieving content for: {title}")
    await ctx.report_progress(0, 100)

    # ... do work ...

    await ctx.report_progress(50, 100)
    # ... more work ...

    await ctx.report_progress(100, 100)
    return content
```

**Use case**: Long-running operations where users benefit from progress updates
and detailed logging.

## Running the Advanced Server

```bash
cd solution/advanced
uv run python wikipedia_server_advanced.py
```

## Testing

```bash
cd solution/advanced
uv run pytest test_wikipedia_server_advanced.py -v
```

## Key Educational Points

1. **Server-Client Communication**: MCP isn't just about tools calling external
   APIs - servers can also call back to clients
2. **Interactive Workflows**: Tools don't have to be simple request-response -
   they can have multi-step interactions
3. **Progress and Logging**: Long operations can provide user feedback through
   the MCP protocol
4. **LLM Composition**: Servers can leverage the client's LLM as part of their
   processing pipeline

## When to Use These Features

- **`ctx.sample()`**: When you want to enhance/transform data using AI
- **`ctx.elicit()`**: When you need user input to disambiguate or confirm
  actions
- **`ctx.info/report_progress()`**: For long operations or when detailed logging
  helps users

These patterns show how MCP enables sophisticated, interactive AI workflows
beyond simple tool calling.
