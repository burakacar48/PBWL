#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Kuadran Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class QuadrantAnalysis(BaseAnalysisModel):
    """Kuadran analizini yapan model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Kuadran Analizi"
        self.description = "Matrisi 4 eşit parçaya bölerek her bölgedeki P/B oranının diğer bölgelere göre nasıl değiştiğini inceler."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Kuadran analizini yapar
        
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
        
        # Matrisi 4 kuadranta böl
        # Q1: Sol üst, Q2: Sağ üst, Q3: Sol alt, Q4: Sağ alt
        q1 = matrix[0:3, 0:3]
        q2 = matrix[0:3, 2:5]
        q3 = matrix[2:5, 0:3]
        q4 = matrix[2:5, 2:5]
        
        # Her kuadranttaki P ve B sayılarını hesapla
        quadrants = [q1, q2, q3, q4]
        quadrant_stats = []
        
        for i, q in enumerate(quadrants):
            p_count = np.sum(q == 1)
            b_count = np.sum(q == 2)
            total = p_count + b_count
            
            if total > 0:
                p_ratio = p_count / total
                b_ratio = b_count / total
                
                quadrant_stats.append({
                    'quadrant': i+1,
                    'p_count': p_count,
                    'b_count': b_count,
                    'total': total,
                    'p_ratio': p_ratio,
                    'b_ratio': b_ratio
                })
            else:
                quadrant_stats.append({
                    'quadrant': i+1,
                    'p_count': 0,
                    'b_count': 0,
                    'total': 0,
                    'p_ratio': 0,
                    'b_ratio': 0
                })
        
        # Son eklenen konum hangi kuadranda?
        if history:
            last_row, last_col, _ = history[-1]
            last_quadrant = 0
            
            if last_row < 3 and last_col < 3:
                last_quadrant = 1  # Q1
            elif last_row < 3 and last_col >= 2:
                last_quadrant = 2  # Q2
            elif last_row >= 2 and last_col < 3:
                last_quadrant = 3  # Q3
            else:
                last_quadrant = 4  # Q4
            
            # Son kuadranda P/B oranlarına bakarak tahmin yap
            last_q_stats = quadrant_stats[last_quadrant-1]
            
            if last_q_stats['total'] >= 3:
                if last_q_stats['p_ratio'] > last_q_stats['b_ratio']:
                    return 1  # P
                elif last_q_stats['b_ratio'] > last_q_stats['p_ratio']:
                    return 2  # B
            
            # Kuadranlar arası karşılaştırma
            # En yüksek ve en düşük oranlı kuadranları bul
            valid_quadrants = [q for q in quadrant_stats if q['total'] > 0]
            if valid_quadrants:
                max_p_ratio = max(valid_quadrants, key=lambda x: x['p_ratio'])
                max_b_ratio = max(valid_quadrants, key=lambda x: x['b_ratio'])
                
                # Son kuadran maksimum W oranına sahipse
                if last_quadrant == max_p_ratio['quadrant'] and max_p_ratio['p_ratio'] > 0.6:
                    return 1  # P
                
                # Son kuadran maksimum L oranına sahipse
                if last_quadrant == max_b_ratio['quadrant'] and max_b_ratio['b_ratio'] > 0.6:
                    return 2  # B
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']