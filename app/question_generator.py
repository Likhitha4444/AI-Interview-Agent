import json
import logging
from typing import List
from app.gemini_client import generate_response
from app.prompts import build_question_generation_prompt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuestionGenerator:
    """Handles generation and validation of interview questions."""

    def generate_questions(self, role: str, skills: List[str]) -> List[str]:
        """
        Generates 5 role-specific interview questions using Gemini.
        """
        prompt = build_question_generation_prompt(role, skills)
        logger.info(f"Generated prompt for role: {role}")

        for attempt in range(2):
            try:
                logger.info(f"API call attempt {attempt + 1}...")
                raw_response = generate_response(prompt)
                
                # Clean response just in case of markdown formatting
                cleaned_response = raw_response.replace('```json', '').replace('```', '').strip()
                
                data = json.loads(cleaned_response)
                logger.info("JSON parsed successfully.")
                
                # Validation
                if "questions" not in data or not isinstance(data["questions"], list):
                    raise ValueError("Missing 'questions' key or not a list.")
                
                questions = data["questions"]
                
                if len(questions) != 5:
                    raise ValueError(f"Expected 5 questions, got {len(questions)}.")
                
                if not all(isinstance(q, str) and q.strip() for q in questions):
                    raise ValueError("Questions list must contain non-empty strings.")
                
                logger.info("Validation successful.")
                return questions

            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 1:
                    logger.error("Final attempt failed.")
                    raise RuntimeError(f"Failed to generate valid questions: {e}")
        
        return []
