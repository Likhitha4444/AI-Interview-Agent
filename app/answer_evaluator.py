import json
import logging
import re
from typing import Dict, Any, List
from app.gemini_client import generate_response
from app.prompts import build_answer_evaluation_prompt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnswerEvaluator:
    """Handles evaluation of candidate answers using Gemini with robust parsing."""

    def _clean_response(self, raw_response: str) -> str:
        """Strips markdown and attempts to isolate the JSON block."""
        # Remove markdown code blocks
        cleaned = re.sub(r"```json\s*", "", raw_response)
        cleaned = re.sub(r"```\s*", "", cleaned)
        
        # Try to find the first '{' and last '}'
        start = cleaned.find('{')
        end = cleaned.rfind('}')
        if start != -1 and end != -1:
            cleaned = cleaned[start:end+1]
        
        return cleaned.strip()

    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coerces types and handles common LLM formatting issues, providing defaults."""
        
        # Defaults
        defaults = {
            "strengths": ["Shows basic understanding."],
            "weaknesses": ["Can improve answer depth."],
            "feedback": "No detailed feedback generated.",
            "ideal_answer": "Ideal answer unavailable."
        }
        
        # Ensure lists
        for field in ["strengths", "weaknesses"]:
            if field not in data or not isinstance(data[field], list) or len(data[field]) == 0:
                data[field] = defaults[field]
            else:
                # Ensure all items are strings and remove empty strings
                data[field] = [str(item) for item in data[field] if item]
                if not data[field]:
                    data[field] = defaults[field]

        # Ensure strings
        for field in ["ideal_answer", "feedback"]:
            if field not in data or not isinstance(data[field], str) or not data[field].strip():
                data[field] = defaults[field]

        # Ensure score
        if "score" not in data:
            data["score"] = 5 # Default neutral score
        else:
            try:
                data["score"] = int(data["score"])
                data["score"] = max(0, min(10, data["score"]))
            except (ValueError, TypeError):
                data["score"] = 5
                
        return data

    def evaluate_answer(self, role: str, question: str, candidate_answer: str) -> Dict[str, Any]:
        """Evaluates a candidate's answer with improved resilience."""
        prompt = build_answer_evaluation_prompt(role, question, candidate_answer)
        logger.info("Prompt generated for answer evaluation.")

        for attempt in range(2):
            try:
                logger.info(f"Gemini evaluation request started (attempt {attempt + 1})...")
                raw_response = generate_response(prompt)
                
                cleaned_response = self._clean_response(raw_response)
                data = json.loads(cleaned_response)
                
                # Sanitize and coerce types
                data = self._sanitize_data(data)
                
                logger.info("JSON parsed and sanitized.")
                return data

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 1:
                    logger.error("Final attempt failed.")
                    raise RuntimeError(f"Failed to evaluate answer: {e}")
                logger.info("Retrying...")
        
        return {}
