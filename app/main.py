from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.rag_engine import rag_engine
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Astro-Oracle: LLM ve RAG kullanarak çalışan otonom astroloji yorumlama motoru.",
    version="0.1.0"
)

class NatalChartRequest(BaseModel):
    user_id: str
    focus_area: str = "general"
    chart_data: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME}'a Hoş Geldiniz", "status": "online"}

@app.post("/api/v1/interpret/natal")
async def interpret_natal(request: NatalChartRequest):
    """
    RAG ve LLM kullanarak doğum haritasını yorumlar.
    """
    try:
        # 1. Harita verilerine dayalı bağlamsal arama sorgusu oluşturma
        # Örnek: "Güneş Koç'ta 10. evde, Ay Oğlak'ta 4. evde"
        query_parts = []
        for planet, info in request.chart_data.items():
            sign = info.get("sign", "")
            house = info.get("house", "")
            query_parts.append(f"{planet} {sign}'ta {house}. evde")
        
        search_query = ", ".join(query_parts) + f". Odak alanı: {request.focus_area}"
        
        # 2. Vektör deposundan ilgili belgeleri geri getirme
        docs = rag_engine.search(search_query)
        context = "\n".join([doc.page_content for doc in docs])
        
        # 3. LLM yorumunu alama
        llm = rag_engine.get_llm()
        
        prompt = f"""
        Sistem: Sen Astro-Oracle adında seçkin bir gökyüzü yorumcususun. 
        Kullanıcının doğum haritasını yorumlamak için aşağıdaki tarihi ve teknik bağlamı kullan.
        Şiirsel, analitik ve uygun yerlerde derinlemesine teknik ol.
        
        Bağlam:
        {context}
        
        Aşağıdaki harita verilerini yorumla:
        {request.chart_data}
        
        Odak Alanı: {request.focus_area}
        """
        
        # Basit bir çağrı kullanın
        response = llm.invoke(prompt)
        
        return {
            "interpretation": response.content,
            "metadata": {
                "sources_used": len(docs),
                "model": "yapılandırılmış-llm"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
