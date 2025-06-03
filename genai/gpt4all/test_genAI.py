import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from genai.gpt4all.genAI import app, get_context_from_weaviate


class TestGenAI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("genai.gpt4all.genAI.weaviate_client")
    @patch("genai.gpt4all.genAI.requests")
    def test_update_weaviate(self, mock_requests, mock_weaviate_client):
        # Mock backend response
        mock_resp = MagicMock()
        mock_resp.json.return_value = [
            {"title": "T1", "content": "C1", "pageId": 1},
            {"title": "T2", "content": "C2", "pageId": 2}
        ]
        mock_resp.raise_for_status.return_value = None
        mock_requests.get.return_value = mock_resp

        # Mock data_object.create
        mock_weaviate_client.data_object.create = MagicMock()

        response = self.client.post("/update_weaviate")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "Weaviate updated with wiki pages"})
        self.assertEqual(mock_weaviate_client.data_object.create.call_count, 2)
        mock_weaviate_client.data_object.create.assert_any_call(
            {"title": "T1", "content": "C1", "page_id": 1}, class_name="WikiPage"
        )
        mock_weaviate_client.data_object.create.assert_any_call(
            {"title": "T2", "content": "C2", "page_id": 2}, class_name="WikiPage"
        )

    @patch("genai.gpt4all.genAI.weaviate_client")
    def test_get_context_from_weaviate(self, mock_weaviate_client):
        # Mock the chained query
        mock_do = MagicMock(return_value={
            "data": {
                "Get": {
                    "WikiPage": [
                        {"title": "T1", "content": "C1"},
                        {"title": "T2", "content": "C2"}
                    ]
                }
            }
        })
        mock_query = MagicMock()
        mock_query.get.return_value.with_near_text.return_value.with_limit.return_value.do = mock_do
        mock_weaviate_client.query = mock_query

        context = get_context_from_weaviate("test")
        self.assertIn("T1: C1", context)
        self.assertIn("T2: C2", context)

    @patch("genai.gpt4all.genAI.model")
    @patch("genai.gpt4all.genAI.get_context_from_weaviate")
    def test_chat_endpoint(self, mock_get_context, mock_model):
        mock_get_context.return_value = "T1: C1\n"
        mock_session = MagicMock()
        mock_model.chat_session.return_value.__enter__.return_value = mock_session
        mock_model.generate.return_value = "Fake response"

        response = self.client.post("/chat", json={"prompt": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Fake response"})

if __name__ == "__main__":
    unittest.main()