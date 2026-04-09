from typing import Dict, Any
from app.chains.base_chain import BaseAstrologyChain
from app.rag_engine import rag_engine
from app.models.schemas import InterpretationResponse

class TransitChain(BaseAstrologyChain):
    def __init__(self):
        super().__init__(type="TRANSIT")

    async def run(self, inputs: Dict[str, Any]) -> InterpretationResponse:
        natal_chart = inputs.get("natal_chart", {})
        transit_data = inputs.get("transit_data", {})
        
        # 1. Format combined chart data for query
        search_query = f"Transit tahmini ve zaman döngüleri: {transit_data}. Doğum haritası: {natal_chart}"
        
        # 2. Advanced RAG Retrieval
        docs = rag_engine.search(search_query, k=5)
        context = self._format_docs(docs)
        citations = rag_engine.get_citations(docs)
        
        # 3. Prompt (Time-focused)
        prompt = f"""
        Zaman Döngüleri Analizi:
        Güncel Transitler: {transit_data}
        Kullanıcı Doğum Haritası: {natal_chart}
        
        Bağlam (RAG):
        {context}
        
        Talimatlar: Mevcut enerjileri, tetiklenen açıları ve öngörüleri zaman bağımlı şekilde yorumla.
        """
        
        # 4. LLM Invocation
        response = self.llm.invoke([
            ("system", "Sen zamanın efendisi olan bir Astro-Oracle öngörü uzmanısın."),
            ("user", prompt)
        ])
        
        return InterpretationResponse(
            interpretation=response.content,
            metadata={
                "engine": "Astro-Oracle-3.0",
                "type": "transits"
            },
            citations=citations
        )
