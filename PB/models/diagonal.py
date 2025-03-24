#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
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
        
        # Her çapraz için P/B oranını kontrol et
        p_prob = 0
        b_prob = 0
        totab_patterns = 0
        
        for diagonal in diagonals:
            if len(diagonal) >= 3:  # En az 3 uzunluğunda patternler
                values = [v for v in diagonal if v > 0]  # Boş olmayanlar
                
                if len(values) >= 3:
                    p_count = values.count(1)
                    b_count = values.count(2)
                    
                    # Son iki değere göre tahmin yap
                    if len(values) >= 3 and values[-3] > 0 and values[-2] > 0:
                        pattern = (values[-3], values[-2])
                        
                        # Bu pattern önceden kaç kez P/B ile devam etmiş
                        p_pattern = 0
                        b_pattern = 0
                        
                        for i in range(len(values) - 2):
                            if values[i] == pattern[0] and values[i+1] == pattern[1]:
                                if i+2 < len(values):
                                    if values[i+2] == 1:
                                        p_pattern += 1
                                    elif values[i+2] == 2:
                                        b_pattern += 1
                        
                        if p_pattern + b_pattern > 0:
                            p_prob += p_pattern / (p_pattern + b_pattern)
                            b_prob += b_pattern / (p_pattern + b_pattern)
                            totab_patterns += 1
        
        # Sonucu belirle
        if totab_patterns > 0:
            p_prob /= totab_patterns
            b_prob /= totab_patterns
            
            if p_prob > b_prob:
                return 1  # P tahmini
            elif b_prob > p_prob:
                return 2  # B tahmini
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']