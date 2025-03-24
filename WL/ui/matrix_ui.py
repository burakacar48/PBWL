#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması - Modern UI
Matris gösterimi sınıfları
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter, QBrush, QPen

class CellLabel(QFrame):
    """Modern matris hücresi"""
    
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Görüntü ayarları - hücre boyutunu küçülttük
        self.setFixedSize(30, 30)
        self.setCursor(Qt.PointingHandCursor)
        
        # Varsayılan olarak boş hücre
        self.value = 0
        self._glow_opacity = 0.0  # Özel değişken olarak tanımla
        
        # Hover için stil
        self.setMouseTracking(True)
        
        # Animasyon
        self.glow_animation = QPropertyAnimation(self, b"glow_opacity")
        self.glow_animation.setDuration(300)
        self.glow_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def setValue(self, value):
        """Hücre değerini ayarla (0: Boş, 1: W, 2: L)"""
        old_value = self.value
        self.value = value
        
        # Sadece değişim varsa animasyon başlat
        if old_value != value:
            if value > 0:
                self.glow_animation.setStartValue(0.0)
                self.glow_animation.setEndValue(1.0)
                self.glow_animation.start()
            
        self.update()
    
    def mousePressEvent(self, event):
        """Tıklama olayını yakala"""
        self.clicked.emit()
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        """Fare hücrenin üzerine geldiğinde"""
        if self.value == 0:  # Sadece boş hücrelerin üzerindeyken hover efekti
            self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Fare hücreden ayrıldığında"""
        if self.value == 0:  # Sadece boş hücrelerin hover efektini sıfırla
            self.update()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        """Hücreyi çiz"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Hücre arka planı
        if self.value == 0:
            # Boş hücre
            if self.underMouse():
                painter.setBrush(QBrush(QColor("#3d3d54")))
            else:
                painter.setBrush(QBrush(QColor("#333345")))
        elif self.value == 1:
            # W hücresi
            painter.setBrush(QBrush(QColor("#6ee7b7")))
        else:
            # L hücresi
            painter.setBrush(QBrush(QColor("#fda4af")))
        
        # Kenar çizgisi
        painter.setPen(QPen(QColor("#444455"), 1))
        
        # Yuvarlatılmış dikdörtgen çiz
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 4, 4)
        
        # Parıltı efekti (W veya L için)
        if self.value > 0 and self._glow_opacity > 0:
            glowColor = QColor("#6ee7b7" if self.value == 1 else "#fda4af")
            glowColor.setAlphaF(self._glow_opacity * 0.3)  # Yarı-saydam parıltı
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(glowColor))
            painter.drawRoundedRect(-3, -3, self.width() + 6, self.height() + 6, 5, 5)
        
        # W veya L metnini çiz
        if self.value > 0:
            painter.setPen(QPen(QColor("#333333"), 1))
            font = QFont("Arial", 12, QFont.Bold)  # Font boyutunu küçülttük
            painter.setFont(font)
            text = "W" if self.value == 1 else "L"
            painter.drawText(self.rect(), Qt.AlignCenter, text)
    
    def get_glow_opacity(self):
        return self._glow_opacity
    
    def set_glow_opacity(self, opacity):
        self._glow_opacity = opacity  # Özel değişkeni güncelle
        self.update()
    
    glow_opacity = pyqtProperty(float, get_glow_opacity, set_glow_opacity)

class MatrixUI(QFrame):
    """5x5 Matris gösterimi"""
    
    cell_clicked = pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Görünüm ayarları - boyutları yarı yarıya düşürdük
        self.setMinimumSize(170, 170)
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border-radius: 8px;
            }
        """)
        
        # Grid layout oluştur
        layout = QGridLayout(self)
        layout.setSpacing(5)  # Hücreler arası boşluk
        
        # İlk satıra sütun indekslerini ekle
        for col in range(5):
            index_label = QLabel(str(col+1))
            index_label.setAlignment(Qt.AlignCenter)
            index_label.setStyleSheet("color: #aaaaaa; font-weight: bold; font-size: 12px;")
            layout.addWidget(index_label, 0, col+1)
        
        # Satır indekslerini ekle
        for row in range(5):
            index_label = QLabel(str(row+1))
            index_label.setAlignment(Qt.AlignCenter)
            index_label.setStyleSheet("color: #aaaaaa; font-weight: bold; font-size: 12px;")
            layout.addWidget(index_label, row+1, 0)
        
        # Hücre etiketlerini oluştur
        self.cells = []
        for row in range(5):
            row_cells = []
            for col in range(5):
                cell = CellLabel()
                cell.clicked.connect(lambda r=row, c=col: self.cell_clicked.emit(r, c))
                layout.addWidget(cell, row+1, col+1)  # İndeksler için kaydırılmış
                row_cells.append(cell)
            self.cells.append(row_cells)
    
    def update_cell(self, row, col, value):
        """Belirli bir hücrenin değerini güncelle"""
        self.cells[row][col].setValue(value)
    
    def clear_all(self):
        """Tüm hücreleri temizle"""
        for row in range(5):
            for col in range(5):
                self.cells[row][col].setValue(0)
