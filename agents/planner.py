"""
Planner Agent: Analyzes user input and creates a plan.
"""
import os
import json
import google.generativeai as genai
from project.core.context_engineering import PLANNER_PROMPT
from project.core.a2a_protocol import PlannerOutput
from project.core.observability import logger

class Planner:
    def __init__(self):
        self.mock_mode = os.environ.get("MOCK_MODE") == "True"
        if not self.mock_mode:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def plan(self, user_input, history_str):
        logger.log("Planner", "Analyzing input...")

        if self.mock_mode:
            # Simple keyword-based mock logic
            if "kill" in user_input.lower() or "die" in user_input.lower():
                 return PlannerOutput("crisis", "HIGH", "emergency_protocol", "Provide emergency disclaimer immediately.").to_dict()
            elif "anxious" in user_input or "stress" in user_input:
                 return PlannerOutput("anxiety", "LOW", "provide_grounding", "Guide user through box_breathing.").to_dict()
            else:
                 return PlannerOutput("neutral", "LOW", "chat", "Respond politely.").to_dict()

        # Real LLM Call
        prompt = f"{PLANNER_PROMPT}\n\nHISTORY:\n{history_str}\n\nCURRENT INPUT: {user_input}\n\nOUTPUT JSON:"
        try:
            response = self.model.generate_content(prompt)
            # Clean response to ensure valid JSON
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:-3]
            data = json.loads(text)
            return data
        except Exception as e:
            logger.log("Planner", f"Error: {e}")
            return PlannerOutput("error", "LOW", "chat", "Apologize and ask again.").to_dict()
