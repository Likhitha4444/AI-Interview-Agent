from typing import List

def build_question_generation_prompt(role: str, skills: List[str]) -> str:
    """
    Constructs a prompt to generate 5 role-specific interview questions.
    """
    skills_str = ", ".join(skills)
    return f"""
Act as a Senior Technical Interviewer with 10+ years of experience.
Interview the candidate for the following role: {role}.
Use the following skills: {skills_str}.

Generate exactly 5 interview questions.
- Start with beginner-level questions.
- Gradually increase the difficulty.
- Include:
  - Core technical questions
  - Practical coding questions
  - Scenario-based questions
  - Problem-solving questions
- Avoid duplicate questions.
- Keep each question concise.

Return ONLY valid JSON in the following format:
{{
  "questions": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ]
}}
"""

def build_answer_evaluation_prompt(role: str, question: str, candidate_answer: str) -> str:
    """
    Constructs a prompt to evaluate a single candidate's answer.
    """
    return f"""
Act as an interviewer evaluating a candidate for the role: {role}.
Evaluate the candidate's answer to the following question: "{question}".
The candidate's answer is: "{candidate_answer}".

Evaluate based on:
- Technical correctness
- Completeness
- Clarity
- Practical understanding
- Communication quality

Return ONLY valid JSON in the following format:
{{
  "score": 0,
  "strengths": ["string", "string"],
  "weaknesses": ["string", "string"],
  "ideal_answer": "string",
  "feedback": "string"
}}

Rules:
- score must be an integer between 0 and 10.
"""

def build_final_summary_prompt(results_json: str) -> str:
    """
    Constructs a prompt to generate an overall interview summary based on results.
    """
    return f"""
Act as a hiring manager. Analyze the following interview results and generate a final hiring recommendation.

Results data:
{results_json}

Return ONLY valid JSON in the following format:
{{
  "overall_score": 0,
  "percentage": 0,
  "strengths": ["string", "string"],
  "areas_for_improvement": ["string", "string"],
  "recommendation": "Recommended" | "Consider" | "Not Recommended",
  "confidence": "High" | "Medium" | "Low",
  "final_feedback": "string",
  "hiring_decision": "Strong Hire" | "Hire" | "Hold" | "Reject",
  "fit_score": 0-100,
  "salary_recommendation": "Fresher" | "Junior" | "Mid-Level",
  "final_notes": "string"
}}
"""
