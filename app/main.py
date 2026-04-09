from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List
from app.core.config import settings
from app.models.schemas import NatalRequest, InterpretationResponse, HealthResponse
from app.chains.natal_chain import NatalChain

app = FastAPI(
    title=settings.APP_NAME,
    description="Astro-Oracle 2.0: Çok katmanlı RAG ve modüler akıl yürütme zincirleri ile güçlendirilmiş otonom gökyüzü analiz motoru.",
    version="0.2.0"
)

# Initialize Chains
natal_chain = NatalChain()

@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} 2.0: Celestial Intelligence Online", "status": "online"}

@app.get("/api/v1/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        version="0.2.0",
        engine="Astro-Oracle-Core"
    )

@app.post("/api/v1/interpret/natal", response_model=InterpretationResponse)
async def interpret_natal(request: NatalRequest):
    """
    Doğum haritasını modüler akıl yürütme zinciri kullanarak yorumlar.
    """
    try:
        response = await natal_chain.run(request.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/query")
async def generic_query(query: str, k: int = 5):
    """
    Vektör deposu üzerinde doğrudan arama yapar (Hata ayıklama ve ham veri erişimi için).
    """
    from app.rag_engine import rag_engine
    try:
        docs = rag_engine.search(query, k=k)
        return {"query": query, "results": [doc.page_content for doc in docs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
