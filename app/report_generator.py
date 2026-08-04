import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from app.gemini_client import generate_response
from app.prompts import build_final_summary_prompt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReportGenerator:
    """Handles generation of final interview reports."""

    def calculate_summary(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates statistics based on evaluations."""
        logger.info("Calculating summary metrics...")
        
        scores = [e["score"] for e in evaluations]
        total_score = sum(scores)
        average_score = total_score / len(scores)
        percentage = (average_score / 10) * 100
        
        excellent = sum(1 for s in scores if s >= 8)
        average = sum(1 for s in scores if 5 <= s < 8)
        poor = sum(1 for s in scores if s < 5)
        
        return {
            "total_score": total_score,
            "average_score": round(average_score, 2),
            "percentage": round(percentage, 2),
            "excellent_answers": excellent,
            "average_answers": average,
            "poor_answers": poor
        }

    def generate_ai_summary(self, role: str, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates AI-based summary feedback."""
        logger.info("Generating AI summary request...")
        
        # Prepare evaluations for the prompt
        results_str = json.dumps(evaluations)
        prompt = build_final_summary_prompt(results_str)
        
        for attempt in range(2):
            try:
                raw_response = generate_response(prompt)
                cleaned_response = raw_response.replace('```json', '').replace('```', '').strip()
                
                data = json.loads(cleaned_response)
                
                # Validation of required fields
                required = [
                    "strengths", "areas_for_improvement", "recommendation", 
                    "confidence", "final_feedback", "hiring_decision", 
                    "fit_score", "salary_recommendation", "final_notes"
                ]
                if not all(k in data for k in required):
                    raise ValueError(f"Missing required fields: {[k for k in required if k not in data]}")
                
                logger.info("AI summary JSON parsed and validated.")
                return data
            except Exception as e:
                logger.warning(f"AI summary attempt {attempt + 1} failed: {e}")
                if attempt == 1:
                    logger.error("Final AI summary attempt failed.")
                    raise RuntimeError(f"Failed to generate AI summary: {e}")
        return {}

    def generate_complete_report(
        self,
        candidate_name: str,
        role: str,
        skills: List[str],
        questions: List[str],
        answers: List[str],
        evaluations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assembles the final comprehensive report."""
        
        # Validation
        if len(questions) != 5 or len(answers) != 5 or len(evaluations) != 5:
            raise ValueError("Exactly five questions, answers, and evaluations are required.")
            
        logger.info("Starting report creation...")
        
        summary = self.calculate_summary(evaluations)
        ai_summary = self.generate_ai_summary(role, evaluations)
        
        detailed_evaluations = []
        for i in range(5):
            detailed_evaluations.append({
                "question": questions[i],
                "answer": answers[i],
                **evaluations[i]
            })
            
        report = {
            "candidate_name": candidate_name,
            "role": role,
            "skills": skills,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": summary,
            "questions": detailed_evaluations,
            "overall_feedback": ai_summary
        }
        
        logger.info("Report creation completed.")
        return report
