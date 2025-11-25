"""
Main Agent: Orchestrator.
"""
from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator
from project.memory.session_memory import SessionMemory
from project.core.observability import logger

class MainAgent:
    def __init__(self):
        self.planner = Planner()
        self.worker = Worker()
        self.evaluator = Evaluator()
        self.memory = SessionMemory()

    def handle_message(self, user_input):
        logger.log("System", f"User Input: {user_input}")

        # 1. Update Memory
        self.memory.add_message("user", user_input)
        history_str = self.memory.get_history_string()

        # 2. Planner
        plan = self.planner.plan(user_input, history_str)

        # 3. Worker
        worker_res = self.worker.work(plan)

        # 4. Evaluator
        eval_res = self.evaluator.evaluate(worker_res)

        final_response = eval_res.get("final_response")

        # 5. Update Memory
        self.memory.add_message("assistant", final_response)

        return {
            "response": final_response,
            "plan": plan,
            "logs": logger.get_logs()
        }

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
