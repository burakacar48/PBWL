#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
W ve L Pattern Analiz Uygulaması
Temel analiz model sınıfı
"""

import numpy as np
from abc import ABC, abstractmethod

class BaseAnalysisModel(ABC):
    """Tüm analiz modelleri için temel sınıf"""
    
    def __init__(self):
        self.name = "Temel Model"
        self.description = "Temel analiz modelidir. Bu model doğrudan kullanılmamalıdır."
        self.min_data_points = 5
    
    @abstractmethod
    def analyze(self, matrix, history=None):
        """
        Verilen matris ve geçmişi analiz eder
        
        Args:
            matrix (numpy.ndarray): 5x5 matris, 0=boş, 1=W, 2=L
            history (list, optional): Geçmiş hamlelerin listesi (row, col, value)
            
        Returns:
            int: Tahmin (0=belirsiz, 1=W, 2=L)
        """
        pass
    
    def _calculate_basic_stats(self, matrix):
        """Temel istatistikleri hesaplar"""
        # W ve L sayıları
        w_count = np.sum(matrix == 1)
        l_count = np.sum(matrix == 2)
        total = w_count + l_count
        
        # Boş hücre yoksa veya yeterli veri yoksa analiz yapma
        if total < self.min_data_points:
            return {
                'prediction': 0,
                'confidence': 0,
                'w_probability': 0,
                'l_probability': 0
            }
        
        # W ve L oranları
        w_ratio = w_count / total if total > 0 else 0
        l_ratio = l_count / total if total > 0 else 0
        
        # Basit olasılık tahmini
        if w_ratio > l_ratio:
            prediction = 1  # W
            confidence = w_ratio
        else:
            prediction = 2  # L
            confidence = l_ratio
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'w_probability': w_ratio,
            'l_probability': l_ratio,
            'w_count': w_count,
            'l_count': l_count,
            'total': total
        }
    
    def _convert_history_to_sequence(self, history):
        """Geçmiş hamleleri sıralı bir diziye dönüştürür"""
        if not history:
            return []
        
        sequence = []
        for _, _, value in history:
            sequence.append(value)
        
        return sequence
    
    def _find_patterns(self, sequence, pattern_length=3):
        """Belirli bir uzunluktaki tüm patternleri bulur"""
        if len(sequence) < pattern_length:
            return {}
        
        patterns = {}
        for i in range(len(sequence) - pattern_length):
            pattern = tuple(sequence[i:i+pattern_length])
            if pattern not in patterns:
                patterns[pattern] = []
            
            # Pattern sonrası gelen değeri ekle (varsa)
            if i + pattern_length < len(sequence):
                patterns[pattern].append(sequence[i+pattern_length])
        
        return patterns
    
    def _calculate_pattern_probabilities(self, patterns):
        """Her pattern için bir sonraki değerin olasılıklarını hesaplar"""
        probabilities = {}
        
        for pattern, next_values in patterns.items():
            if not next_values:
                continue
                
            w_count = next_values.count(1)
            l_count = next_values.count(2)
            total = len(next_values)
            
            w_prob = w_count / total if total > 0 else 0
            l_prob = l_count / total if total > 0 else 0
            
            probabilities[pattern] = {
                'w_probability': w_prob,
                'l_probability': l_prob,
                'count': total
            }
        
        return probabilities