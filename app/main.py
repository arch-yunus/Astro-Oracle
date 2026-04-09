from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.models.schemas import NatalRequest, InterpretationResponse, HealthResponse
from app.chains.natal_chain import NatalChain
from app.chains.synastry_chain import SynastryChain
from app.chains.transit_chain import TransitChain
from app.agents.core import astro_agent
import os

app = FastAPI(
    title=settings.APP_NAME,
    description="Astro-Oracle 3.0: Otonom Ajanlar ve Çok Katmanlı Gök Bilimi Zekası.",
    version="0.3.0"
)

# Mount Frontend
if os.path.exists("frontend"):
    app.mount("/gui", StaticFiles(directory="frontend", html=True), name="gui")

# Initialize Chains & Engines
natal_chain = NatalChain()
synastry_chain = SynastryChain()
transit_chain = TransitChain()

@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} 3.0: Elite Celestial Intelligence Hub Online", "status": "online"}

@app.get("/api/v1/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        version="0.3.0",
        engine="Astro-Oracle-Elite-Core"
    )

@app.post("/api/v1/interpret/natal", response_model=InterpretationResponse)
async def interpret_natal(request: NatalRequest):
    """Doğum haritasını modüler zincir üzerinden analiz eder."""
    try:
        response = await natal_chain.run(request.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/agent/query")
async def agent_query(query: str):
    """
    Otonom Astro-Ajan'ı çalıştırır. Karmaşık ve çok adımlı gökyüzü soruları için kullanılır.
    """
    try:
        response = await astro_agent.run(query)
        return {"agent_response": response, "query": query}
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
