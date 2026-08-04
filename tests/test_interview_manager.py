from app.interview_manager import InterviewManager

def run_test():
    """Test the InterviewManager workflow."""
    manager = InterviewManager()
    
    # Start
    manager.start_interview("Alice Smith", "Python Developer", ["Python", "API"])
    print(f"\nStarted interview for {manager.candidate_name}")
    print(f"Generated {len(manager.questions)} questions.")
    
    # Submit 5 answers
    for i, q in enumerate(manager.questions):
        print(f"\nQuestion: {q}")
        manager.submit_answer(q, f"This is mock answer {i+1} for: {q}")
        print("Answer submitted.")
        
    # Generate
    print("\nGenerating report...")
    report = manager.generate_report()
    
    print("\n---------------------------------------")
    print("Interview Summary")
    print("---------------------------------------")
    print(f"Overall Score: {report['summary']['total_score']}")
    print(f"Recommendation: {report['overall_feedback']['recommendation']}")
    print(f"Transcript Path: {report['transcript_path']}")
    print(f"Database ID: {report['db_id']}")
    print("---------------------------------------\n")

if __name__ == "__main__":
    run_test()
