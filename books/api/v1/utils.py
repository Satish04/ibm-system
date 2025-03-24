import requests
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

OLLAMA_API_URL = "http://ollama:11434"
logger = logging.getLogger(__name__)

# Configure retry strategy
retry_strategy = Retry(
    total=3,  # number of retries
    backoff_factor=1,  # wait 1, 2, 4 seconds between retries
    status_forcelist=[500, 502, 503, 504]  # HTTP status codes to retry on
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("http://", adapter)
http.mount("https://", adapter)

def generate_summary(text):
    """Generate a summary using Ollama API."""
    try:
        # First, check if Ollama service is available
        max_health_retries = 3
        health_check_timeout = 30  # increased from 10 to 30 seconds
        
        for attempt in range(max_health_retries):
            try:
                health_check = http.get(f"{OLLAMA_API_URL}/api/tags", timeout=health_check_timeout)
                if health_check.status_code == 200:
                    logger.info("Ollama service is healthy")
                    break
            except requests.exceptions.RequestException as e:
                if attempt == max_health_retries - 1:
                    logger.error(f"Health check failed after {max_health_retries} attempts: {e}")
                    return "Failed to connect to Ollama service. Please try again in a few moments."
                logger.warning(f"Health check attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)  # exponential backoff

        # Generate summary using Ollama
        response = http.post(
            f"{OLLAMA_API_URL}/api/generate",
            json={
                "model": "mistral",
                "prompt": f"Please provide a concise summary of the following text:\n\n{text}",
                "stream": False,
                "temperature": 0.7,  # Add some temperature for more natural responses
                "max_tokens": 150  # Limit response length for faster generation
            },
            timeout=180  # 3 minutes should be enough with max_tokens limit
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
        return "Request timed out. Please try again with a shorter text or contact support if the issue persists."
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return "An error occurred while generating the summary. Please try again later."
