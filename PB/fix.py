#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
baccarat_fix.py - WL Pattern Analyzer'ı P/B (Player/Banker) analizöre dönüştüren script

Bu script WL Pattern Analyzer'ı baccarat oyunu için düzenleyerek:
1. W (Win) ve L (Loss) yerine P (Player) ve B (Banker) olarak değiştirir
2. Renk temalarını baccarat oyununa uygun olarak günceller
3. Arayüz terminolojisini baccarat için düzenler
"""

import re
import os
import sys

def update_main_window_file(file_path="ui/main_window.py"):
    """main_window.py dosyasını günceller"""
    
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return False
    
    # Dosyayı oku
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Başlık ve pencere başlığını değiştir
    content = content.replace('WL Pattern Analyzer', 'Baccarat Pattern Analyzer')
    content = content.replace('W ve L Pattern Analiz', 'Baccarat P/B Pattern Analiz')
    
    # 2. W/L ifadelerini P/B olarak değiştir
    content = content.replace('"W"', '"P"')
    content = content.replace('"L"', '"B"')
    
    # 3. Renk temalarını baccarat'a uygun olarak değiştir
    # P (Player) için mavi tonları
    content = content.replace('#3a5d4a', '#3a4c5d')  # Koyu mavi-yeşil
    content = content.replace('#2a3d33', '#2a3340')  # Daha koyu mavi
    content = content.replace('#6ee7b7', '#6eb7e7')  # Açık mavi
    content = content.replace('#2a3b34', '#2a3441')  # Koyu mavi-gri
    
    # B (Banker) için kırmızı tonları - mevcut olduğu gibi kalsın
    # #5d3a4a - Koyu kırmızı
    # #3d2a33 - Daha koyu kırmızı
    # #fda4af - Açık kırmızı
    
    # 4. W/L buton yazıları değişimi
    win_button_pattern = r'self\.win_button = ModernButton\("W", self, "✓",'
    content = content.replace(win_button_pattern, 'self.win_button = ModernButton("P", self, "P",')
    
    loss_button_pattern = r'self\.loss_button = ModernButton\("L", self, "✗",'
    content = content.replace(loss_button_pattern, 'self.loss_button = ModernButton("B", self, "B",')
    
    # 5. Tahmin gösterimini güncelle
    content = content.replace('if result == 1:\n            self.prediction_indicator.setStyleSheet', 
                             'if result == 1:  # P (Player)\n            self.prediction_indicator.setStyleSheet')
    content = content.replace('elif result == 2:\n            self.prediction_indicator.setStyleSheet', 
                             'elif result == 2:  # B (Banker)\n            self.prediction_indicator.setStyleSheet')
    
    # Güncellenen içeriği dosyaya yaz
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{file_path} başarıyla güncellendi.")
    return True

def update_matrix_ui_file(file_path="ui/matrix_ui.py"):
    """matrix_ui.py dosyasını günceller"""
    
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return False
    
    # Dosyayı oku
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. W/L ifadelerini P/B olarak değiştir
    content = content.replace('text = "W" if self.value == 1 else "L"', 
                              'text = "P" if self.value == 1 else "B"')
    
    # 2. Renk temalarını güncelle (P için mavi tonları)
    content = content.replace('#6ee7b7', '#6eb7e7')  # Açık mavi
    
    # Güncellenen içeriği dosyaya yaz
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{file_path} başarıyla güncellendi.")
    return True

def update_pattern_analyzer_file(file_path="core/pattern_analyzer.py"):
    """pattern_analyzer.py dosyasını günceller"""
    
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return False
    
    # Dosyayı oku
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # W/L referanslarını P/B olarak değiştir
    content = content.replace('W/L', 'P/B')
    content = content.replace('W ve L', 'P ve B')
    
    # Açıklamaları güncelle
    content = content.replace('# Matristeki W ve L sayıları', '# Matristeki P ve B sayıları')
    content = content.replace('w_count = np.sum(matrix == 1)  # W sayısı', 'p_count = np.sum(matrix == 1)  # P sayısı')
    content = content.replace('l_count = np.sum(matrix == 2)  # L sayısı', 'b_count = np.sum(matrix == 2)  # B sayısı')
    
    # Değişken isimlerini güncelle
    content = content.replace('w_count', 'p_count')
    content = content.replace('l_count', 'b_count')
    content = content.replace('w_ratio', 'p_ratio')
    content = content.replace('l_ratio', 'b_ratio')
    content = content.replace('w_probability', 'p_probability')
    content = content.replace('l_probability', 'b_probability')
    content = content.replace('w_prob', 'p_prob')
    content = content.replace('l_prob', 'b_prob')
    content = content.replace('w_pattern', 'p_pattern')
    content = content.replace('l_pattern', 'b_pattern')
    
    # Güncellenen içeriği dosyaya yaz
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{file_path} başarıyla güncellendi.")
    return True

def update_model_files(models_dir="models"):
    """models klasöründeki tüm model dosyalarını günceller"""
    
    if not os.path.exists(models_dir):
        print(f"Hata: {models_dir} klasörü bulunamadı.")
        return False
    
    # .py uzantılı tüm dosyaları bul
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.py')]
    
    for file_name in model_files:
        file_path = os.path.join(models_dir, file_name)
        
        # Dosyayı oku
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # W/L referanslarını P/B olarak değiştir
        content = content.replace('W/L', 'P/B')
        content = content.replace('W ve L', 'P ve B')
        
        # Değişken isimlerini güncelle
        content = content.replace('w_count', 'p_count')
        content = content.replace('l_count', 'b_count')
        content = content.replace('w_ratio', 'p_ratio')
        content = content.replace('l_ratio', 'b_ratio')
        content = content.replace('w_probability', 'p_probability')
        content = content.replace('l_probability', 'b_probability')
        content = content.replace('w_prob', 'p_prob')
        content = content.replace('l_prob', 'b_prob')
        content = content.replace('w_pattern', 'p_pattern')
        content = content.replace('l_pattern', 'b_pattern')
        
        # W ve L açıklamalarını P ve B olarak değiştir
        content = content.replace('if prediction == 1:  # W', 'if prediction == 1:  # P')
        content = content.replace('if prediction == 2:  # L', 'if prediction == 2:  # B')
        content = content.replace('return 1  # W', 'return 1  # P')
        content = content.replace('return 2  # L', 'return 2  # B')
        content = content.replace('return 1  # W tahmini', 'return 1  # P tahmini')
        content = content.replace('return 2  # L tahmini', 'return 2  # B tahmini')
        
        # Güncellenen içeriği dosyaya yaz
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"{file_path} başarıyla güncellendi.")
    
    return True

def create_additional_file():
    """Baccarat'a özgü ek bilgiler için yeni bir dosya oluştur"""
    
    file_path = "baccarat_info.py"
    
    # Dosya içeriğini parça parça oluşturalım
    content = [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*-",
        "",
        "# Baccarat Pattern Analyzer - Baccarat bilgileri",
        "",
        "# Baccarat oyunu hakkında bilgiler",
        "BACCARAT_RULES = {",
        "    \"Player\": \"P - Oyuncu eli. Genellikle mavi ile gösterilir.\",",
        "    \"Banker\": \"B - Bankacı eli. Genellikle kırmızı ile gösterilir.\",",
        "    \"Tie\": \"T - Beraberlik. Bu analiz aracında takip edilmiyor.\",",
        "    \"Pair\": \"Pair - Aynı değerde iki kart. Bu analiz aracında takip edilmiyor.\",",
        "}",
        "",
        "# Baccarat masa limitleri",
        "TABLE_LIMITS = {",
        "    \"Minimum\": 100,",
        "    \"Maximum\": 10000,",
        "}",
        "",
        "# Temel pattern türleri",
        "PATTERN_TYPES = [",
        "    \"Bead Plate - Temel P/B sonuçları dizisi\",",
        "    \"Big Road - 6x50 matris formatında sonuçlar\",",
        "    \"Big Eye Road - Big Road'a göre türetilen pattern\",",
        "    \"Small Road - Big Road'dan türetilen başka bir pattern\",",
        "    \"Cockroach Road - Big Road'dan türetilen üçüncü pattern\",",
        "]",
        "",
        "# Baccarat stratejileri",
        "STRATEGIES = [",
        "    \"Takip stratejisi - Kazanan tarafa bahis yap\",",
        "    \"Ters takip - Kaybeden tarafa bahis yap\",",
        "    \"Eğilim analizi - Uzun dönemli trend analizi\",",
        "    \"Desen analizi - Big Road ve diğer desenler üzerinden tahmin\",",
        "    \"İstatistiksel analiz - Matematiksel olasılıkları takip et\",",
        "]",
        "",
        "def get_baccarat_info():",
        "    # Baccarat bilgilerini yazdırır",
        "    ",
        "    print(\"===== BACCARAT OYUNU HAKKINDA =====\")",
        "    print(\"Baccarat, P (Player/Oyuncu) ve B (Banker/Bankacı) arasındaki bir kart oyunudur.\")",
        "    print(\"Oyunun amacı hangi elin 9'a en yakın değere sahip olacağını tahmin etmektir.\")",
        "    ",
        "    print(\"\\nTERİMLER:\")",
        "    for key, value in BACCARAT_RULES.items():",
        "        print(f\"- {value}\")",
        "    ",
        "    print(\"\\nSTRATEJİLER:\")",
        "    for strategy in STRATEGIES:",
        "        print(f\"- {strategy}\")",
        "",
        "if __name__ == \"__main__\":",
        "    get_baccarat_info()"
    ]
    
    # Satırları birleştirerek dosya içeriğini oluştur
    file_content = "\n".join(content)
    
    # Dosyayı oluştur
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print(f"{file_path} başarıyla oluşturuldu.")
    return True

