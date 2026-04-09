import os

# Astro-Oracle 3.0 Demo Knowledge Base
# Creating high-density professional reference files for the RAG engine.

CONTENT = {
    "antique_turkish_astronomy.txt": """
ANTİK TÜRK GÖK BİLİMİ VE TAKIMYILDIZ EFSANELERİ
---
Eski Türk kozmolojisinde gökyüzü, 'Kök Kalı' olarak adlandırılan kutsal bir mekandır. 
Yedi katlı gök anlayışı, gezegenlerin yedi küresiyle ilişkilendirilirdi.

Ülker (Pleiades): Türk mitolojisinde 'Yedi Kız Kardeş' olarak bilinir. Tarım ve mevsimlerin habercisidir.
Demir Kazık (Kutup Yıldızı): Göğün merkezidir, her şey onun etrafında döner. Sadakat ve değişmezliği simgeler.
Yediger (Büyük Ayı): Türklerde 'Yedi Hanlar' olarak geçer. Karar verme ve idari stratejilerle ilişkilidir.
""",
    "helenistic_techniques.txt": """
HELENİSTİK ASTROLOJİ: TEMEL TEKNİKLER
---
Zaman Yöneticileri (Time Lords): Hayatın farklı dönemlerinin hangi gezegen tarafından yönetildiğini belirleyen sistem.
Zodiacal Releasing: Şans ve ruh noktalarından (Lot of Fortune/Spirit) hareketle kariyer ve yaşam amacını belirleme.
Sekt (Mezhep): Gündüz ve gece haritaları arasındaki temel ayrım. Gündüz haritasında Güneş, gece haritasında Ay başroldedir.
""",
    "astro_oracle_v3_manifesto.txt": """
ASTRO-ORACLE 3.0: ELITE CELESTIAL INTELLIGENCE HUB
---
Bu sistem, makine öğrenmesi ve kadim bilgeliğin kusursuz birleşimidir. 
Astro-Agent, yalnızca veriyi okumaz; gökyüzündeki sembolik dili insan hayatındaki stratejik kararlara dönüştürür.
Amacımız: Gökyüzünün rehberliğini, modern dünyanın hızıyla senkronize etmektir.
"""
}

def seed():
    data_dir = "app/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    for filename, content in CONTENT.items():
        path = os.path.join(data_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Besleme verisi oluşturuldu: {path}")

if __name__ == "__main__":
    seed()
