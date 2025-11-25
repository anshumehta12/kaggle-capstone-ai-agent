"""
Simple logger to track agent thoughts.
"""
import datetime

class Logger:
    def __init__(self):
        self.logs = []

    def log(self, agent_name, message, data=None):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {agent_name}: {message}"
        if data:
            entry += f"\nData: {data}"
        print(entry) # Print to console for Colab visibility
        self.logs.append(entry)

    def get_logs(self):
        return "\n".join(self.logs)

# Singleton instance
logger = Logger()
