#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Komşuluk Pattern Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class NeighborhoodAnalysis(BaseAnalysisModel):
    """Komşuluk patternlerini analiz eden model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Komşuluk Pattern Analizi"
        self.description = "Bir hücrenin 8 komşusu içinde W veya L oranının bir sonraki sonucu nasıl etkilediğini analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Komşuluk patternlerini analiz eder
        
        Args:
            matrix (numpy.ndarray): 5x5 matris, 0=boş, 1=W, 2=L
            history (list, optional): Geçmiş hamlelerin listesi (row, col, value)
            
        Returns:
            int: Tahmin (0=belirsiz, 1=W, 2=L)
        """
        # Temel istatistikler
        stats = self._calculate_basic_stats(matrix)
        
        if stats['total'] < self.min_data_points or not history:
            return 0  # Yetersiz veri
        
        # Komşuluk oranlarına göre tahmin yapma
        neighborhood_stats = {}
        
        # 8 komşuluktaki P/B oranları
        for row in range(5):
            for col in range(5):
                if matrix[row, col] > 0:
                    # Bu hücrenin komşularını bul
                    neighbors = []
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Hücrenin kendisi
                            
                            r, c = row + dr, col + dc
                            if 0 <= r < 5 and 0 <= c < 5 and matrix[r, c] > 0:
                                neighbors.append(matrix[r, c])
                    
                    if neighbors:
                        # Komşuluktaki P/B oranı
                        p_ratio = neighbors.count(1) / len(neighbors)
                        b_ratio = neighbors.count(2) / len(neighbors)
                        
                        # Bu orana sahip komşuluklar için istatistik tut
                        key = (round(p_ratio, 2), round(b_ratio, 2))
                        if key not in neighborhood_stats:
                            neighborhood_stats[key] = {'w': 0, 'l': 0}
                        
                        # Merkez hücrenin değerini ekle
                        if matrix[row, col] == 1:
                            neighborhood_stats[key]['w'] += 1
                        else:
                            neighborhood_stats[key]['l'] += 1
        
        # Son eklenen hücrenin komşuluğunu analiz et
        if history:
            last_row, last_col, _ = history[-1]
            
            # Boş bir komşuluk bul
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    
                    r, c = last_row + dr, last_col + dc
                    if 0 <= r < 5 and 0 <= c < 5 and matrix[r, c] == 0:
                        # Bu boş hücrenin komşularını bul
                        neighbors = []
                        for d2r in [-1, 0, 1]:
                            for d2c in [-1, 0, 1]:
                                if d2r == 0 and d2c == 0:
                                    continue
                                
                                r2, c2 = r + d2r, c + d2c
                                if 0 <= r2 < 5 and 0 <= c2 < 5 and matrix[r2, c2] > 0:
                                    neighbors.append(matrix[r2, c2])
                        
                        if neighbors:
                            # Komşuluktaki P/B oranı
                            p_ratio = neighbors.count(1) / len(neighbors)
                            b_ratio = neighbors.count(2) / len(neighbors)
                            
                            key = (round(p_ratio, 2), round(b_ratio, 2))
                            if key in neighborhood_stats:
                                # Bu komşuluk oranında daha önce ne görülmüş?
                                p_count = neighborhood_stats[key]['w']
                                b_count = neighborhood_stats[key]['l']
                                
                                if p_count + b_count > 0:
                                    if p_count > b_count:
                                        return 1  # P tahmini
                                    elif b_count > p_count:
                                        return 2  # B tahmini
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']