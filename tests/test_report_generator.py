from app.report_generator import ReportGenerator

def run_test():
    """Test the ReportGenerator functionality."""
    generator = ReportGenerator()
    
    # Mock data
    candidate = "Jane Doe"
    role = "Software Engineer"
    skills = ["Python", "Algorithms"]
    questions = [f"Question {i}" for i in range(1, 6)]
    answers = [f"Answer {i}" for i in range(1, 6)]
    evaluations = [
        {"score": 9, "strengths": ["Clear"], "weaknesses": ["Brief"], "ideal_answer": "...", "feedback": "..."},
        {"score": 7, "strengths": ["Good"], "weaknesses": ["Slow"], "ideal_answer": "...", "feedback": "..."},
        {"score": 6, "strengths": ["Okay"], "weaknesses": ["Confused"], "ideal_answer": "...", "feedback": "..."},
        {"score": 8, "strengths": ["Strong"], "weaknesses": ["None"], "ideal_answer": "...", "feedback": "..."},
        {"score": 9, "strengths": ["Expert"], "weaknesses": ["None"], "ideal_answer": "...", "feedback": "..."},
    ]
    
    try:
        report = generator.generate_complete_report(candidate, role, skills, questions, answers, evaluations)
        
        print("\n---------------------------------------")
        print("Final Interview Report")
        print("---------------------------------------")
        print(f"Candidate: {report['candidate_name']}")
        print(f"Role: {report['role']}")
        print(f"Overall Score: {report['summary']['total_score']}")
        print(f"Average Score: {report['summary']['average_score']}")
        print(f"Percentage: {report['summary']['percentage']}%")
        print(f"Recommendation: {report['overall_feedback']['recommendation']}")
        print(f"Confidence: {report['overall_feedback']['confidence']}")
        print(f"Strengths: {', '.join(report['overall_feedback']['strengths'])}")
        print(f"Areas for Improvement: {', '.join(report['overall_feedback']['areas_for_improvement'])}")
        print(f"Final Feedback: {report['overall_feedback']['final_feedback']}")
        print("---------------------------------------\n")
            
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    run_test()
