#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Spiral Pattern Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class SpiralAnalysis(BaseAnalysisModel):
    """Spiral şeklindeki patternleri analiz eden model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Spiral Pattern Analizi"
        self.description = "Matriste dıştan içe veya içten dışa spiral şeklinde ilerleyen sonuçları analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Spiral patternleri analiz eder
        
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
        
        # Dıştan içe doğru spiral oluştur
        spiral_outside_in = []
        
        n = 5  # 5x5 matris
        row_start, col_start = 0, 0
        row_end, col_end = n-1, n-1
        
        while row_start <= row_end and col_start <= col_end:
            # Üst satır
            for i in range(col_start, col_end + 1):
                if matrix[row_start, i] > 0:
                    spiral_outside_in.append(matrix[row_start, i])
            row_start += 1
            
            # Sağ sütun
            for i in range(row_start, row_end + 1):
                if matrix[i, col_end] > 0:
                    spiral_outside_in.append(matrix[i, col_end])
            col_end -= 1
            
            # Alt satır
            if row_start <= row_end:
                for i in range(col_end, col_start - 1, -1):
                    if matrix[row_end, i] > 0:
                        spiral_outside_in.append(matrix[row_end, i])
                row_end -= 1
            
            # Sol sütun
            if col_start <= col_end:
                for i in range(row_end, row_start - 1, -1):
                    if matrix[i, col_start] > 0:
                        spiral_outside_in.append(matrix[i, col_start])
                col_start += 1
        
        # İçten dışa doğru spiral (dıştan içe spirali ters çevirerek elde edilir)
        spiral_inside_out = spiral_outside_in[::-1]
        
        # Her iki spiral için pattern analizi yap
        spirals = [spiral_outside_in, spiral_inside_out]
        
        best_prediction = 0
        best_confidence = 0
        
        for spiral in spirals:
            if len(spiral) < 3:
                continue
            
            # Son iki elemanı pattern olarak kullan
            pattern = (spiral[-3], spiral[-2])
            
            # Bu pattern sonrası gelen P/B olasılıklarını hesapla
            p_count = 0
            b_count = 0
            
            for i in range(len(spiral) - 2):
                if spiral[i] == pattern[0] and spiral[i+1] == pattern[1]:
                    if i+2 < len(spiral):
                        if spiral[i+2] == 1:
                            p_count += 1
                        elif spiral[i+2] == 2:
                            b_count += 1
            
            # Olasılıkları hesapla
            total = p_count + b_count
            if total > 0:
                p_prob = p_count / total
                b_prob = b_count / total
                
                # En yüksek güvenle tahmini seç
                confidence = max(p_prob, b_prob)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_prediction = 1 if p_prob > b_prob else 2
        
        if best_prediction != 0:
            return best_prediction
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']