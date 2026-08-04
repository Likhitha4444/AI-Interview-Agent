import logging
import time
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from app.question_generator import QuestionGenerator
from app.answer_evaluator import AnswerEvaluator
from app.report_generator import ReportGenerator
from app.database import DatabaseManager
from app.exceptions import ValidationError, InterviewError
from app.constants import TRANSCRIPT_FOLDER, MODEL_NAME

logger = logging.getLogger(__name__)

class InterviewManager:
    """Orchestrates the entire AI interview workflow."""

    def __init__(self):
        self.question_gen = QuestionGenerator()
        self.evaluator = AnswerEvaluator()
        self.report_gen = ReportGenerator()
        self.db = DatabaseManager()
        
        self.candidate_name = None
        self.role = None
        self.skills = []
        self.questions = []
        self.answers = []
        self.evaluations = []
        self.is_started = False
        self.is_completed = False
        self.is_report_generated = False
        self.start_time = None
        self.processing_times = {"generation": 0, "evaluation": 0, "total": 0}

    def start_interview(self, candidate_name: str, role: str, skills: List[str]):
        if self.is_started:
            raise InterviewError("Interview already started.")
        
        self.candidate_name = candidate_name
        self.role = role
        self.skills = skills
        self.is_started = True
        self.start_time = time.time()
        
        logger.info(f"Interview Started for {candidate_name} as {role}.")
        
        start_gen = time.time()
        self.questions = self.question_gen.generate_questions(role, skills)
        self.processing_times["generation"] = time.time() - start_gen
        
        logger.info("Questions Generated.")

    def submit_answer(self, question: str, answer: str):
        if not self.is_started:
            raise InterviewError("Interview not started.")
        if self.is_completed:
            raise InterviewError("Interview already completed.")
        if len(self.answers) >= 5:
            raise ValidationError("All five answers already submitted.")
            
        self.answers.append(answer)
        logger.info(f"Answer Submitted for question: {question}")
        if len(self.answers) == 5:
            self.is_completed = True

    def generate_report(self) -> Dict[str, Any]:
        if not self.is_completed:
            raise InterviewError("Interview not completed.")
        if self.is_report_generated:
            raise InterviewError("Report already generated.")
        
        start_eval = time.time()
        # Evaluate
        logger.info("Starting evaluation...")
        for i in range(5):
            eval_result = self.evaluator.evaluate_answer(self.role, self.questions[i], self.answers[i])
            self.evaluations.append(eval_result)
        self.processing_times["evaluation"] = time.time() - start_eval
        
        self.processing_times["total"] = time.time() - self.start_time
        logger.info("Evaluation Completed.")
        
        # Generate report
        report = self.report_gen.generate_complete_report(
            self.candidate_name, self.role, self.skills, self.questions, self.answers, self.evaluations
        )
        report["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "processing_times": self.processing_times,
            "model": MODEL_NAME,
            "version": "1.0"
        }
        
        self.is_report_generated = True
        
        # Save to DB
        db_id = self.db.save_interview(report)
        report["db_id"] = db_id
        
        # Save transcript
        transcript_path = self._save_transcript(report)
        report["transcript_path"] = transcript_path
        
        return report

    def _save_transcript(self, report: Dict[str, Any]) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.candidate_name.replace(' ', '_')}_{timestamp}.json"
        path = os.path.join(TRANSCRIPT_FOLDER, filename)
        
        os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        return path
