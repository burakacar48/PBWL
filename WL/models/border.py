#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması
Sınır Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class BorderAnalysis(BaseAnalysisModel):
    """Sınır analizini yapan model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Sınır Analizi"
        self.description = "Matrisin kenar ve köşelerindeki sonuçların iç kısımdan farklı olup olmadığını analiz eder."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Sınır analizini yapar
        
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
        
        # Sınır ve iç kısım maskelerini oluştur
        border_mask = np.zeros((5, 5), dtype=bool)
        border_mask[0, :] = True  # Üst kenar
        border_mask[4, :] = True  # Alt kenar
        border_mask[:, 0] = True  # Sol kenar
        border_mask[:, 4] = True  # Sağ kenar
        
        inner_mask = ~border_mask  # İç kısım (sınır olmayan yerler)
        
        # Sadece dolu hücreleri al
        non_empty = matrix > 0
        border_non_empty = border_mask & non_empty
        inner_non_empty = inner_mask & non_empty
        
        # Sınırdaki ve iç kısımdaki W/L sayıları
        border_w = np.sum((matrix == 1) & border_non_empty)
        border_l = np.sum((matrix == 2) & border_non_empty)
        inner_w = np.sum((matrix == 1) & inner_non_empty)
        inner_l = np.sum((matrix == 2) & inner_non_empty)
        
        # Oran hesapları
        border_total = border_w + border_l
        inner_total = inner_w + inner_l
        
        border_w_ratio = border_w / border_total if border_total > 0 else 0
        border_l_ratio = border_l / border_total if border_total > 0 else 0
        inner_w_ratio = inner_w / inner_total if inner_total > 0 else 0
        inner_l_ratio = inner_l / inner_total if inner_total > 0 else 0
        
        # Tahmin için faktörler
        # 1. Son hamle sınırda mı değil mi?
        if history and len(history) > 0:
            last_row, last_col, _ = history[-1]
            is_last_border = border_mask[last_row, last_col]
            
            # Sınır ile iç kısım arasında belirgin fark var mı?
            if border_total >= 3 and inner_total >= 3:
                border_inner_diff = abs(border_w_ratio - inner_w_ratio)
                
                if border_inner_diff > 0.2:  # Belirgin bir fark var
                    if is_last_border:
                        # Son hamle sınırdaysa, sınır oranlarını kullan
                        if border_w_ratio > border_l_ratio:
                            return 1  # W
                        else:
                            return 2  # L
                    else:
                        # Son hamle iç kısımdaysa, iç kısım oranlarını kullan
                        if inner_w_ratio > inner_l_ratio:
                            return 1  # W
                        else:
                            return 2  # L
            
            # Sınır içi kontrastı (köşeler vs kenarlar)
            if is_last_border:
                # Son hamle bir köşe mi?
                is_corner = (last_row == 0 or last_row == 4) and (last_col == 0 or last_col == 4)
                
                # Köşeler ve köşe dışı kenarlar için W/L hesaplama
                corners = [(0,0), (0,4), (4,0), (4,4)]
                corner_values = [matrix[r,c] for r,c in corners if matrix[r,c] > 0]
                
                edges = []
                for r in range(5):
                    for c in range(5):
                        if border_mask[r,c] and (r,c) not in corners and matrix[r,c] > 0:
                            edges.append(matrix[r,c])
                
                if corner_values and edges:
                    corner_w_ratio = corner_values.count(1) / len(corner_values)
                    edge_w_ratio = edges.count(1) / len(edges)
                    
                    if abs(corner_w_ratio - edge_w_ratio) > 0.3:  # Belirgin fark var
                        if is_corner:
                            if corner_w_ratio > corner_values.count(2) / len(corner_values):
                                return 1  # W
                            else:
                                return 2  # L
                        else:  # Kenardaysa
                            if edge_w_ratio > edges.count(2) / len(edges):
                                return 1  # W
                            else:
                                return 2  # L
        
        # Alternatif tahmin: Belirgin sınır-iç kontrast varsa
        if border_total >= 3 and inner_total >= 3:
            if abs(border_w_ratio - inner_w_ratio) > 0.3:
                # Sınır ve iç kısım ters eğilimde ise
                if (border_w_ratio > border_l_ratio and inner_w_ratio < inner_l_ratio) or \
                   (border_w_ratio < border_l_ratio and inner_w_ratio > inner_l_ratio):
                    # Son hamle sınırdaysa ve W çoğunluktaysa
                    if history and border_mask[history[-1][0], history[-1][1]]:
                        if border_w_ratio > border_l_ratio:
                            return 1  # W
                        else:
                            return 2  # L
                    # Son hamle iç kısımdaysa
                    elif history and not border_mask[history[-1][0], history[-1][1]]:
                        if inner_w_ratio > inner_l_ratio:
                            return 1  # W
                        else:
                            return 2  # L
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']