from app.question_generator import QuestionGenerator

def run_test():
    """Test the QuestionGenerator functionality."""
    role = input("Enter Candidate Role: ").strip()
    skills_input = input("Enter Skills (comma separated): ").strip()
    skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    generator = QuestionGenerator()
    
    try:
        print("\nGenerating questions, please wait...\n")
        questions = generator.generate_questions(role, skills)
        
        print("\n------------------------------------")
        print("Interview Questions")
        print("------------------------------------\n")
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    run_test()
