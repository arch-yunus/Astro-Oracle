from typing import Dict, Any
from app.chains.base_chain import BaseAstrologyChain
from app.rag_engine import rag_engine
from app.core.constants import PROMPT_TEMPLATES
from app.models.schemas import InterpretationResponse

class SynastryChain(BaseAstrologyChain):
    def __init__(self):
        super().__init__(type="SYNASTRY")

    async def run(self, inputs: Dict[str, Any]) -> InterpretationResponse:
        user_ids = inputs.get("user_ids", ["P1", "P2"])
        partner_chart_data = inputs.get("partner_chart_data", {})
        
        # 1. Format combined chart data for query
        search_query = f"Sinastri analizi: Gezegenler arası uyum, çekim ve karma. {partner_chart_data}"
        
        # 2. Advanced RAG Retrieval
        docs = rag_engine.search(search_query, k=5)
        context = self._format_docs(docs)
        citations = rag_engine.get_citations(docs)
        
        # 3. Prompt (Simplified for now)
        prompt = f"""
        Sinastri Analizi Talebi:
        Partner 1 ve Partner 2 harita verileri: {partner_chart_data}
        
        Bağlam (RAG):
        {context}
        
        Talimatlar: İlişki dinamiklerini, karmik bağları ve uyumu analiz et.
        """
        
        # 4. LLM Invocation
        response = self.llm.invoke([
            ("system", "Sen uzman bir sinastri ve ilişki astroloğu olan Astro-Oracle'sın."),
            ("user", prompt)
        ])
        
        return InterpretationResponse(
            interpretation=response.content,
            metadata={
                "engine": "Astro-Oracle-3.0",
                "type": "synastry"
            },
            citations=citations
        )
