#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması - Modern UI
Ana uygulama başlatıcısı
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import WLPatternAnalyzer

if __name__ == "__main__":
    # High DPI display support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    # Fusion stil ile modern görünüm
    app.setStyle("Fusion")
    
    # Ana pencereyi oluştur ve göster
    main_window = WLPatternAnalyzer()
    main_window.show()
    
    sys.exit(app.exec_())