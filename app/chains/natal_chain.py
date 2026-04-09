from typing import Dict, Any
from app.chains.base_chain import BaseAstrologyChain
from app.rag_engine import rag_engine
from app.core.constants import PROMPT_TEMPLATES
from app.models.schemas import InterpretationResponse

class NatalChain(BaseAstrologyChain):
    def __init__(self):
        super().__init__(type="NATAL")

    async def run(self, inputs: Dict[str, Any]) -> InterpretationResponse:
        user_id = inputs.get("user_id", "anonymous")
        focus_area = inputs.get("focus_area", "general")
        chart_data = inputs.get("chart_data", {})
        
        # 1. Format chart data for query
        query_parts = []
        for planet, info in chart_data.items():
            if isinstance(info, dict):
                sign = info.get("sign", "")
                house = info.get("house", "")
                query_parts.append(f"{planet} {sign}'ta {house}. evde")
        
        search_query = ", ".join(query_parts) + f". Odak alanı: {focus_area}"
        
        # 2. Advanced RAG Retrieval (MMR)
        docs = rag_engine.search(search_query, k=5)
        context = self._format_docs(docs)
        citations = rag_engine.get_citations(docs)
        
        # 3. Prompt Construction
        prompt = PROMPT_TEMPLATES["NATAL_SYNTHESIS"].format(
            user_id=user_id,
            focus_area=focus_area,
            chart_data_formatted=str(chart_data),
            context=context
        )
        
        # 4. LLM Invocation
        response = self.llm.invoke([
            ("system", self.system_message),
            ("user", prompt)
        ])
        
        return InterpretationResponse(
            interpretation=response.content,
            metadata={
                "engine": "Astro-Oracle-2.0",
                "focus": focus_area
            },
            citations=citations
        )
