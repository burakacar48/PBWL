#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Serpme Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel
import math

class ScatterAnalysis(BaseAnalysisModel):
    """Serpme analizini yapan model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Serpme Analizi"
        self.description = "Belirli bir sonucun (W veya L) matristeki dağılımını ve kümelenme seviyesini ölçerek bir sonraki sonucu tahmin eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Serpme analizini yapar
        
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
        
        # P ve B konumlarını topla
        w_positions = []
        l_positions = []
        
        for row in range(5):
            for col in range(5):
                if matrix[row, col] == 1:
                    w_positions.append((row, col))
                elif matrix[row, col] == 2:
                    l_positions.append((row, col))
        
        # Kümelenme seviyesini hesapla
        w_clustering = self._calculate_clustering(w_positions)
        l_clustering = self._calculate_clustering(l_positions)
        
        # Kümelenme eğilimine göre tahmin yap
        if w_clustering > 0.3 and l_clustering > 0.3:
            # Her iki değer de kümelenme eğiliminde
            # Son değere göre tahmin yap
            if history and history[-1][2] == 1:
                return 1  # P
            elif history and history[-1][2] == 2:
                return 2  # B
        elif w_clustering > 0.3:
            # W kümelenme eğiliminde
            return 1  # P
        elif l_clustering > 0.3:
            # L kümelenme eğiliminde
            return 2  # B
        
        # Dağılım merkezlerini hesapla
        if w_positions:
            w_center = np.mean(w_positions, axis=0)
        else:
            w_center = (2, 2)  # Merkez
            
        if l_positions:
            l_center = np.mean(l_positions, axis=0)
        else:
            l_center = (2, 2)  # Merkez
        
        # En son eklenen konumlara göre merkeze yakınlık analizi
        if history and len(history) >= 2:
            last_row, last_col, last_val = history[-1]
            if last_val == 1:
                # Son W eklendiyse, bir sonraki W tahmin et
                distance_to_w = self._calculate_distance((last_row, last_col), w_center)
                if distance_to_w < 1.5:  # Merkeze yakınsa
                    return 1  # P
                else:
                    return 2  # B
            else:
                # Son L eklendiyse, bir sonraki L tahmin et
                distance_to_l = self._calculate_distance((last_row, last_col), l_center)
                if distance_to_l < 1.5:  # Merkeze yakınsa
                    return 2  # B
                else:
                    return 1  # P
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']
    
    def _calculate_clustering(self, positions):
        """Pozisyonlar arasındaki kümelenme seviyesini hesaplar"""
        if len(positions) < 2:
            return 0
        
        # Tüm noktalar arası mesafeleri hesapla
        distances = []
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                dist = self._calculate_distance(positions[i], positions[j])
                distances.append(dist)
        
        # Ortalama mesafe
        avg_distance = np.mean(distances)
        
        # Kümelenme oranı (1'e yaklaştıkça daha fazla kümelenme var)
        # 5x5 matris için max mesafe sqrt(8) = 2.83
        clustering = 1 - (avg_distance / 2.83)
        
        return clustering
    
    def _calculate_distance(self, pos1, pos2):
        """İki nokta arasındaki Öklid mesafesini hesaplar"""
        return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)