import sys, os
# Ensure the root project directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project.main_agent import run_agent

if __name__ == "__main__":
    print("--- Running Demo ---")
    response = run_agent("Hello! This is a demo.")
    print(f"Response: {response}")
