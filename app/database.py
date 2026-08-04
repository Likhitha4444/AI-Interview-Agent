import sqlite3
import json
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'database/interview_agent.db'

class DatabaseManager:
    """Handles SQLite database operations for interview data."""

    def __init__(self):
        self.initialize_database()

    def _get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_database(self):
        """Creates tables if they do not exist."""
        logger.info(f"Initializing database at {DB_PATH}...")
        with self._get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            # Drop to recreate with new schema
            conn.execute("DROP TABLE IF EXISTS interviews")
            conn.execute("""
                CREATE TABLE interviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    skills TEXT NOT NULL,
                    total_score REAL,
                    average_score REAL,
                    percentage REAL,
                    recommendation TEXT,
                    confidence TEXT,
                    hiring_decision TEXT,
                    fit_score INTEGER,
                    salary_recommendation TEXT,
                    final_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interview_id INTEGER,
                    question TEXT,
                    candidate_answer TEXT,
                    score REAL,
                    strengths TEXT,
                    weaknesses TEXT,
                    ideal_answer TEXT,
                    feedback TEXT,
                    FOREIGN KEY(interview_id) REFERENCES interviews(id) ON DELETE CASCADE
                )
            """)
        logger.info("Database tables initialized.")

    def save_interview(self, report: Dict[str, Any]) -> int:
        """Saves a complete interview report."""
        if len(report.get("questions", [])) != 5:
            raise ValueError("Exactly five questions are required.")

        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO interviews (candidate_name, role, skills, total_score, average_score, percentage, recommendation, confidence, hiring_decision, fit_score, salary_recommendation, final_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                report["candidate_name"],
                report["role"],
                ",".join(report["skills"]),
                report["summary"]["total_score"],
                report["summary"]["average_score"],
                report["summary"]["percentage"],
                report["overall_feedback"]["recommendation"],
                report["overall_feedback"]["confidence"],
                report["overall_feedback"]["hiring_decision"],
                report["overall_feedback"]["fit_score"],
                report["overall_feedback"]["salary_recommendation"],
                report["overall_feedback"]["final_notes"]
            ))
            interview_id = cursor.lastrowid

            for q in report["questions"]:
                conn.execute("""
                    INSERT INTO interview_questions (interview_id, question, candidate_answer, score, strengths, weaknesses, ideal_answer, feedback)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    interview_id,
                    q["question"],
                    q["answer"],
                    q["score"],
                    json.dumps(q["strengths"]),
                    json.dumps(q["weaknesses"]),
                    q["ideal_answer"],
                    q["feedback"]
                ))
        
        logger.info(f"Interview {interview_id} saved.")
        return interview_id

    def get_interview(self, interview_id: int) -> Dict[str, Any]:
        """Retrieves a complete interview report."""
        with self._get_connection() as conn:
            interview = conn.execute("SELECT * FROM interviews WHERE id = ?", (interview_id,)).fetchone()
            if not interview:
                return None
            
            questions = conn.execute("SELECT * FROM interview_questions WHERE interview_id = ?", (interview_id,)).fetchall()
            
            return {
                "interview": dict(interview),
                "questions": [dict(q) for q in questions]
            }

    def get_all_interviews(self) -> List[Dict[str, Any]]:
        """Retrieves list of all interviews."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT id, candidate_name, role, percentage, recommendation, created_at FROM interviews ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in rows]

    def delete_interview(self, interview_id: int):
        """Deletes an interview."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM interviews WHERE id = ?", (interview_id,))
        logger.info(f"Interview {interview_id} deleted.")
