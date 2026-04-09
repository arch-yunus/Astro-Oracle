# 🪐 Astro-Oracle: Otonom Gökyüzü Yorumlama Motoru

[![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Sürümü](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Aktif-green.svg)](https://python.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vektör_Veritabanı-ff69b4.svg)](https://www.trychroma.com/)

**Astro-Oracle**, **Geri Getirme Artırımlı Üretim (RAG)** ve gelişmiş **Büyük Dil Modellerini (LLM)** kullanan kurumsal düzeyde otonom bir gökyüzü yorumlama motorudur. Statik astroloji botlarının aksine Astro-Oracle; antik gök bilimi metinlerini, tarihi el yazmalarını ve çeşitli mitolojik çerçeveleri dinamik ve bağlama duyarlı bir şekilde sentezler.

---

## 🏛️ Sistem Mimarisi

Astro-Oracle, yetkili kaynaklara dayanan yüksek doğruluklu yorumlar sağlamak için çok katmanlı bir RAG boru hattı kullanır.

```mermaid
graph TD
    A[Kullanıcı Harita Verisi] --> B[RAG Sorgu Oluşturucu]
    B --> C{Bağlam Geri Getirici}
    C -->|Semantik Arama| D[(ChromaDB Vektör Havuzu)]
    D --> E[Bilgi Bağlamı]
    E --> F[Prompt Mühendisliği Katmanı]
    F --> G[LLM Akıl Yürütme Motoru]
    G --> H[Final Yorumlama]
    
    subgraph "Bilgi Bankası (Veri İşleme)"
    I[Antik Metinler] --> J[Parçalama ve Embedding]
    K[Astroloji El Kitapları] --> J
    L[Mitolojik Kayıtlar] --> J
    J --> D
    end
```

### Temel Bileşenler
- **`app/main.py`**: Yorumlama istekleri için FastAPI tabanlı REST geçidi.
- **`app/rag_engine.py`**: LangChain, ChromaDB ve LLM sağlayıcıları için entegrasyon katmanı.
- **`app/core/config.py`**: `pydantic-settings` üzerinden merkezi yapılandırma yönetimi.
- **`scripts/ingest_data.py`**: Özyinelemeli doküman dizinleme ve vektörleştirme için özelleşmiş hat.

---

## 🔬 Temel Özellikler

- **Semantik Çok Kaynaklı Sentez**: Batı, Vedik, Helenistik ve Antik Türk (Tengrizm) astronomik perspektiflerinden dinamik bağlam geri getirimi.
- **Agnostik LLM Entegrasyonu**: **OpenAI (GPT-4/Turbo)** ve **Google (Gemini Pro)** için hazır konfigürasyon; yerel modeller (Llama 3/Mistral) ile uyumluluk.
- **Yüksek Yoğunluklu Prompt Mühendisliği**: Analitik, şiirsel ve teknik olarak doğru gökyüzü okumaları için tasarlanmış bağlam zengini istemler.
- **Ölçeklenebilir Doküman Hattı**: Karmaşık PDF ve metin kaynaklarının otomatik olarak yüksek performanslı bir vektör veritabanına dönüştürülmesi.

---

## 🚀 Hızlı Kurulum

### 1. Ortam Yapılandırması
Depoyu klonlayın ve sanal ortamı başlatın:
```bash
git clone https://github.com/arch-yunus/astro-oracle.git
cd astro-oracle
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Gizli Değişkenlerin Yönetimi
`.env` dosyanızı şablon üzerinden yapılandırın:
```bash
cp .env.example .env
# .env dosyasını OPENAI_API_KEY veya GOOGLE_API_KEY ile güncelleyin
```

### 3. Bilgi İşleme (Ingestion)
`app/data/` klasörüne kaynak dokümanlarınızı yerleştirin ve işlemeyi başlatın:
```bash
python scripts/ingest_data.py --source ./app/data
```

### 4. Servisi Başlatma
FastAPI sunucusunu yayına alın:
```bash
uvicorn app.main:app --reload --port 8000
```

---

## 🛰️ API Kullanım Örneği

**Uç Nokta (Endpoint):** `POST /api/v1/interpret/natal`

**İstek Gövdesi (Payload):**
```json
{
  "user_id": "nexus-01",
  "focus_area": "strategic_alignment",
  "chart_data": {
    "sun": {"sign": "Aries", "house": 10},
    "moon": {"sign": "Capricorn", "house": 4},
    "mars": {"sign": "Scorpio", "house": 8}
  }
}
```

---

## 🗺️ Stratejik Yol Haritası

- [x] **Aşama 1**: Temel RAG Hattı ve Vektör Veritabanı Uygulaması.
- [x] **Aşama 2**: Çoklu-LLM Desteği (OpenAI / Gemini).
- [/] **Aşama 3**: Tarihi Türk Astronomi Veri Entegrasyonu.
- [ ] **Aşama 4**: Gerçek Zamanlı Transit İzleme Merkezi (WebSockets).
- [ ] **Aşama 5**: İnteraktif Harita Sentezi (LLM Destekli Sohbet).

---

## 🛡️ Lisans ve Telif Hakkı

**MIT Lisansı** altında dağıtılmaktadır. Daha fazla bilgi için `LICENSE` dosyasına bakınız.
Telif Hakkı (c) 2026 **Astro-Oracle**.
