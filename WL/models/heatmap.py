#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması
Yoğunluk Haritası Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class HeatmapAnalysis(BaseAnalysisModel):
    """Yoğunluk haritası analizini yapan model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Yoğunluk Haritası Analizi"
        self.description = "W ve L sonuçlarının matris üzerindeki yoğunluğunu ısı haritası olarak görselleştirerek yoğun bölgelerdeki değişimleri analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Yoğunluk haritası analizini yapar
        
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
        
        # W ve L yoğunluk haritaları oluştur
        w_heatmap = np.zeros((5, 5))
        l_heatmap = np.zeros((5, 5))
        
        # 3x3 pencerelerle yoğunluk hesapla
        for row in range(3):
            for col in range(3):
                window = matrix[row:row+3, col:col+3]
                
                w_count = np.sum(window == 1)
                l_count = np.sum(window == 2)
                
                # Merkez hücredeki yoğunluğu artır
                w_heatmap[row+1, col+1] += w_count / 9  # Normalize
                l_heatmap[row+1, col+1] += l_count / 9  # Normalize
        
        # Kenar hücreler için daha küçük pencereler kullan
        # Üst kenar
        for col in range(1, 4):
            window = matrix[0:2, col-1:col+2]
            w_count = np.sum(window == 1)
            l_count = np.sum(window == 2)
            w_heatmap[0, col] += w_count / 6  # Normalize
            l_heatmap[0, col] += l_count / 6  # Normalize
        
        # Alt kenar
        for col in range(1, 4):
            window = matrix[3:5, col-1:col+2]
            w_count = np.sum(window == 1)
            l_count = np.sum(window == 2)
            w_heatmap[4, col] += w_count / 6  # Normalize
            l_heatmap[4, col] += l_count / 6  # Normalize
        
        # Sol kenar
        for row in range(1, 4):
            window = matrix[row-1:row+2, 0:2]
            w_count = np.sum(window == 1)
            l_count = np.sum(window == 2)
            w_heatmap[row, 0] += w_count / 6  # Normalize
            l_heatmap[row, 0] += l_count / 6  # Normalize
        
        # Sağ kenar
        for row in range(1, 4):
            window = matrix[row-1:row+2, 3:5]
            w_count = np.sum(window == 1)
            l_count = np.sum(window == 2)
            w_heatmap[row, 4] += w_count / 6  # Normalize
            l_heatmap[row, 4] += l_count / 6  # Normalize
        
        # Köşeler için 2x2 pencere
        corners = [(0,0), (0,4), (4,0), (4,4)]
        for row, col in corners:
            r_start = max(0, row-1)
            r_end = min(5, row+2)
            c_start = max(0, col-1)
            c_end = min(5, col+2)
            
            window = matrix[r_start:r_end, c_start:c_end]
            w_count = np.sum(window == 1)
            l_count = np.sum(window == 2)
            
            window_size = (r_end-r_start) * (c_end-c_start)
            w_heatmap[row, col] += w_count / window_size  # Normalize
            l_heatmap[row, col] += l_count / window_size  # Normalize
        
        # Yoğunluk haritalarına göre tahmin
        if history and len(history) > 0:
            last_row, last_col, last_val = history[-1]
            
            # Son hamlenin çevresindeki yoğunluğa bak
            neighbors = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    
                    r, c = last_row + dr, last_col + dc
                    if 0 <= r < 5 and 0 <= c < 5 and matrix[r, c] == 0:
                        # Bu boş hücre için W ve L yoğunlukları
                        w_density = w_heatmap[r, c]
                        l_density = l_heatmap[r, c]
                        
                        if w_density > 0 or l_density > 0:
                            neighbors.append((r, c, w_density, l_density))
            
            if neighbors:
                # En yüksek yoğunluğa sahip komşuyu bul
                max_density = max(neighbors, key=lambda x: max(x[2], x[3]))
                r, c, w_dens, l_dens = max_density
                
                # Yoğunluk farkı belirgin mi?
                if abs(w_dens - l_dens) > 0.2:
                    if w_dens > l_dens:
                        return 1  # W
                    else:
                        return 2  # L
                
                # Belirgin fark yoksa, W/L alternatif olarak gelir
                if last_val == 1:
                    return 2  # W sonrası L
                else:
                    return 1  # L sonrası W
        
        # Matrisin tamamındaki yoğunluk dağılımını analiz et
        w_hotspots = np.sum(w_heatmap > 0.5)  # W yoğun bölgeler
        l_hotspots = np.sum(l_heatmap > 0.5)  # L yoğun bölgeler
        
        if w_hotspots > l_hotspots and w_hotspots >= 2:
            return 1  # W tahmini
        elif l_hotspots > w_hotspots and l_hotspots >= 2:
            return 2  # L tahmini
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']