from app.answer_evaluator import AnswerEvaluator

def run_test():
    """Test the AnswerEvaluator functionality."""
    role = input("Enter Role: ").strip()
    question = input("Enter Question: ").strip()
    answer = input("Enter Candidate Answer: ").strip()

    evaluator = AnswerEvaluator()
    
    try:
        print("\nEvaluating answer, please wait...\n")
        evaluation = evaluator.evaluate_answer(role, question, answer)
        
        print("\n---------------------------------------")
        print("Evaluation Results")
        print("---------------------------------------")
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        print(f"Score: {evaluation['score']}/10")
        print(f"Strengths: {', '.join(evaluation['strengths'])}")
        print(f"Weaknesses: {', '.join(evaluation['weaknesses'])}")
        print(f"Ideal Answer: {evaluation['ideal_answer']}")
        print(f"Feedback: {evaluation['feedback']}")
        print("---------------------------------------\n")
            
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    run_test()
