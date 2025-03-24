from django.test import TestCase
from unittest.mock import patch, Mock
from books.api.v1.utils import generate_summary
import requests

class GenerateSummaryTest(TestCase):
    """Test cases for the generate_summary utility function."""

    def setUp(self):
        """Set up test data for summary generation."""
        self.test_text = "This is a test description for summary generation."
        self.mock_summary = "This is a test summary."

    @patch('books.api.v1.utils.requests.get')
    @patch('books.api.v1.utils.requests.post')
    def test_successful_summary_generation(self, mock_post, mock_get):
        """Test successful generation of a summary when the API is working correctly."""
        # Mock successful health check
        mock_health = Mock()
        mock_health.status_code = 200
        mock_get.return_value = mock_health

        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": self.mock_summary}
        mock_post.return_value = mock_response

        summary = generate_summary(self.test_text)
        self.assertEqual(summary, self.mock_summary)

    @patch('books.api.v1.utils.requests.get')
    def test_health_check_failure(self, mock_get):
        """Test handling of Ollama service being unavailable."""
        # Mock failed health check
        mock_get.side_effect = requests.exceptions.ConnectionError("Service unavailable")
        
        summary = generate_summary(self.test_text)
        self.assertEqual(summary, "Failed to connect to Ollama service. Please ensure the service is running.")

    @patch('books.api.v1.utils.requests.get')
    @patch('books.api.v1.utils.requests.post')
    def test_timeout_handling(self, mock_post, mock_get):
        """Test handling of API request timeout."""
        # Mock successful health check
        mock_health = Mock()
        mock_health.status_code = 200
        mock_get.return_value = mock_health

        # Mock timeout error
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        summary = generate_summary(self.test_text)
        self.assertEqual(summary, "Request timed out. The service might be overloaded.")

    @patch('books.api.v1.utils.requests.get')
    @patch('books.api.v1.utils.requests.post')
    def test_empty_response_handling(self, mock_post, mock_get):
        """Test handling of empty response from the API."""
        # Mock successful health check
        mock_health = Mock()
        mock_health.status_code = 200
        mock_get.return_value = mock_health

        # Mock empty API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        summary = generate_summary(self.test_text)
        self.assertEqual(summary, "No summary available.")

    @patch('books.api.v1.utils.requests.get')
    @patch('books.api.v1.utils.requests.post')
    def test_request_parameters(self, mock_post, mock_get):
        """Test that correct parameters are sent to the Ollama API."""
        # Mock successful health check
        mock_health = Mock()
        mock_health.status_code = 200
        mock_get.return_value = mock_health

        # Mock response to check request parameters
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": self.mock_summary}
        mock_post.return_value = mock_response

        generate_summary(self.test_text)

        # Verify the API call parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Check URL
        self.assertTrue(args[0].endswith('/api/generate'))
        
        # Check request parameters
        self.assertEqual(kwargs['json']['model'], 'mistral')
        self.assertTrue(self.test_text in kwargs['json']['prompt'])
        self.assertEqual(kwargs['json']['stream'], False)
        self.assertEqual(kwargs['timeout'], 120)  # Updated timeout value
