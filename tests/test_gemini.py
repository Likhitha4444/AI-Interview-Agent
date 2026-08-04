import logging
from app.gemini_client import generate_response

# Configure basic logging for the test script
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_test():
    """Test the Gemini client connection."""
    prompt = "Hello, introduce yourself in one sentence."
    logger.info(f"Test Prompt: {prompt}")
    
    try:
        response = generate_response(prompt)
        print("\n--- Gemini Response ---")
        print(response)
        print("-----------------------\n")
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    run_test()
