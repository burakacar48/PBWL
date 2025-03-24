#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması
Çapraz (Diagonal) Pattern Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class DiagonalAnalysis(BaseAnalysisModel):
    """Çapraz patternleri analiz eden model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Çapraz (Diagonal) Pattern Analizi"
        self.description = "5x5 matriste sol üstten sağ alta ve sağ üstten sol alta çapraz olarak ilerleyen patternleri analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Çapraz patternleri analiz eder
        
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
        
        # Çapraz patternleri topla
        diagonals = []
        
        # Ana köşegen ve paralelleri (sol üst - sağ alt)
        for offset in range(-4, 5):
            diagonal = np.diag(matrix, offset)
            diagonals.append(diagonal)
        
        # Ters köşegen ve paralelleri (sağ üst - sol alt)
        flipped = np.fliplr(matrix)
        for offset in range(-4, 5):
            diagonal = np.diag(flipped, offset)
            diagonals.append(diagonal)
        
        # Her çapraz için W/L oranını kontrol et
        w_prob = 0
        l_prob = 0
        total_patterns = 0
        
        for diagonal in diagonals:
            if len(diagonal) >= 3:  # En az 3 uzunluğunda patternler
                values = [v for v in diagonal if v > 0]  # Boş olmayanlar
                
                if len(values) >= 3:
                    w_count = values.count(1)
                    l_count = values.count(2)
                    
                    # Son iki değere göre tahmin yap
                    if len(values) >= 3 and values[-3] > 0 and values[-2] > 0:
                        pattern = (values[-3], values[-2])
                        
                        # Bu pattern önceden kaç kez W/L ile devam etmiş
                        w_pattern = 0
                        l_pattern = 0
                        
                        for i in range(len(values) - 2):
                            if values[i] == pattern[0] and values[i+1] == pattern[1]:
                                if i+2 < len(values):
                                    if values[i+2] == 1:
                                        w_pattern += 1
                                    elif values[i+2] == 2:
                                        l_pattern += 1
                        
                        if w_pattern + l_pattern > 0:
                            w_prob += w_pattern / (w_pattern + l_pattern)
                            l_prob += l_pattern / (w_pattern + l_pattern)
                            total_patterns += 1
        
        # Sonucu belirle
        if total_patterns > 0:
            w_prob /= total_patterns
            l_prob /= total_patterns
            
            if w_prob > l_prob:
                return 1  # W tahmini
            elif l_prob > w_prob:
                return 2  # L tahmini
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']