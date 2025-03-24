import requests
import logging

OLLAMA_API_URL = "http://ollama:11434"
logger = logging.getLogger(__name__)

def generate_summary(text):
    """Generate a summary using Ollama API."""
    try:
        # First, check if Ollama service is available
        health_check = requests.get(f"{OLLAMA_API_URL}/api/generate", timeout=10)
        health_check.raise_for_status()
        logger.info("Ollama service is healthy")

        # Generate summary using Ollama
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json={
                "model": "mistral",
                "prompt": f"Please provide a concise summary of the following text:\n\n{text}",
                "stream": False
            },
            timeout=120  # Changed from 300 to 120 seconds
        )
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully generated summary")
        return result.get("response", "No summary available.")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return "Failed to connect to Ollama service. Please ensure the service is running."
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error: {e}")
        return "Request timed out. The service might be overloaded."
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return f"Failed to generate summary: {e}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {e}"
