#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Simetri Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel

class SymmetryAnalysis(BaseAnalysisModel):
    """Simetri analizini yapan model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Simetri Analizi"
        self.description = "Matristeki sonuçların yatay, dikey veya çapraz simetri gösterip göstermediğini ve bunun sonuçları nasıl etkilediğini inceler."
        self.min_data_points = 5
    
    def analyze(self, matrix, history=None):
        """
        Simetri analizini yapar
        
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
        
        # Boş olmayan hücreleri işaretle
        non_empty = matrix > 0
        
        # Yatay simetri skoru (yatay eksene göre)
        h_sym_score = 0
        h_sym_total = 0
        
        for row in range(2):  # Sadece üst yarıyı kontrol et (orta satır hariç)
            for col in range(5):
                mirror_row = 4 - row  # Alttan ayna görüntüsü
                
                # Her iki hücre de doluysa karşılaştır
                if non_empty[row, col] and non_empty[mirror_row, col]:
                    h_sym_total += 1
                    if matrix[row, col] == matrix[mirror_row, col]:
                        h_sym_score += 1
        
        h_symmetry = h_sym_score / h_sym_total if h_sym_total > 0 else 0
        
        # Dikey simetri skoru (dikey eksene göre)
        v_sym_score = 0
        v_sym_total = 0
        
        for row in range(5):
            for col in range(2):  # Sadece sol yarıyı kontrol et (orta sütun hariç)
                mirror_col = 4 - col  # Sağdan ayna görüntüsü
                
                # Her iki hücre de doluysa karşılaştır
                if non_empty[row, col] and non_empty[row, mirror_col]:
                    v_sym_total += 1
                    if matrix[row, col] == matrix[row, mirror_col]:
                        v_sym_score += 1
        
        v_symmetry = v_sym_score / v_sym_total if v_sym_total > 0 else 0
        
        # Çapraz simetri skoru (ana köşegen ve ters köşegene göre)
        d1_sym_score = 0
        d1_sym_total = 0
        
        for i in range(2):  # Sadece köşegenin üst kısmını kontrol et (orta hariç)
            for j in range(i, 5):
                if i != j:  # Köşegendeki hücreleri hariç tut
                    # Ana köşegene göre simetri
                    if non_empty[i, j] and non_empty[j, i]:
                        d1_sym_total += 1
                        if matrix[i, j] == matrix[j, i]:
                            d1_sym_score += 1
        
        d1_symmetry = d1_sym_score / d1_sym_total if d1_sym_total > 0 else 0
        
        # Ters köşegen simetrisi
        d2_sym_score = 0
        d2_sym_total = 0
        
        for i in range(2):  # Sadece köşegenin üst kısmını kontrol et (orta hariç)
            for j in range(5-i-1):
                if i != 4-j:  # Köşegendeki hücreleri hariç tut
                    # Ters köşegene göre simetri
                    if non_empty[i, j] and non_empty[4-j, 4-i]:
                        d2_sym_total += 1
                        if matrix[i, j] == matrix[4-j, 4-i]:
                            d2_sym_score += 1
        
        d2_symmetry = d2_sym_score / d2_sym_total if d2_sym_total > 0 else 0
        
        # Genel simetri skoru
        symmetry_scores = [h_symmetry, v_symmetry, d1_symmetry, d2_symmetry]
        valid_scores = [s for s in symmetry_scores if s > 0]
        
        if valid_scores:
            overall_symmetry = sum(valid_scores) / len(valid_scores)
        else:
            overall_symmetry = 0
        
        # Simetri analizi sonuçlarına göre tahmin
        if overall_symmetry > 0.7:
            # Yüksek simetri var, simetriye göre pattern devam eder
            if history and len(history) > 0:
                last_row, last_col, last_val = history[-1]
                
                # Yatay simetri yüksekse, yatay ayna noktasına bak
                if h_symmetry > 0.6:
                    mirror_row = 4 - last_row
                    if 0 <= mirror_row < 5 and matrix[mirror_row, last_col] > 0:
                        return matrix[mirror_row, last_col]  # Ayna görüntüsü değeri
                
                # Dikey simetri yüksekse, dikey ayna noktasına bak
                if v_symmetry > 0.6:
                    mirror_col = 4 - last_col
                    if 0 <= mirror_col < 5 and matrix[last_row, mirror_col] > 0:
                        return matrix[last_row, mirror_col]  # Ayna görüntüsü değeri
                
                # Çapraz simetri yüksekse, çapraz ayna noktasına bak
                if d1_symmetry > 0.6:
                    if matrix[last_col, last_row] > 0:
                        return matrix[last_col, last_row]  # Ana köşegen ayna görüntüsü
                
                if d2_symmetry > 0.6:
                    if matrix[4-last_col, 4-last_row] > 0:
                        return matrix[4-last_col, 4-last_row]  # Ters köşegen ayna görüntüsü
        
        # Simetri kırılma eğilimi
        if 0.3 < overall_symmetry < 0.7 and history and len(history) > 0:
            # Kısmi simetri var, kırılma eğilimi olabilir
            last_val = history[-1][2]  # Son hamlenin değerini al
            if last_val == 1:
                return 2  # W sonrası L
            elif last_val == 2:
                return 1  # L sonrası W
        
        # Belirgin bir pattern yoksa genel istatistiklere göre tahmin yap
        return stats['prediction']