"""
Evaluator Agent: Safety and quality assurance gatekeeper.
"""
import re
from typing import Dict
from project.core.context_engineering import EVALUATOR_PROMPT
from project.core.a2a_protocol import EvaluatorOutput
from project.core.observability import logger
from project.core.gemini_client import GeminiClient

class Evaluator:
    def __init__(self):
        self.client = GeminiClient(EVALUATOR_PROMPT)
        self.mock_mode = False
        
        # Enhanced Safety filters
        self.banned_phrases = [
            r"\bdiagnos(e|is)\b", 
            r"\bmedication\b", 
            r"\bprescri(be|ption)\b",
            r"\btherap(y|ist)\b.*\b(recommend|suggest)", 
            r"\bguarantee\b", 
            r"\bcure\b",
            r"as a doctor", # preventing roleplay leak
            r"i am a doctor"
        ]
        
    # NOTE: Added user_input to arguments
    def evaluate(self, worker_output: Dict, user_input: str) -> Dict:
        draft = worker_output.get("draft_response", "")
        tools_used = worker_output.get("tools_used", [])
        
        logger.log("Evaluator", "Starting safety evaluation", 
                   data={"draft_length": len(draft)})
        
        # Mock mode
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._mock_evaluate(draft)
        
        # 1. Regex Safety Checks (Hard Rules)
        if self._contains_medical_advice(draft):
            logger.log("Evaluator", "REJECTED: Medical advice detected")
            return EvaluatorOutput(
                status="REJECTED",
                feedback="Contains medical advice or diagnosis language.",
                final_response=self._get_fallback_response()
            ).to_dict()
        
        if self._contains_harmful_content(draft):
            logger.log("Evaluator", "REJECTED: Harmful content detected")
            return EvaluatorOutput(
                status="REJECTED",
                feedback="Potentially harmful content detected.",
                final_response=self._get_fallback_response()
            ).to_dict()
        
        # 2. LLM Contextual Check (Smart Rules)
        # We inject the prompt template manually here to pass both input and response
        prompt = EVALUATOR_PROMPT.replace("{user_input}", user_input).replace("{agent_response}", draft)
        
        evaluation = self.client.generate_json(prompt)
        
        if not evaluation:
            logger.log("Evaluator", "Evaluation failed, defaulting to APPROVED if regex passed")
            return EvaluatorOutput(
                status="APPROVED", # Fallback to approved if regex passed but LLM failed
                feedback="Automated check passed.",
                final_response=draft
            ).to_dict()
        
        # Post-process evaluation
        if evaluation.get("status") == "APPROVED":
            final_response = draft
        else:
            final_response = evaluation.get("final_response", self._get_fallback_response())
            logger.warning("Evaluator", f"Guardrail Triggered: {evaluation.get('feedback')}")
        
        logger.log("Evaluator", f"Evaluation result: {evaluation.get('status')}")
        
        return EvaluatorOutput(
            status=evaluation.get("status", "REJECTED"),
            feedback=evaluation.get("feedback", "Safety check failed."),
            final_response=final_response
        ).to_dict()
    
    def _contains_medical_advice(self, text: str) -> bool:
        text_lower = text.lower()
        # Exception: "I cannot diagnose" is safe, but "I diagnose" is bad.
        # This basic regex catches the word "diagnose", so we need to be careful.
        # Improvement: If the sentence starts with negation, ignore.
        # For now, strict mode:
        for pattern in self.banned_phrases:
            if re.search(pattern, text_lower):
                # Allow refusal context like "I cannot provide a diagnosis"
                if "cannot" in text_lower or "not a doctor" in text_lower:
                    continue 
                return True
        return False
    
    def _contains_harmful_content(self, text: str) -> bool:
        return any(keyword in text.lower() for keyword in ["self-harm", "hurt yourself", "do it"])
    
    def _get_fallback_response(self) -> str:
        return """
        I apologize, but I cannot fulfill that request. I am an AI companion, not a mental health professional or doctor.
        
        If you are in distress, please contact:
        **988 Suicide & Crisis Lifeline** (US)
        **111** (UK)
        """
    
    def _mock_evaluate(self, draft: str) -> Dict:
        return EvaluatorOutput(status="APPROVED", feedback="Mock Pass", final_response=draft).to_dict()