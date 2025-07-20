import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from genAI import app, get_context_from_weaviate, get_page_content, AI_BACKEND

client = TestClient(app)

class TestGenAIApi(unittest.TestCase):
    
    @patch("genAI.requests.get")
    @patch("genAI.get_weaviate_collection")
    def test_update_weaviate_success(self, mock_get_collection, mock_requests_get):
        mock_collection = MagicMock()
        mock_get_collection.return_value = mock_collection

        mock_requests_get.return_value = MagicMock(
            status_code=200,
            json=lambda: [
                {"title": "T1", "content": "C1", "pageId": 1},
                {"title": "T2", "content": "C2", "pageId": 2}
            ]
        )

        response = client.post("/update_weaviate")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "Weaviate updated with wiki pages"})
        self.assertEqual(mock_collection.data.insert.call_count, 2)

    @patch("genAI.get_weaviate_collection")
    def test_get_context_from_weaviate(self, mock_get_collection):
        mock_obj = MagicMock()
        mock_obj.properties = {"title": "Test", "content": "Sample", "pageId": 42}
        mock_get_collection.return_value.query.near_text.return_value.objects = [mock_obj]

        context = get_context_from_weaviate("sample query")
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0]["pageId"], 42)

    @patch("genAI.requests.get")
    def test_get_page_content_success(self, mock_requests_get):
        mock_requests_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"title": "Intro", "content": "Content here"}
        )
        result = get_page_content(1)
        self.assertIn("Intro", result)
        self.assertIn("Content here", result)

    @patch("genAI.requests.get")
    def test_get_page_content_failure(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 404
        result = get_page_content(999)
        self.assertEqual(result, "")

    def test_set_backend_valid_mode(self):
        response = client.post("/set_backend", json={"mode": "cloud"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "AI backend set to cloud")
        self.assertEqual(AI_BACKEND["mode"], "cloud")

    def test_set_backend_invalid_mode(self):
        response = client.post("/set_backend", json={"mode": "invalid"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid mode", response.text)

    def test_get_backend(self):
        AI_BACKEND["mode"] = "cloud"
        response = client.get("/get_backend")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"mode": "cloud"})

    @patch("genAI.get_page_content")
    @patch("genAI.get_context_from_weaviate")
    @patch("genAI.requests.post")
    def test_chat_cloud_mode(self, mock_post, mock_get_context, mock_get_page_content):
        AI_BACKEND["mode"] = "cloud"

        mock_get_context.return_value = [{"title": "T", "content": "C", "pageId": 1}]
        mock_get_page_content.return_value = "Page Content"

        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "choices": [{"message": {"content": "AI response"}}]
            }
        )

        response = client.post("/chat", json={"prompt": "Hello", "page_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("AI response", response.text)

if __name__ == "__main__":
    unittest.main()