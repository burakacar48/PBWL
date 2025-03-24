#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
T-Şekli Pattern Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class TShapeAnalysis(BaseAnalysisModel):
    """T şeklindeki patternleri analiz eden model"""
    
    def __init__(self):
        super().__init__()
        self.name = "T-Şekli Pattern Analizi"
        self.description = "Matris üzerinde T şeklinde ilerleyen sonuçları analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        T şeklindeki patternleri analiz eder
        
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
        
        # Tüm olası T şekilleri için P/B oranlarını topla
        t_shapes = []
        
        # 4 farklı yönde T şekli oluştur: ┳ ┣ ┻ ┫
        for i in range(4):
            for row in range(3):
                for col in range(3):
                    shape = []
                    if i == 0:  # ┳ şekli (yukarı T)
                        for c in range(3):
                            if matrix[row, col+c] > 0:
                                shape.append(matrix[row, col+c])
                        for r in range(1, 3):
                            if matrix[row+r, col+1] > 0:
                                shape.append(matrix[row+r, col+1])
                    elif i == 1:  # ┣ şekli (sola T)
                        for r in range(3):
                            if matrix[row+r, col] > 0:
                                shape.append(matrix[row+r, col])
                        for c in range(1, 3):
                            if matrix[row+1, col+c] > 0:
                                shape.append(matrix[row+1, col+c])
                    elif i == 2:  # ┻ şekli (aşağı T)
                        for c in range(3):
                            if matrix[row+2, col+c] > 0:
                                shape.append(matrix[row+2, col+c])
                        for r in range(2):
                            if matrix[row+r, col+1] > 0:
                                shape.append(matrix[row+r, col+1])
                    elif i == 3:  # ┫ şekli (sağa T)
                        for r in range(3):
                            if matrix[row+r, col+2] > 0:
                                shape.append(matrix[row+r, col+2])
                        for c in range(2):
                            if matrix[row+1, col+c] > 0:
                                shape.append(matrix[row+1, col+c])
                                
                    if len(shape) >= 4:  # En az 4 değer olmalı
                        t_shapes.append(shape)
        
        # T şekillerine göre tahmin yap
        p_prob = 0
        b_prob = 0
        total_shapes = 0
        
        for shape in t_shapes:
            p_count = shape.count(1)
            b_count = shape.count(2)
            total = p_count + b_count
            
            if total > 0:
                p_prob += p_count / total
                b_prob += b_count / total
                total_shapes += 1
        
        # Sonucu belirle
        if total_shapes > 0:
            p_prob /= total_shapes
            b_prob /= total_shapes
            
            if p_prob > b_prob:
                return 1  # P tahmini
            elif b_prob > p_prob:
                return 2  # B tahmini
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']