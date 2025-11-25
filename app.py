"""
Basic entry point for an application wrapper.
"""
from project.main_agent import run_agent

def main():
    print("--- Mental Health Companion (Console App) ---")
    print("Type 'quit' to exit.")

    while True:
        user_in = input("You: ")
        if user_in.lower() in ["quit", "exit"]:
            break

        response = run_agent(user_in)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()
