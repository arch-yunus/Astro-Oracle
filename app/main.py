from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.rag_engine import rag_engine
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Astro-Oracle: Autonomous Astrology Interpretation Engine using LLM and RAG.",
    version="0.1.0"
)

class NatalChartRequest(BaseModel):
    user_id: str
    focus_area: str = "general"
    chart_data: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "status": "online"}

@app.post("/api/v1/interpret/natal")
async def interpret_natal(request: NatalChartRequest):
    """
    Interprets a natal chart using RAG and LLM.
    """
    try:
        # 1. Construct contextual search query based on chart data
        # Example: "Sun in Aries house 10, Moon in Capricorn house 4"
        query_parts = []
        for planet, info in request.chart_data.items():
            sign = info.get("sign", "")
            house = info.get("house", "")
            query_parts.append(f"{planet} in {sign} house {house}")
        
        search_query = ", ".join(query_parts) + f". Focus area: {request.focus_area}"
        
        # 2. Retrieve relevant documents from Vector Store
        docs = rag_engine.search(search_query)
        context = "\n".join([doc.page_content for doc in docs])
        
        # 3. Get LLM interpretation
        llm = rag_engine.get_llm()
        
        prompt = f"""
        System: You are Astro-Oracle, an elite celestial interpreter. 
        Use the following historical and technical context to interpret the user's natal chart.
        Be poetic, analytical, and deeply technical where appropriate.
        
        Context:
        {context}
        
        Interpret the following chart data:
        {request.chart_data}
        
        Focus Area: {request.focus_area}
        """
        
        # Use a simple call for boilerplate
        response = llm.invoke(prompt)
        
        return {
            "interpretation": response.content,
            "metadata": {
                "sources_used": len(docs),
                "model": "configured-llm"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
