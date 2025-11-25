"""
Defines the data structures for Agent-to-Agent communication.
"""
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class PlannerOutput:
    emotion: str
    risk_level: str
    action: str
    instruction: str

    def to_dict(self):
        return asdict(self)

@dataclass
class WorkerOutput:
    draft_response: str
    tools_used: List[str]

    def to_dict(self):
        return asdict(self)

@dataclass
class EvaluatorOutput:
    status: str
    feedback: str
    final_response: str

    def to_dict(self):
        return asdict(self)
