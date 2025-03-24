#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması - Modern UI
Ana pencere uygulaması
"""

import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QComboBox, QGridLayout, 
                            QStackedWidget, QMessageBox, QGroupBox, QSizePolicy,
                            QFrame, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient, QPainter, QBrush, QPen, QFontMetrics

from ui.matrix_ui import MatrixUI
from core.pattern_analyzer import analyze_pattern
from models.base_model import BaseAnalysisModel
from models.diagonal import DiagonalAnalysis
from models.rectangle import RectangleAnalysis
from models.lshape import LShapeAnalysis
from models.tshape import TShapeAnalysis
from models.spiral import SpiralAnalysis
from models.neighborhood import NeighborhoodAnalysis
from models.zigzag import ZigzagAnalysis
from models.scatter import ScatterAnalysis
from models.quadrant import QuadrantAnalysis
from models.symmetry import SymmetryAnalysis
from models.border import BorderAnalysis
from models.heatmap import HeatmapAnalysis
from models.combined import CombinedAnalysis
from models.hibrit import HibritAnalysis


class ModernButton(QPushButton):
    """Modern görünümlü gradyan buton"""
    
    def __init__(self, text="", parent=None, icon_text="", start_color="#3a5d4a", end_color="#2a3d33"):
        super().__init__(text, parent)
        
        self.start_color = start_color
        self.end_color = end_color
        self.icon_text = icon_text
        
        # Buton stilini ayarla
        self.setMinimumHeight(50)  # Buton yüksekliğini artırdık
        font = QFont("Arial", 16, QFont.Bold)  # Font boyutunu daha da artırdık
        self.setFont(font)
        
        # İkon boşluğu ekle - metin yoksa veya sadece ikon varsa
        if icon_text:
            # Metin boşsa (sadece ikon)
            if not text:
                self.setStyleSheet(f"""
                    QPushButton {{
                        color: white;
                        border: none;
                        border-radius: 6px;
                        text-align: center;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                      stop:0 {self.lighten_color(start_color)}, 
                                                      stop:1 {self.lighten_color(end_color)});
                    }}
                    QPushButton:pressed {{
                        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                       stop:0 {end_color}, 
                                                       stop:1 {start_color});
                    }}
                """)
            else:
                # İkon ve metin
                self.setStyleSheet(f"""
                    QPushButton {{
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding-left: 45px;
                        text-align: center;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                      stop:0 {self.lighten_color(start_color)}, 
                                                      stop:1 {self.lighten_color(end_color)});
                    }}
                    QPushButton:pressed {{
                        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                       stop:0 {end_color}, 
                                                       stop:1 {start_color});
                    }}
                """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    color: white;
                    border: none;
                    border-radius: 6px;
                    text-align: center;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 {self.lighten_color(start_color)}, 
                                                  stop:1 {self.lighten_color(end_color)});
                }}
                QPushButton:pressed {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 {end_color}, 
                                                   stop:1 {start_color});
                }}
            """)
    
    def lighten_color(self, color, factor=120):
        """Rengi açıklaştırır"""
        color = color.lstrip('#')
        r = min(255, int(color[0:2], 16) + factor)
        g = min(255, int(color[2:4], 16) + factor)
        b = min(255, int(color[4:6], 16) + factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def paintEvent(self, event):
        """Buton çizimi"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Buton arka planı
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(self.start_color))
        gradient.setColorAt(1, QColor(self.end_color))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 6, 6)
        
        # İkon çizimi
        if self.icon_text:
            # Sadece ikon mu yoksa ikon+metin mi?
            if not self.text():
                # Sadece ikonsa, ortala
                icon_size = 28  # İkon boyutunu daha da artırdık
                icon_x = (self.width() - icon_size) // 2
                icon_y = (self.height() - icon_size) // 2
                
                painter.setPen(QPen(QColor("#ffffff")))
                painter.setBrush(QBrush(QColor("#ffffff")))
                painter.drawEllipse(icon_x, icon_y, icon_size, icon_size)
                
                # İkon metni
                painter.setPen(QPen(QColor(self.end_color)))
                icon_font = QFont("Arial", 14, QFont.Bold)  # Font boyutunu artırdık
                painter.setFont(icon_font)
                metrics = QFontMetrics(icon_font)
                text_width = metrics.horizontalAdvance(self.icon_text)
                painter.drawText(
                    icon_x + (icon_size - text_width) // 2,
                    icon_y + icon_size // 2 + metrics.ascent() // 2 - 1,
                    self.icon_text
                )
            else:
                # İkon ve metin
                icon_size = 28  # İkon boyutunu artırdık
                icon_x = 15
                icon_y = (self.height() - icon_size) // 2
                
                painter.setPen(QPen(QColor("#ffffff")))
                painter.setBrush(QBrush(QColor("#ffffff")))
                painter.drawEllipse(icon_x, icon_y, icon_size, icon_size)
                
                # İkon metni
                painter.setPen(QPen(QColor(self.end_color)))
                icon_font = QFont("Arial", 14, QFont.Bold)
                painter.setFont(icon_font)
                metrics = QFontMetrics(icon_font)
                text_width = metrics.horizontalAdvance(self.icon_text)
                painter.drawText(
                    icon_x + (icon_size - text_width) // 2,
                    icon_y + icon_size // 2 + metrics.ascent() // 2 - 1,
                    self.icon_text
                )
                
                # Ana metin - ikon varsa sağa kaydır
                painter.setPen(QPen(QColor("#ffffff")))
                text_rect = self.rect().adjusted(icon_x + icon_size + 10, 0, 0, 0)
                painter.drawText(text_rect, Qt.AlignCenter, self.text())
        else:
            # İkon yoksa metni tam ortala
            painter.setPen(QPen(QColor("#ffffff")))
            painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class StatsTable(QTableWidget):
    """Model istatistikleri için özel tablo widget'ı"""
    
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
        self.setStyleSheet("""
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
        """)
    
    def update_stats(self, model_stats, predictions=None):
        """Model istatistiklerini günceller"""
        if predictions is None:
            predictions = {}
            
        # Hibrit Analiz'i gizle
        filtered_stats = {k: v for k, v in model_stats.items() if k != "Hibrit Analiz"}
        
        # Sıralanacak modellerin sayısını güncelle
        self.setRowCount(len(filtered_stats))
        
        # Model istatistiklerini sırala (başarı oranına göre azalan)
        sorted_stats = sorted(
            filtered_stats.items(), 
            key=lambda x: x[1]["success_rate"], 
            reverse=True
        )
        
        for i, (model_name, stats) in enumerate(sorted_stats):
            # Model adı
            name_item = QTableWidgetItem(model_name)
            self.setItem(i, 0, name_item)
            
            # Başarı oranı
            success_rate = stats.get('success_rate', 0)
            correct = stats.get('correct', 0)
            total = stats.get('total', 0)
            
            # Eğer tahmin yapıldıysa, doğruları da göster
            if total >= 3:  # En az 3 tahmin yapıldıysa
                success_item = QTableWidgetItem(f"{success_rate}% ({correct}/{total})")
            elif total > 0:  # 1-2 tahmin varsa, güvenilir değil mesajı
                success_item = QTableWidgetItem(f"Yetersiz ({correct}/{total})")
            else:
                success_item = QTableWidgetItem(f"Veri yok")
            
            # Başarı oranına göre renklendirme
            if total >= 3:  # Sadece yeterli tahmin varsa renklendirme yap
                if success_rate >= 70:
                    success_item.setForeground(QColor("#6ee7b7"))  # Yeşil
                elif success_rate >= 60:
                    success_item.setForeground(QColor("#fcd34d"))  # Sarı
                else:
                    success_item.setForeground(QColor("#fda4af"))  # Kırmızı
            else:
                success_item.setForeground(QColor("#aaaaaa"))  # Gri (yeterli veri yok)
            
            success_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(i, 1, success_item)
            
            # Tahmin
            prediction = predictions.get(model_name, 0)
            
            if prediction == 1:
                pred_text = "W"
                pred_color = QColor("#6ee7b7")  # Yeşil
            elif prediction == 2:
                pred_text = "L"
                pred_color = QColor("#fda4af")  # Kırmızı
            else:
                pred_text = "-"
                pred_color = QColor("#aaaaaa")  # Gri
                
            pred_item = QTableWidgetItem(pred_text)
            pred_item.setForeground(pred_color)
            pred_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(i, 2, pred_item)


class ModernPanel(QFrame):
    """Modern görünümlü panel"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        
        # Panel stilini ayarla
        self.setStyleSheet("""
            QFrame {
                background-color: #333345;
                border-radius: 8px;
            }
        """)
        
        # Ana layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        
        # Başlık
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                }
            """)
            self.layout.addWidget(title_label)


