#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması
Dikdörtgen/Kare Bölge Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel
from itertools import product

class RectangleAnalysis(BaseAnalysisModel):
    """Dikdörtgen/kare bölgelerdeki patternleri analiz eden model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Dikdörtgen/Kare Bölge Analizi"
        self.description = "Matris üzerinde 2x2, 2x3, 3x2, 3x3 gibi dikdörtgen alanlar içindeki sonuçları analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Dikdörtgen bölgeleri analiz eder
        
        Args:
            matrix (numpy.ndarray): 5x5 matris, 0=boş, 1=W, 2=L
            history (list, optional): Geçmiş hamlelerin listesi (row, col, value)
            
        Returns:
            int: Tahmin (0=belirsiz, 1=W, 2=L)
        """
        # Temel istatistikler
        stats = self._calculate_basic_stats(matrix)
        
        if stats['total'] < self.min_data_points:
            return 0  # Yetersiz veri
        
        # Analiz edilecek dikdörtgen boyutları
        rectangle_sizes = [(2, 2), (2, 3), (3, 2), (3, 3)]
        
        w_weight = 0
        l_weight = 0
        total_weight = 0
        
        for rows, cols in rectangle_sizes:
            # Tüm olası başlangıç noktaları
            for i in range(6 - rows):
                for j in range(6 - cols):
                    # Dikdörtgen bölgeyi al
                    rect = matrix[i:i+rows, j:j+cols]
                    
                    # Boş olmayan hücreleri say
                    non_empty = np.sum(rect > 0)
                    
                    # Yeterli veri varsa analiz et
                    if non_empty >= 4:
                        w_count = np.sum(rect == 1)
                        l_count = np.sum(rect == 2)
                        
                        if w_count + l_count > 0:
                            # Bölgedeki W/L oranı
                            w_ratio = w_count / (w_count + l_count)
                            l_ratio = l_count / (w_count + l_count)
                            
                            # Ağırlıklı toplama ekle
                            weight = non_empty / (rows * cols)  # Doluluk oranı kadar ağırlık
                            w_weight += w_ratio * weight
                            l_weight += l_ratio * weight
                            total_weight += weight
        
        # Sonucu belirle
        if total_weight > 0:
            w_prob = w_weight / total_weight
            l_prob = l_weight / total_weight
            
            if w_prob > l_prob:
                return 1  # W tahmini
            elif l_prob > w_prob:
                return 2  # L tahmini
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']