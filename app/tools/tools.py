from langchain.tools import tool
from typing import Optional, Dict, Any
from app.rag_engine import rag_engine

@tool
def celestial_knowledge_search(query: str) -> str:
    """
    Antik metinler, astroloji el kitapları ve mitolojik kayıtlardan oluşan vektör deposunda semantik arama yapar.
    Karmaşık astrolojik kavramları ve tarihi bağlamları anlamak için bu aracı kullanın.
    """
    docs = rag_engine.search(query, k=5)
    return "\n\n".join([doc.page_content for doc in docs])

@tool
def get_astrology_metadata(term: str) -> str:
    """
    Gezegen sembolleri, temel nitelikler ve astrolojik terimlerin teknik tanımlarını getirir.
    Terimler sözlüğü olarak kullanılabilir.
    """
    from app.core.constants import PLANET_SYMBOLS
    # Simple lookup for now
    term_lower = term.lower()
    for planet, symbol in PLANET_SYMBOLS.items():
        if planet.lower() in term_lower:
            return f"{planet} sembolü: {symbol}"
    return f"'{term}' terimi için özel metadata bulunamadı."
