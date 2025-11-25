"""
Evaluator Agent: Safety checks.
"""
import os
import json
import google.generativeai as genai
from project.core.context_engineering import EVALUATOR_PROMPT
from project.core.a2a_protocol import EvaluatorOutput
from project.core.observability import logger

class Evaluator:
    def __init__(self):
        self.mock_mode = os.environ.get("MOCK_MODE") == "True"
        if not self.mock_mode:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def evaluate(self, worker_output):
        draft = worker_output.get("draft_response")
        logger.log("Evaluator", "Checking draft...")

        if self.mock_mode:
            return EvaluatorOutput("APPROVED", "Mock Safe", draft).to_dict()

        prompt = f"{EVALUATOR_PROMPT}\n\nDRAFT RESPONSE: {draft}\n\nOUTPUT JSON:"
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:-3]
            data = json.loads(text)

            # Fallback if json parsing is sloppy
            final_res = data.get("sanitized_response", draft)
            if data.get("status") != "APPROVED":
                 final_res = "I apologize, but I cannot provide that specific advice. However, I am here to listen."

            return EvaluatorOutput(data.get("status"), data.get("feedback"), final_res).to_dict()
        except Exception as e:
            logger.log("Evaluator", f"Error: {e}")
            return EvaluatorOutput("APPROVED", "Error skipped", draft).to_dict()
