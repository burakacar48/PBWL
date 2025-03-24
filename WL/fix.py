#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
stats_table_fix.py - WL Pattern Analyzer düzenleyici
Bu script, main_window.py dosyasını güncelleyerek:
1. Model istatistikleri tablosunu 3 satır görünecek şekilde küçültür
2. Tablo içinde scroll bar eklenerek tüm model istatistiklerini kaydırarak görmeyi sağlar
"""

import re
import os
import sys

def update_main_window_file(file_path):
    """main_window.py dosyasını günceller"""
    
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return False
    
    # Dosyayı oku
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. StatsTable sınıfında değişiklikler yap
    stats_table_class_pattern = r'class StatsTable\(QTableWidget\):.*?def update_stats\('
    stats_table_replacement = """class StatsTable(QTableWidget):
    \"\"\"Model istatistikleri için özel tablo widget'ı\"\"\"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Tablo ayarları
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Model", "Başarı", "Tahmin"])
        
        # Sadece 3 satır göster, geri kalanı scroll ile görüntülenecek
        self.setFixedHeight(120)  # Daha küçük sabit yükseklik
        
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)
        
        # Scroll bar ayarları
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Dikey scroll bar ekle
        
        # Tablo stil ayarları
        self.setStyleSheet(\"\"\"
            QTableWidget {
                background-color: #333345;
                border: none;
                border-radius: 6px;
                gridline-color: #3d3d54;
                color: white;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d54;
            }
            QTableWidget::item:selected {
                background-color: #3d3d54;
            }
            QHeaderView::section {
                background-color: #3d3d54;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QScrollBar:vertical {
                border: none;
                background: #333345;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4d4d66;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        \"\"\")
    
    def update_stats("""
    
    content = re.sub(stats_table_class_pattern, stats_table_replacement, content, flags=re.DOTALL)
    
    # 2. İstatistik panelinin boyutunu ayarla
    stats_panel_pattern = r'# Model İstatistikleri Paneli\s+stats_panel = ModernPanel\("Model İstatistikleri", self\)'
    stats_panel_replacement = """# Model İstatistikleri Paneli
        stats_panel = ModernPanel("Model İstatistikleri", self)
        stats_panel.setMinimumHeight(200)  # İstatistik paneli için minimum yükseklik"""
    
    content = re.sub(stats_panel_pattern, stats_panel_replacement, content)
    
    # Güncellenmiş içeriği dosyaya yaz
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{file_path} başarıyla güncellendi.")
    return True

if __name__ == "__main__":
    # Varsayılan veya parametre olarak verilen dosya yolunu kullan
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "ui/main_window.py"
        
        # Dosya mevcut klasörde yoksa, ui/ klasöründe aramayı dene
        if not os.path.exists(file_path):
            file_path = os.path.join("ui", "main_window.py")
    
    result = update_main_window_file(file_path)
    
    if result:
        print("İşlem başarılı! Değişiklikler:")
        print("1. Model istatistikleri tablosu 3 satır görünecek şekilde ayarlandı")
        print("2. Tablo içerisinde dikey scroll bar eklendi")
        print("3. Tablo yüksekliği 120 piksel olarak sabitlendi")
        print("4. Scroll bar için özel stil ayarları eklendi")
        print("\nBu değişiklikleri incelemek veya geri almak için, dosyayı yedekleyin.")
    else:
        print("İşlem başarısız oldu. Lütfen main_window.py dosyasının doğru konumda olduğunu kontrol edin.")
