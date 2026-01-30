from unittest.mock import Mock, patch

import pytest

from llm_client import LLMClient


class TestLLMClient:

    def test_init_with_base_url(self):
        client = LLMClient(api_key="test_key", base_url="http://localhost:8080")
        assert hasattr(client.client, "chat")

    @pytest.fixture
    def mock_instructor_client(self):
        with patch("llm_client.OpenAI") as mock_openai:
            with patch("llm_client.instructor") as mock_instructor:
                mock_client = Mock()
                mock_instructor_client = Mock()

                # мокаем instructor
                mock_instructor.from_openai.return_value = mock_instructor_client
                mock_openai.return_value = mock_client

                yield mock_instructor_client

    @pytest.mark.parametrize(
        "html_input,expected_selectors",
        [
            (
                "<html>test</html>",
                {
                    "name": ".product-title",
                    "price": ".price",
                    "images": ".gallery img",
                    "description": ".desc",
                    "specifications": ".specs",
                    "availability": ".stock",
                },
            )
        ],
    )
    def test_call_llm_success(
        self, mock_instructor_client, html_input, expected_selectors
    ):
        mock_response = Mock()
        mock_response.model_dump.return_value = expected_selectors

        mock_instructor_client.chat.completions.create.return_value = mock_response

        client = LLMClient(api_key="test_key", base_url="https://api.deepseek.com")
        result = client.call_LLM(html_input, "analyze prompt")

        assert result == expected_selectors
