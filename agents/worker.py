"""
Worker Agent: Executes the plan and generates content.
"""
import os
import google.generativeai as genai
from project.core.context_engineering import WORKER_PROMPT
from project.core.a2a_protocol import WorkerOutput
from project.tools.tools import Tools
from project.core.observability import logger

class Worker:
    def __init__(self):
        self.mock_mode = os.environ.get("MOCK_MODE") == "True"
        if not self.mock_mode:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def work(self, planner_output):
        logger.log("Worker", f"Executing instruction: {planner_output.get('instruction')}")

        instruction = planner_output.get("instruction", "")
        action = planner_output.get("action", "")

        # Tool Usage
        context_data = ""
        tools_used = []

        if action == "provide_grounding":
            # Simple keyword matching to pick tool
            if "box" in instruction.lower():
                context_data = Tools.get_grounding_technique("box_breathing")
                tools_used.append("box_breathing")
            else:
                context_data = Tools.get_grounding_technique("54321_grounding")
                tools_used.append("54321_grounding")
        elif action == "provide_resources":
            context_data = str(Tools.get_helpline("Global"))
            tools_used.append("helpline_search")

        if self.mock_mode:
             draft = f"[Mock Worker] Based on {action}: {instruction}. Data: {context_data}"
             return WorkerOutput(draft, tools_used).to_dict()

        # Real LLM Generation
        prompt = f"{WORKER_PROMPT}\n\nINSTRUCTION: {instruction}\nCONTEXT DATA: {context_data}\n\nDRAFT RESPONSE:"
        response = self.model.generate_content(prompt)
        return WorkerOutput(response.text, tools_used).to_dict()