def update_main_py(file_path="main.py"):
    """main.py dosyasını günceller"""
    
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return False
    
    # Dosyayı oku
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Başlık ve açıklamaları güncelle
    content = content.replace('W ve L Pattern Analiz', 'Baccarat P/B Pattern Analiz')
    
    # Güncellenen içeriği dosyaya yaz
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{file_path} başarıyla güncellendi.")
    return True

if __name__ == "__main__":
    # Varsayılan veya parametre olarak verilen klasör yolunu kullan
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = "."
    
    print("Baccarat Pattern Analyzer için dönüşüm başlatılıyor...")
    
    # Önce dosya yollarını oluştur
    main_window_path = os.path.join(base_dir, "ui", "main_window.py")
    matrix_ui_path = os.path.join(base_dir, "ui", "matrix_ui.py")
    pattern_analyzer_path = os.path.join(base_dir, "core", "pattern_analyzer.py")
    models_dir = os.path.join(base_dir, "models")
    main_py_path = os.path.join(base_dir, "main.py")
    
    # Dosyaları güncelle
    main_window_updated = update_main_window_file(main_window_path)
    matrix_ui_updated = update_matrix_ui_file(matrix_ui_path)
    pattern_analyzer_updated = update_pattern_analyzer_file(pattern_analyzer_path)
    models_updated = update_model_files(models_dir)
    main_py_updated = update_main_py(main_py_path)
    additional_file_created = create_additional_file()
    
    # Sonuçları göster
    print("\nDönüşüm tamamlandı.")
    print("Yapılan değişiklikler:")
    print("1. 'W' (Win) ifadeleri 'P' (Player) olarak değiştirildi")
    print("2. 'L' (Loss) ifadeleri 'B' (Banker) olarak değiştirildi")
    print("3. Renk temaları baccarat'a uygun olarak güncellendi:")
    print("   - P (Player) için mavi tonları")
    print("   - B (Banker) için kırmızı tonları")
    print("4. Uygulama başlığı 'Baccarat Pattern Analyzer' olarak değiştirildi")
    print("5. Buton ikonları baccarat sembollerine güncellendi")
    print("6. Baccarat bilgileri için yeni 'baccarat_info.py' dosyası oluşturuldu")
    
    print("\nUygulamayı şu komutla başlatabilirsiniz:")
    print("python main.py")
