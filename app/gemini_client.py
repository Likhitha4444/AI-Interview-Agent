import logging
from google import genai
from google.genai import errors
from app.config import get_api_key
from app.exceptions import GeminiError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the Gemini client
try:
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    # Using the requested model
    MODEL_NAME = 'gemini-2.5-flash'
    logger.info(f"Gemini client initialized with model: {MODEL_NAME}")
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    raise

def generate_response(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the generated text.

    Args:
        prompt (str): The text prompt to send.

    Returns:
        str: The generated response.

    Raises:
        GeminiError: For quota or general API errors.
    """
    try:
        logger.info("Sending prompt to Gemini...")
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        
        if not response.text:
            raise ValueError("Received an empty response from Gemini.")
            
        return response.text
    except errors.ClientError as e:
        logger.error(f"Gemini API Client error: {e}")
        if e.code == 429:
            raise GeminiError("RESOURCE_EXHAUSTED")
        raise GeminiError(f"API Client error: {e.message}")
    except Exception as e:
        logger.error(f"General error communicating with Gemini: {e}")
        raise GeminiError(f"Unexpected error: {str(e)}")
