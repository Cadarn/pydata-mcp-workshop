from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp import Context

from solution.advanced import wikipedia_server


class TestSmartSummarize:
    @patch("solution.advanced.wikipedia_server.wiki")
    @pytest.mark.asyncio
    async def test_smart_summarize_enhances_content(self, mock_wiki: MagicMock) -> None:
        mock_page = MagicMock()
        mock_page.exists.return_value = True
        mock_page.summary = "Original Wikipedia summary."
        mock_wiki.page.return_value = mock_page

        mock_context = AsyncMock(spec=Context)
        mock_sample_response = MagicMock()
        mock_sample_response.text = "Enhanced AI summary."
        mock_context.sample.return_value = mock_sample_response

        result = await wikipedia_server.smart_summarize.fn("Test Article", mock_context)

        assert result == "Enhanced AI summary."
        mock_context.sample.assert_called_once()

    @patch("solution.advanced.wikipedia_server.wiki")
    @pytest.mark.asyncio
    async def test_smart_summarize_handles_nonexistent_article(
        self, mock_wiki: MagicMock
    ) -> None:
        mock_page = MagicMock()
        mock_page.exists.return_value = False
        mock_wiki.page.return_value = mock_page

        mock_context = AsyncMock(spec=Context)

        with pytest.raises(ValueError, match="Article 'Nonexistent' not found"):
            await wikipedia_server.smart_summarize.fn("Nonexistent", mock_context)


class TestInteractiveSearch:
    @patch("solution.advanced.wikipedia_server.search_wikipedia")
    @patch("solution.advanced.wikipedia_server.get_article_summary")
    @pytest.mark.asyncio
    async def test_interactive_search_single_result_returns_summary(
        self, mock_get_summary: MagicMock, mock_search: MagicMock
    ) -> None:
        mock_search.fn.return_value = ["Single Article"]
        mock_get_summary.fn.return_value = "Article summary"

        mock_context = AsyncMock(spec=Context)

        result = await wikipedia_server.interactive_search.fn(
            "unique query", mock_context
        )

        assert result == "Article summary"
        mock_context.elicit.assert_not_called()

    @patch("solution.advanced.wikipedia_server.search_wikipedia")
    @patch("solution.advanced.wikipedia_server.get_article_summary")
    @pytest.mark.asyncio
    async def test_interactive_search_multiple_results_elicits_choice(
        self, mock_get_summary: MagicMock, mock_search: MagicMock
    ) -> None:
        mock_search.fn.return_value = ["Article 1", "Article 2", "Article 3"]
        mock_get_summary.fn.return_value = "Selected article summary"

        mock_context = AsyncMock(spec=Context)
        mock_elicit_result = MagicMock()
        mock_elicit_result.action = "accept"
        mock_elicit_result.data = "2"
        mock_context.elicit.return_value = mock_elicit_result

        result = await wikipedia_server.interactive_search.fn(
            "ambiguous query", mock_context
        )

        assert result == "Selected article summary"
        mock_context.elicit.assert_called_once()

    @patch("solution.advanced.wikipedia_server.search_wikipedia")
    @patch("solution.advanced.wikipedia_server.get_article_summary")
    @pytest.mark.asyncio
    async def test_interactive_search_accepts_title_match(
        self, mock_get_summary: MagicMock, mock_search: MagicMock
    ) -> None:
        mock_search.fn.return_value = [
            "Python (programming language)",
            "Python (mythology)",
            "Python (snake)",
        ]
        mock_get_summary.fn.return_value = "Programming language summary"

        mock_context = AsyncMock(spec=Context)
        mock_elicit_result = MagicMock()
        mock_elicit_result.action = "accept"
        mock_elicit_result.data = "programming"
        mock_context.elicit.return_value = mock_elicit_result

        result = await wikipedia_server.interactive_search.fn("python", mock_context)

        assert result == "Programming language summary"
        mock_get_summary.fn.assert_called_once_with("Python (programming language)")

    @patch("solution.advanced.wikipedia_server.search_wikipedia")
    @pytest.mark.asyncio
    async def test_interactive_search_handles_user_cancellation(
        self, mock_search: MagicMock
    ) -> None:
        mock_search.fn.return_value = ["Article 1", "Article 2"]

        mock_context = AsyncMock(spec=Context)
        mock_elicit_result = MagicMock()
        mock_elicit_result.action = "decline"
        mock_context.elicit.return_value = mock_elicit_result

        result = await wikipedia_server.interactive_search.fn("query", mock_context)

        assert "cancelled" in result.lower()


class TestGetArticleWithProgress:
    @patch("solution.advanced.wikipedia_server.wiki")
    @pytest.mark.asyncio
    async def test_get_article_with_progress_reports_progress(
        self, mock_wiki: MagicMock
    ) -> None:
        mock_page = MagicMock()
        mock_page.exists.return_value = True
        mock_page.text = "Short article content."
        mock_wiki.page.return_value = mock_page

        mock_context = AsyncMock(spec=Context)

        result = await wikipedia_server.get_article_with_progress.fn(
            mock_context, "Test Article", 2000
        )

        assert result == "Short article content."
        progress_calls = mock_context.report_progress.call_args_list
        assert len(progress_calls) >= 2
        final_call = progress_calls[-1]
        assert final_call[0] == (100, 100)

    @patch("solution.advanced.wikipedia_server.wiki")
    @pytest.mark.asyncio
    async def test_get_article_with_progress_truncates_long_content(
        self, mock_wiki: MagicMock
    ) -> None:
        long_content = "A" * 3000 + ". More content here."
        mock_page = MagicMock()
        mock_page.exists.return_value = True
        mock_page.text = long_content
        mock_wiki.page.return_value = mock_page

        mock_context = AsyncMock(spec=Context)

        result = await wikipedia_server.get_article_with_progress.fn(
            mock_context, "Test Article", 1000
        )

        assert len(result) <= 1030
        assert "[Content truncated...]" in result
        mock_context.info.assert_called()