class WLPatternAnalyzer(QMainWindow):
    """W ve L Pattern analiz için ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        
        # Ana pencere ayarları
        self.setWindowTitle("WL Pattern Analyzer")
        self.setMinimumSize(700, 450)  # Pencere boyutunu artırdık
        self.setMaximumSize(700, 450)
        
        # Uygulama verisi
        self.matrix_data = np.zeros((5, 5), dtype=int)  # 0: Boş, 1: W, 2: L
        self.history = []  # Tüm sonuç geçmişi
        
        # Kullanılabilir analiz modelleri
        self.analysis_models = {
            "Çapraz (Diagonal)": DiagonalAnalysis(),
            "Dikdörtgen": RectangleAnalysis(),
            "L-Şekli": LShapeAnalysis(),
            "T-Şekli": TShapeAnalysis(),
            "Spiral": SpiralAnalysis(),
            "Komşuluk": NeighborhoodAnalysis(),
            "Zig-Zag": ZigzagAnalysis(),
            "Serpme": ScatterAnalysis(),
            "Kuadran": QuadrantAnalysis(),
            "Simetri": SymmetryAnalysis(),
            "Sınır": BorderAnalysis(),
            "Isı Haritası": HeatmapAnalysis(),
            "Karma Analiz": CombinedAnalysis(),
            "Hibrit Analiz": HibritAnalysis()
        }
        
        # Şu anki aktif model
        self.current_model = self.analysis_models["Hibrit Analiz"]
        
        # Model istatistikleri
        self.model_stats = {model_name: {"success_rate": 50, "correct": 0, "total": 0} 
                          for model_name in self.analysis_models.keys()}
        
        # Gerçek sonuçlar (kullanıcı doğrulaması için)
        self.actual_results = []
        
        # Karanlık mod uygula
        self._set_dark_theme()
        
        # Arayüz kurulumu
        self._setup_ui()
        
    def _set_dark_theme(self):
        """Karanlık mod teması uygular"""
        palette = QPalette()
        
        # Temel renkler
        palette.setColor(QPalette.Window, QColor("#1e1e2e"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#252535"))
        palette.setColor(QPalette.AlternateBase, QColor("#2a2a3c"))
        palette.setColor(QPalette.ToolTipBase, QColor("#1e1e2e"))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#333345"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.white)
        palette.setColor(QPalette.Link, QColor("#6ee7b7"))
        palette.setColor(QPalette.Highlight, QColor("#6ee7b7"))
        palette.setColor(QPalette.HighlightedText, QColor("#1e1e2e"))
        
        # Devre dışı widget renkleri
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#aaaaaa"))
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor("#aaaaaa"))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor("#aaaaaa"))
        
        self.setPalette(palette)
        
        # Global stil ayarları
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLabel {
                color: white;
            }
            QComboBox {
                background-color: #3d3d54;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px 10px;
                min-height: 30px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 20px;
                height: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #3d3d54;
                color: white;
                selection-background-color: #6ee7b7;
                selection-color: #1e1e2e;
                border: none;
            }
        """)
        
    def _setup_ui(self):
        """Ana uygulama arayüzünü kurar"""
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Sabit boşluklar için QVBoxLayout kullanalım
        main_wrapper = QVBoxLayout(central_widget)
        main_wrapper.setContentsMargins(10, 10, 10, 10)
        
        # Uygulama Başlığı
        header_panel = QFrame()
        header_panel.setStyleSheet("background-color: #252535; border-radius: 8px;")
        header_panel.setFixedHeight(40)
        
        header_layout = QHBoxLayout(header_panel)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # Logo
        logo_label = QLabel()
        logo_label.setFixedSize(20, 20)
        logo_label.setStyleSheet("background-color: #94e2cd; border-radius: 10px;")
        header_layout.addWidget(logo_label)
        
        # Başlık metni
        title_label = QLabel("WL Pattern Analyzer")
        title_font = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        # Model seçimi başlığa taşındı
        header_layout.addStretch()
        
        model_label = QLabel("Model:")
        model_label.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        header_layout.addWidget(model_label)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(list(self.analysis_models.keys()))
        self.model_combo.setCurrentText("Hibrit Analiz")
        self.model_combo.currentIndexChanged.connect(self._on_model_changed)
        self.model_combo.setFixedWidth(200)
        header_layout.addWidget(self.model_combo)
        
        # Başlığı ekle
        main_wrapper.addWidget(header_panel)
        
        # Ana içerik paneli
        content_panel = QFrame()
        content_panel.setStyleSheet("background-color: transparent;")
        
        main_layout = QHBoxLayout(content_panel)
        main_layout.setContentsMargins(0, 10, 0, 0)
        main_layout.setSpacing(10)
        
        # Sol Panel - Matris
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #2a2a3c; border-radius: 8px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(10)
        
        # Matris gösterimi
        self.matrix_ui = MatrixUI(self)
        self.matrix_ui.cell_clicked.connect(self._on_cell_clicked)
        self.matrix_ui.setStyleSheet("QFrame { background-color: transparent; }")
        left_layout.addWidget(self.matrix_ui)
        
        # Matris durum
        matrix_status_layout = QHBoxLayout()
        matrix_status_label = QLabel("Matris Durum:")
        matrix_status_label.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        matrix_status_layout.addWidget(matrix_status_label)
        
        self.matrix_status_value = QLabel("0 girdi (min. 5 gerekli)")
        self.matrix_status_value.setStyleSheet("font-size: 14px;")
        matrix_status_layout.addWidget(self.matrix_status_value)
        matrix_status_layout.addStretch()
        
        left_layout.addLayout(matrix_status_layout)
        
        # Butonlar paneli - Dikey düzene çevir
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        
        # W ve L butonları için yatay düzen
        wl_buttons_layout = QHBoxLayout()
        wl_buttons_layout.setSpacing(10)
        
        # W butonu
        self.win_button = ModernButton("W", self, "✓", "#3a5d4a", "#2a3d33")
        self.win_button.clicked.connect(lambda: self._add_selection(1))
        self.win_button.setMinimumWidth(80)  # Genişliği biraz azalttık
        wl_buttons_layout.addWidget(self.win_button)
        
        # L butonu
        self.loss_button = ModernButton("L", self, "✗", "#5d3a4a", "#3d2a33")
        self.loss_button.clicked.connect(lambda: self._add_selection(2))
        self.loss_button.setMinimumWidth(80)  # Genişliği biraz azalttık
        wl_buttons_layout.addWidget(self.loss_button)
        
        # W/L butonlarını ana buton düzenine ekle
        buttons_layout.addLayout(wl_buttons_layout)
        
        # Geri Al ve Temizle butonları için yatay düzen
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setSpacing(10)
        
        # Geri Al butonu - sadece ikon
        self.undo_button = ModernButton("", self, "↩", "#3a5d65", "#2a3d45")
        self.undo_button.setToolTip("Geri Al")
        self.undo_button.clicked.connect(self._on_undo_clicked)
        self.undo_button.setEnabled(False)
        action_buttons_layout.addWidget(self.undo_button)
        
        # Temizle butonu - sadece ikon
        self.clear_button = ModernButton("", self, "🧹", "#4d4a55", "#3d3a45")
        self.clear_button.setToolTip("Temizle")
        self.clear_button.clicked.connect(self._on_clear_clicked)
        self.clear_button.setEnabled(False)
        action_buttons_layout.addWidget(self.clear_button)
        
        # Geri Al/Temizle butonlarını ana buton düzenine ekle
        buttons_layout.addLayout(action_buttons_layout)  # Ağırlık 1 olarak ayarlandı
        
        left_layout.addLayout(buttons_layout)
        
        # Sol paneli ana layout'a ekle
        main_layout.addWidget(left_panel, 6)  # Önceden 1 idi, 0.6 oranı için 6:10
        
        # Sağ Panel - Analiz
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #2a2a3c; border-radius: 8px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(15)
        
        # Analiz Sonucu Paneli
        result_panel = ModernPanel("Analiz Sonucu", self)
        result_panel.setMinimumHeight(120)
        
        result_box = QFrame()
        result_box.setStyleSheet("""
            QFrame {
                background-color: #2a3b34;
                border-radius: 6px;
            }
        """)
        result_box.setMinimumHeight(80)
        
        result_box_layout = QVBoxLayout(result_box)
        result_box_layout.setContentsMargins(15, 10, 15, 10)
        
        # Tahmin gösterimi
        prediction_layout = QHBoxLayout()
        
        # W tahmini göstergesi (daire)
        self.prediction_indicator = QFrame()
        self.prediction_indicator.setFixedSize(50, 50)
        self.prediction_indicator.setStyleSheet("""
            QFrame {
                background-color: #6ee7b7;
                border-radius: 25px;
            }
        """)
        
        # Gösterge içindeki W/L metni
        self.prediction_text = QLabel("W")
        self.prediction_text.setAlignment(Qt.AlignCenter)
        self.prediction_text.setStyleSheet("""
            QLabel {
                color: #1a1a2e;
                font-weight: bold;
                font-size: 24px;
            }
        """)
        
        # Gösterge için layout
        indicator_layout = QVBoxLayout(self.prediction_indicator)
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        indicator_layout.addWidget(self.prediction_text)
        
        prediction_layout.addWidget(self.prediction_indicator)
        prediction_layout.addSpacing(20)
        
        # Güven seviyesi bilgileri
        confidence_info_layout = QVBoxLayout()
        
        confidence_label = QLabel("Tahmin Güveni")
        confidence_label.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        confidence_info_layout.addWidget(confidence_label)
        
        # Güven değeri ve gösterge aynı satırda
        confidence_value_layout = QHBoxLayout()
        
        # Güven çubuğu
        self.confidence_bar = QFrame()
        self.confidence_bar.setStyleSheet("""
            QFrame {
                background-color: #333345;
                border-radius: 3px;
            }
        """)
        self.confidence_bar.setFixedHeight(6)
        
        self.confidence_fill = QFrame(self.confidence_bar)
        self.confidence_fill.setStyleSheet("""
            QFrame {
                background-color: #6ee7b7;
                border-radius: 3px;
            }
        """)
        self.confidence_fill.setFixedHeight(6)
        self.confidence_fill.setFixedWidth(0)
        
        # Güven değeri
        self.confidence_label = QLabel("0%")
        self.confidence_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.confidence_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #6ee7b7; min-width: 80px;")
        
        confidence_value_layout.addWidget(self.confidence_bar, 1)  # 1 ağırlık ile esnek genişlik
        confidence_value_layout.addWidget(self.confidence_label)
        
        confidence_info_layout.addLayout(confidence_value_layout)
        prediction_layout.addLayout(confidence_info_layout, 1)  # 1 ağırlık ile esnek genişlik
        
        result_box_layout.addLayout(prediction_layout)
        
        result_panel.layout.addWidget(result_box)
        right_layout.addWidget(result_panel)
        
        # Model İstatistikleri Paneli
        stats_panel = ModernPanel("Model İstatistikleri", self)
        stats_panel.setMinimumHeight(200)  # İstatistik paneli için minimum yükseklik
        
        self.stats_table = StatsTable()
        self.stats_table.update_stats(self.model_stats)
        
        stats_panel.layout.addWidget(self.stats_table)
        right_layout.addWidget(stats_panel)
        
        # Sağ paneli ana layout'a ekle
        main_layout.addWidget(right_panel, 10)  # Önceden 1 idi, 1.0 oranı için 10:10
        
        # Ana içeriği ekle
        main_wrapper.addWidget(content_panel)
        
    def _on_cell_clicked(self, row, col):
        """Matris hücresine tıklandığında"""
        # Eğer hücre boşsa, işlem yap
        if self.matrix_data[row, col] == 0:
            # Değeri ekle ve hücreyi güncelle
            value = 1 if self.sender() == self.win_button else 2
            self._add_at_position(row, col, value)

    def _add_selection(self, value):
        """W (1) veya L (2) değerini ekler"""
        # Eğer matris doluysa, ilk satırı sil ve diğer verileri yukarı kaydır
        if 0 not in self.matrix_data:
            # İlk satırı silerek matrisi kaydır (sessizce, uyarı olmadan)
            self._shift_matrix_up()

        # Boş bir hücre bul
        for row in range(5):
            for col in range(5):
                if self.matrix_data[row, col] == 0:
                    self._add_at_position(row, col, value)
                    return

    def _shift_matrix_up(self):
        """Matrisi yukarı kaydırır, en üst satırı siler ve en alt satırı boşaltır"""
        # Matrisi bir satır yukarı kaydır
        for row in range(4):
            self.matrix_data[row] = self.matrix_data[row + 1].copy()

        # En alt satırı boşalt
        self.matrix_data[4] = np.zeros(5, dtype=int)

        # Görsel matrisi güncelle
        for row in range(5):
            for col in range(5):
                self.matrix_ui.update_cell(row, col, self.matrix_data[row, col])

        # Geçmiş verileri güncelle - artık ilk satırdan olanları sil
        new_history = []
        for hist_row, hist_col, hist_val in self.history:
            if hist_row > 0:  # İlk satırda olmayanlar
                # Satır indeksini bir azalt
                new_history.append((hist_row - 1, hist_col, hist_val))

        # Geçmişi güncelle
        self.history = new_history
    
    def _add_at_position(self, row, col, value):
        """Belirli pozisyona W veya L ekler"""
        # Eğer zaten bir tahmin yapılmışsa, onu gerçek sonuç olarak kaydet
        if self.history and len(self.history) > len(self.actual_results):
            self.actual_results.append(value)
        
        # Değeri ekle ve hücreyi güncelle
        self.matrix_data[row, col] = value
        self.matrix_ui.update_cell(row, col, value)
        
        # Geçmişe ekle
        self.history.append((row, col, value))
        
        # Matris durumunu güncelle
        self._update_matrix_status()
        
        # Butonları etkinleştir
        self.undo_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        
        # Otomatik analiz yap
        self._perform_analysis()
    
    def _update_matrix_status(self):
        """Matris durum bilgisini günceller"""
        data_count = np.sum(self.matrix_data > 0)
        required = max(0, 5 - data_count)
        
        if required > 0:
            self.matrix_status_value.setText(f"{data_count} girdi (min. {required} daha gerekli)")
            self.matrix_status_value.setStyleSheet("color: #fcd34d; font-size: 14px;")
        else:
            self.matrix_status_value.setText(f"{data_count} girdi (yeterli)")
            self.matrix_status_value.setStyleSheet("color: #6ee7b7; font-size: 14px;")
    
    def _on_undo_clicked(self):
        """Son eklenen değeri geri al"""
        if self.history:
            row, col, _ = self.history.pop()
            self.matrix_data[row, col] = 0
            self.matrix_ui.update_cell(row, col, 0)
            
            # Matris durumunu güncelle
            self._update_matrix_status()
            
            # Eğer son eklenen bir gerçek sonuçsa, onu da kaldır
            if len(self.actual_results) > 0 and len(self.history) < len(self.actual_results):
                self.actual_results.pop()
            
            # Geçmiş boşsa butonları devre dışı bırak
            if not self.history:
                self.undo_button.setEnabled(False)
                self.clear_button.setEnabled(False)
                # Analiz sonucunu temizle
                self._reset_prediction_ui()
            else:
                # Otomatik analiz yap
                self._perform_analysis()
    
    def _reset_prediction_ui(self):
        """Tahmin UI'ını sıfırlar"""
        self.prediction_indicator.setStyleSheet("QFrame { background-color: #333345; border-radius: 25px; }")
        self.prediction_text.setText("?")
        self.prediction_text.setStyleSheet("QLabel { color: #aaaaaa; font-weight: bold; font-size: 24px; }")
        self.confidence_fill.setFixedWidth(0)
        self.confidence_label.setText("0%")
        self.confidence_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #aaaaaa; min-width: 80px;")
    
    def _on_clear_clicked(self):
        """Tüm matrisi temizle"""
        self.matrix_data = np.zeros((5, 5), dtype=int)
        self.matrix_ui.clear_all()
        self.history = []
        self.actual_results = []  # Gerçek sonuçları da temizle
        
        # Matris durumunu güncelle
        self._update_matrix_status()
        
        # Model istatistiklerini sıfırla
        for model_name in self.model_stats:
            self.model_stats[model_name] = {"success_rate": 50, "correct": 0, "total": 0}
        self.stats_table.update_stats(self.model_stats)
        
        # Butonları devre dışı bırak
        self.undo_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        
        # Tahmin UI'ını sıfırla
        self._reset_prediction_ui()
    
    def _on_model_changed(self, index):
        """Model seçimi değiştiğinde"""
        model_name = self.model_combo.currentText()
        self.current_model = self.analysis_models[model_name]
        
        # Otomatik analiz yap (eğer veri varsa)
        if self.history:
            self._perform_analysis()

    def _perform_analysis(self):
        """Seçilen model ile analiz yap"""
        # Eğer yeterli veri yoksa çalıştırma
        if len(self.history) < 5:
            self._reset_prediction_ui()
            return

        # Tüm modeller için tahmin yap
        model_predictions = {}

        # Hibrit analiz hariç diğer tüm modellerin tahminlerini al
        for model_name, model in self.analysis_models.items():
            if model_name != "Hibrit Analiz":
                prediction = model.analyze(self.matrix_data, self.history)
                model_predictions[model_name] = prediction

        # Eğer bir önceki tahmin için gerçek sonuç girilmişse, başarıyı ölç
        if len(self.actual_results) > 0 and len(self.history) > len(self.actual_results):
            actual = self.actual_results[-1]

            # Önce diğer modellerin başarı oranını güncelle
            for model_name, prediction in model_predictions.items():
                # Sadece sonuç varsa ve model tahmin yapabiliyorsa hesapla
                if prediction != 0 and actual != 0:
                    self.model_stats[model_name]["total"] += 1
                    if prediction == actual:
                        self.model_stats[model_name]["correct"] += 1

                    # Başarı oranını hesapla - en az 3 tahmin yapılmışsa
                    correct = self.model_stats[model_name]["correct"]
                    total = self.model_stats[model_name]["total"]

                    if total >= 3:  # Minimum 3 tahmin yapılması gereken bir eşik
                        self.model_stats[model_name]["success_rate"] = int((correct / total) * 100)
                    else:
                        # Çok az veri varsa, henüz oran hesaplanmadı olarak işaretle
                        self.model_stats[model_name]["success_rate"] = 50  # Varsayılan değer

        # Şimdi güncellenmiş istatistiklerle Hibrit model için tahmin yap
        hibrit_confidence = 0.5
        hibrit_model = self.analysis_models["Hibrit Analiz"]
        hibrit_result = hibrit_model.analyze(self.matrix_data, self.history, self.model_stats)

        # Hibrit model artık tahminin yanında güven seviyesini de döndürsün
        if isinstance(hibrit_result, dict):
            prediction = hibrit_result.get('prediction', 0)
            hibrit_confidence = hibrit_result.get('confidence', 0.6)  # Varsayılan güven 60%
        else:
            # Eski tip dönüş için uyumluluk
            prediction = hibrit_result

            # Hibrit için güven seviyesini hesapla (en iyi 3 modelin ağırlıklı ortalaması)
            top_models = []
            for m_name, m_stat in self.model_stats.items():
                if m_name != "Hibrit Analiz" and m_name != "Karma Analiz" and m_stat["total"] >= 3:
                    top_models.append({"name": m_name, "success_rate": m_stat["success_rate"]})

            top_models = sorted(top_models, key=lambda x: x["success_rate"], reverse=True)[:3]

            # En iyi 3 modelin ortalama başarı oranı
            if top_models:
                avg_success = sum(m["success_rate"] for m in top_models) / len(top_models)
                hibrit_confidence = avg_success / 100.0  # 0-1 arası değere dönüştür
            else:
                hibrit_confidence = 0.6  # Varsayılan güven

        # Hibrit tahminini ekle
        model_predictions["Hibrit Analiz"] = prediction

        # Seçili modelin tahmini
        model_name = self.model_combo.currentText()
        result = model_predictions[model_name]

        # Şimdi de Hibrit modelin başarısını güncelle (eğer önceki tahmin için gerçek sonuç girilmişse)
        if len(self.actual_results) > 0 and len(self.history) > len(self.actual_results):
            actual = self.actual_results[-1]
            # Hibrit model tahmini için başarı oranını güncelle
            if prediction != 0 and actual != 0:
                self.model_stats["Hibrit Analiz"]["total"] += 1
                if prediction == actual:
                    self.model_stats["Hibrit Analiz"]["correct"] += 1

                # Başarı oranını hesapla - en az 3 tahmin yapılmışsa
                correct = self.model_stats["Hibrit Analiz"]["correct"]
                total = self.model_stats["Hibrit Analiz"]["total"]

                if total >= 3:  # Minimum 3 tahmin yapılması gereken bir eşik
                    self.model_stats["Hibrit Analiz"]["success_rate"] = int((correct / total) * 100)

        # İstatistik tablosunu güncelle - model tahminlerini de gönder
        self.stats_table.update_stats(self.model_stats, model_predictions)

        # Güven seviyesini hesapla
        if result != 0:
            if model_name == "Hibrit Analiz":
                # Hibrit için özel güven seviyesi hesaplaması
                confidence = hibrit_confidence
            else:
                # Diğer modeller için standart hesaplama
                total_predictions = self.model_stats[model_name]["total"]
                success_rate = self.model_stats[model_name]["success_rate"]

                # Yeterli veri yoksa veya başarı oranı çok yüksekse dikkatli ol
                if total_predictions < 5:
                    confidence = 0.5  # Çok az veri varsa orta güven seviyesi
                else:
                    confidence = success_rate / 100.0  # 0-1 arası değer
        else:
            confidence = 0.5  # Belirsiz durumlarda orta değer

        # Güven çubuğunu güncelle
        bar_width = int(self.confidence_bar.width() * confidence)
        self.confidence_fill.setFixedWidth(bar_width)
        self.confidence_label.setText(f"{int(confidence * 100)}%")

        # Sonucu göster
        if result == 1:
            self.prediction_indicator.setStyleSheet("QFrame { background-color: #6ee7b7; border-radius: 25px; }")
            self.prediction_text.setText("W")
            self.prediction_text.setStyleSheet("QLabel { color: #1a1a2e; font-weight: bold; font-size: 24px; }")
            self.confidence_fill.setStyleSheet("background-color: #6ee7b7; border-radius: 3px;")
            self.confidence_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #6ee7b7; min-width: 80px;")
        elif result == 2:
            self.prediction_indicator.setStyleSheet("QFrame { background-color: #fda4af; border-radius: 25px; }")
            self.prediction_text.setText("L")
            self.prediction_text.setStyleSheet("QLabel { color: #1a1a2e; font-weight: bold; font-size: 24px; }")
            self.confidence_fill.setStyleSheet("background-color: #fda4af; border-radius: 3px;")
            self.confidence_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #fda4af; min-width: 80px;")
        else:
            self.prediction_indicator.setStyleSheet("QFrame { background-color: #4d4a55; border-radius: 25px; }")
            self.prediction_text.setText("?")
            self.prediction_text.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; font-size: 24px; }")
            self.confidence_fill.setStyleSheet("background-color: #fcd34d; border-radius: 3px;")
            self.confidence_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #fcd34d; min-width: 80px;")
    
    def _update_model_stats(self, prediction_result):
        """Model istatistiklerini günceller (gerçek uygulamada kullanılacak)"""
        # Bu kısım gerçek uygulamada kullanılmak üzere hazırlanmıştır
        # Şu an için sadece örnek verileri gösteriyoruz
        pass
