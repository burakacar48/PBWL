#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Baccarat Pattern Analyzer - Baccarat bilgileri

# Baccarat oyunu hakkında bilgiler
BACCARAT_RULES = {
    "Player": "P - Oyuncu eli. Genellikle mavi ile gösterilir.",
    "Banker": "B - Bankacı eli. Genellikle kırmızı ile gösterilir.",
    "Tie": "T - Beraberlik. Bu analiz aracında takip edilmiyor.",
    "Pair": "Pair - Aynı değerde iki kart. Bu analiz aracında takip edilmiyor.",
}

# Baccarat masa limitleri
TABLE_LIMITS = {
    "Minimum": 100,
    "Maximum": 10000,
}

# Temel pattern türleri
PATTERN_TYPES = [
    "Bead Plate - Temel P/B sonuçları dizisi",
    "Big Road - 6x50 matris formatında sonuçlar",
    "Big Eye Road - Big Road'a göre türetilen pattern",
    "Small Road - Big Road'dan türetilen başka bir pattern",
    "Cockroach Road - Big Road'dan türetilen üçüncü pattern",
]

# Baccarat stratejileri
STRATEGIES = [
    "Takip stratejisi - Kazanan tarafa bahis yap",
    "Ters takip - Kaybeden tarafa bahis yap",
    "Eğilim analizi - Uzun dönemli trend analizi",
    "Desen analizi - Big Road ve diğer desenler üzerinden tahmin",
    "İstatistiksel analiz - Matematiksel olasılıkları takip et",
]

def get_baccarat_info():
    # Baccarat bilgilerini yazdırır
    
    print("===== BACCARAT OYUNU HAKKINDA =====")
    print("Baccarat, P (Player/Oyuncu) ve B (Banker/Bankacı) arasındaki bir kart oyunudur.")
    print("Oyunun amacı hangi elin 9'a en yakın değere sahip olacağını tahmin etmektir.")
    
    print("\nTERİMLER:")
    for key, value in BACCARAT_RULES.items():
        print(f"- {value}")
    
    print("\nSTRATEJİLER:")
    for strategy in STRATEGIES:
        print(f"- {strategy}")

if __name__ == "__main__":
    get_baccarat_info()