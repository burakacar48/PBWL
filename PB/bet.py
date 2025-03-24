import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QColor, QFont

class BetProgressionCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bet İlerleme")
        self.setGeometry(300, 300, 150, 350)
        self.setFixedSize(150, 350)  # Sabit boyut
        
        # Pencereyi her zaman üstte tut
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Dark mode palette
        self.setup_dark_theme()
        
        # Bet progression
        self.bet_progression = [1000, 3000, 8000, 17000, 36000, 75000, 155000, 325000]
        self.multiplier = 2  # Default çarpan
        
        # Ana widget ve layout oluştur
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 5)
        main_layout.setSpacing(10)
        
        # Çarpan giriş alanı
        multiplier_layout = QHBoxLayout()
        multiplier_label = QLabel("Çarpan:")
        multiplier_label.setStyleSheet("color: #cccccc;")
        self.multiplier_input = QLineEdit()
        self.multiplier_input.setText(str(self.multiplier))
        self.multiplier_input.setAlignment(Qt.AlignCenter)
        self.multiplier_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                color: white;
                border: 1px solid #0078d7;
                border-radius: 2px;
                padding: 2px;
            }
        """)
        self.multiplier_input.setFixedHeight(20)
        
        multiplier_layout.addWidget(multiplier_label)
        multiplier_layout.addWidget(self.multiplier_input)
        main_layout.addLayout(multiplier_layout)
        
        # Bet miktarları listesi
        self.bet_list = QListWidget()
        self.bet_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border-radius: 2px;
                color: #0099ff;
                border: none;
            }
            QListWidget::item {
                height: 20px;
                padding-left: 5px;
            }
            QListWidget::item:alternate {
                background-color: #2d2d2d;
            }
            QListWidget::item:!alternate {
                background-color: #333333;
            }
        """)
        self.bet_list.setAlternatingRowColors(True)
        main_layout.addWidget(self.bet_list)
        
        # Toplam gereken miktar
        self.total_label = QLabel()
        self.total_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.total_label.setStyleSheet("""
            QLabel {
                background-color: #2a2a2a;
                color: #e74c3c;
                font-weight: bold;
                padding: 5px;
                border-radius: 2px;
            }
        """)
        self.total_label.setFixedHeight(30)
        main_layout.addWidget(self.total_label)
        
        # Hesapla butonu
        self.calculate_button = QPushButton("Hesapla")
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 2px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0086f0;
            }
            QPushButton:pressed {
                background-color: #006bb8;
            }
        """)
        self.calculate_button.clicked.connect(self.calculate_bets)
        main_layout.addWidget(self.calculate_button)
        
        # İlk hesaplamayı yap
        self.calculate_bets()
    
    def setup_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
        """)
    
    def calculate_bets(self):
        # Çarpanı al
        try:
            self.multiplier = float(self.multiplier_input.text())
        except ValueError:
            self.multiplier = 1
            self.multiplier_input.setText("1")
        
        # Bet listesini temizle
        self.bet_list.clear()
        
        # Çarpanlı bet miktarlarını hesapla
        calculated_bets = [amount * self.multiplier for amount in self.bet_progression]
        
        # Listeyi güncelle
        for bet in calculated_bets:
            item = QListWidgetItem(f"Rp {int(bet):,}".replace(",", "."))
            self.bet_list.addItem(item)
        
        # Toplam tutarı hesapla
        total = sum(calculated_bets)
        self.total_label.setText(f"Rp {int(total):,}".replace(",", "."))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BetProgressionCalculator()
    window.show()
    sys.exit(app.exec_())