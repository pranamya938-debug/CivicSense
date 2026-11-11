import sys
from pathlib import Path

# Ensure src is in python path
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from predict import CivicSensePredictor

def main():
    print("==================================================")
    print("      CIVICSENSE – AI/ML DEMO INTERFACE           ")
    print("      Member 1: AI/ML/NLP Component               ")
    print("==================================================")
    print()

    # Initialize predictor
    predictor = CivicSensePredictor()

    while True:
        try:
            user_input = input("Enter citizen complaint text (or type 'exit' to quit): ").strip()
            
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("\nExiting CivicSense Demo. Good luck with your presentation!")
                break

            # Get prediction and routing result
            result = predictor.predict_complaint_text(user_input)

            print("\n--- PREDICTION & ROUTING RESULT ---")
            print(f"  • Complaint Text    : {result['complaint_text']}")
            print(f"  • Predicted Category: {result['predicted_category']}")
            print(f"  • Sub-Category      : {result['predicted_sub_category']}")
            print(f"  • Routing Department: {result['department']}")
            print(f"  • Mapping Status    : {result['mapping_status']}")
            print(f"  • Confidence Score  : {result['confidence']}")
            print(f"  • Model Version     : {result['model_version']}")
            print("-" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\nExiting demo. Have a great presentation!")
            break
        except Exception as e:
            print(f"\n[Error] An error occurred during prediction: {e}\n")

if __name__ == "__main__":
    main()