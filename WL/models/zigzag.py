#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması
Zig-Zag Pattern Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class ZigzagAnalysis(BaseAnalysisModel):
    """Zig-zag patternlerini analiz eden model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Zig-Zag Pattern Analizi"
        self.description = "Matris üzerinde zig-zag şeklinde ilerleyen sonuçları inceler."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Zig-zag patternleri analiz eder
        
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
        
        # Farklı zig-zag patternleri oluştur
        zigzags = []
        
        # Yatay zigzag (soldan sağa, sağdan sola alternatif olarak)
        horizontal_zigzag = []
        for row in range(5):
            if row % 2 == 0:  # Soldan sağa
                for col in range(5):
                    if matrix[row, col] > 0:
                        horizontal_zigzag.append(matrix[row, col])
            else:  # Sağdan sola
                for col in range(4, -1, -1):
                    if matrix[row, col] > 0:
                        horizontal_zigzag.append(matrix[row, col])
        
        zigzags.append(horizontal_zigzag)
        
        # Dikey zigzag (yukarıdan aşağı, aşağıdan yukarı alternatif olarak)
        vertical_zigzag = []
        for col in range(5):
            if col % 2 == 0:  # Yukarıdan aşağı
                for row in range(5):
                    if matrix[row, col] > 0:
                        vertical_zigzag.append(matrix[row, col])
            else:  # Aşağıdan yukarı
                for row in range(4, -1, -1):
                    if matrix[row, col] > 0:
                        vertical_zigzag.append(matrix[row, col])
        
        zigzags.append(vertical_zigzag)
        
        # Çapraz zigzag (ana köşegen boyunca)
        diagonal_zigzag = []
        for i in range(5):
            if matrix[i, i] > 0:
                diagonal_zigzag.append(matrix[i, i])
        for i in range(3, -1, -1):
            if matrix[i, 4-i] > 0:
                diagonal_zigzag.append(matrix[i, 4-i])
        
        zigzags.append(diagonal_zigzag)
        
        # Her zigzag pattern için analiz yap
        best_prediction = 0
        best_confidence = 0
        
        for zigzag in zigzags:
            if len(zigzag) < 3:
                continue
            
            # Son iki elemanı pattern olarak kullan
            pattern = (zigzag[-3], zigzag[-2])
            
            # Bu pattern sonrası gelen W/L olasılıklarını hesapla
            w_count = 0
            l_count = 0
            
            for i in range(len(zigzag) - 2):
                if zigzag[i] == pattern[0] and zigzag[i+1] == pattern[1]:
                    if i+2 < len(zigzag):
                        if zigzag[i+2] == 1:
                            w_count += 1
                        elif zigzag[i+2] == 2:
                            l_count += 1
            
            # Olasılıkları hesapla
            total = w_count + l_count
            if total > 0:
                w_prob = w_count / total
                l_prob = l_count / total
                
                # En yüksek güvenle tahmini seç
                confidence = max(w_prob, l_prob)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_prediction = 1 if w_prob > l_prob else 2
        
        if best_prediction != 0:
            return best_prediction
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']