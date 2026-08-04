from app.database import DatabaseManager

def run_test():
    """Test the DatabaseManager functionality."""
    db = DatabaseManager()
    
    # Mock data
    report = {
        "candidate_name": "John Doe",
        "role": "Data Scientist",
        "skills": ["Python", "ML"],
        "summary": {"total_score": 40, "average_score": 8.0, "percentage": 80.0},
        "overall_feedback": {"recommendation": "Recommended", "confidence": "High"},
        "questions": [
            {"question": "Q1", "answer": "A1", "score": 8, "strengths": ["S1"], "weaknesses": ["W1"], "ideal_answer": "IA1", "feedback": "F1"},
            {"question": "Q2", "answer": "A2", "score": 8, "strengths": ["S2"], "weaknesses": ["W2"], "ideal_answer": "IA2", "feedback": "F2"},
            {"question": "Q3", "answer": "A3", "score": 8, "strengths": ["S3"], "weaknesses": ["W3"], "ideal_answer": "IA3", "feedback": "F3"},
            {"question": "Q4", "answer": "A4", "score": 8, "strengths": ["S4"], "weaknesses": ["W4"], "ideal_answer": "IA4", "feedback": "F4"},
            {"question": "Q5", "answer": "A5", "score": 8, "strengths": ["S5"], "weaknesses": ["W5"], "ideal_answer": "IA5", "feedback": "F5"},
        ]
    }
    
    try:
        # Save
        print("Saving interview...")
        interview_id = db.save_interview(report)
        print(f"Saved interview ID: {interview_id}")
        
        # Retrieve
        print("\nRetrieving interview...")
        retrieved = db.get_interview(interview_id)
        print(f"Retrieved candidate: {retrieved['interview']['candidate_name']}")
        
        # List all
        print("\nListing all interviews:")
        all_interviews = db.get_all_interviews()
        for i in all_interviews:
            print(f"- ID: {i['id']}, Candidate: {i['candidate_name']}")
            
        # Delete
        print(f"\nDeleting interview {interview_id}...")
        db.delete_interview(interview_id)
        print("Success.")
            
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    run_test()
