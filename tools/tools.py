"""
Provides data retrieval tools for the Worker agent.
"""
import json

# Static Data (Simulating JSON file load for simplicity)
HELPLINES = {
    "US": {"name": "988 Suicide & Crisis Lifeline", "number": "988"},
    "UK": {"name": "NHS 111", "number": "111"},
    "IN": {"name": "Kiran Mental Health Helpline", "number": "1800-599-0019"},
    "Global": {"name": "Befrienders Worldwide", "number": "Visit befrienders.org"}
}

TECHNIQUES = {
    "box_breathing": "Inhale for 4 seconds, hold for 4 seconds, exhale for 4 seconds, hold for 4 seconds. Repeat.",
    "54321_grounding": "Acknowledge 5 things you see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
    "body_scan": "Focus on your toes, tense them, then relax. Move slowly up your body to your head."
}

class Tools:
    @staticmethod
    def get_helpline(country_code="Global"):
        """Returns helpline info for a given country code (US, UK, IN, Global)."""
        return HELPLINES.get(country_code, HELPLINES["Global"])

    @staticmethod
    def get_grounding_technique(technique_name):
        """Returns the script for a specific technique."""
        return TECHNIQUES.get(technique_name, "Take a deep breath and count to ten.")

    @staticmethod
    def get_all_techniques():
        return list(TECHNIQUES.keys())
