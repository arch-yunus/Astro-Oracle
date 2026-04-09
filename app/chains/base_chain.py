from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.rag_engine import rag_engine
from app.core.constants import SYSTEM_MESSAGES, PROMPT_TEMPLATES
from app.models.schemas import InterpretationResponse

class BaseAstrologyChain(ABC):
    def __init__(self, type: str):
        self.type = type
        self.system_message = SYSTEM_MESSAGES.get(type, SYSTEM_MESSAGES["NATAL"])
        self.llm = rag_engine.get_llm()

    @abstractmethod
    async def run(self, inputs: Dict[str, Any]) -> InterpretationResponse:
        pass

    def _format_docs(self, docs) -> str:
        return "\n\n".join([doc.page_content for doc in docs])
