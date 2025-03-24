#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması
L-Şekli Pattern Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class LShapeAnalysis(BaseAnalysisModel):
    """L şeklindeki patternleri analiz eden model"""
    
    def __init__(self):
        super().__init__()
        self.name = "L-Şekli Pattern Analizi"
        self.description = "Matris üzerinde L şeklinde (yatay ve dikey birleşim) ilerleyen patternleri analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        L şeklindeki patternleri analiz eder
        
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
        
        # Tüm olası L şekilleri için W/L oranlarını topla
        l_shapes = []
        
        # 4 farklı yönde L şekli oluştur: ┌ ┐ └ ┘
        for i in range(4):
            for row in range(3):
                for col in range(3):
                    shape = []
                    if i == 0:  # ┌ şekli
                        for r in range(3):
                            if matrix[row+r, col] > 0:
                                shape.append(matrix[row+r, col])
                        for c in range(1, 3):
                            if matrix[row, col+c] > 0:
                                shape.append(matrix[row, col+c])
                    elif i == 1:  # ┐ şekli
                        for r in range(3):
                            if matrix[row+r, col+2] > 0:
                                shape.append(matrix[row+r, col+2])
                        for c in range(2):
                            if matrix[row, col+c] > 0:
                                shape.append(matrix[row, col+c])
                    elif i == 2:  # └ şekli
                        for r in range(3):
                            if matrix[row+r, col] > 0:
                                shape.append(matrix[row+r, col])
                        for c in range(1, 3):
                            if matrix[row+2, col+c] > 0:
                                shape.append(matrix[row+2, col+c])
                    elif i == 3:  # ┘ şekli
                        for r in range(3):
                            if matrix[row+r, col+2] > 0:
                                shape.append(matrix[row+r, col+2])
                        for c in range(2):
                            if matrix[row+2, col+c] > 0:
                                shape.append(matrix[row+2, col+c])
                                
                    if len(shape) >= 4:  # En az 4 değer olmalı
                        l_shapes.append(shape)
        
        # L şekillerine göre tahmin yap
        w_prob = 0
        l_prob = 0
        total_shapes = 0
        
        for shape in l_shapes:
            w_count = shape.count(1)
            l_count = shape.count(2)
            total = w_count + l_count
            
            if total > 0:
                w_prob += w_count / total
                l_prob += l_count / total
                total_shapes += 1
        
        # Sonucu belirle
        if total_shapes > 0:
            w_prob /= total_shapes
            l_prob /= total_shapes
            
            if w_prob > l_prob:
                return 1  # W tahmini
            elif l_prob > w_prob:
                return 2  # L tahmini
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']