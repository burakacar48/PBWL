#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Temel analiz fonksiyonları
"""

import numpy as np
from collections import Counter

def analyze_pattern(matrix, pattern_type, params=None):
    """
    Belirtilen pattern tipine göre analiz yapar
    
    Args:
        matrix (numpy.ndarray): 5x5 matris, 0=boş, 1=W, 2=L
        pattern_type (str): Analiz edilecek pattern tipi
        params (dict, optional): Ek parametreler
        
    Returns:
        dict: Analiz sonuçları
    """
    if params is None:
        params = {}
    
    # Matristeki P ve B sayıları
    p_count = np.sum(matrix == 1)
    b_count = np.sum(matrix == 2)
    total = p_count + b_count
    
    # Boş hücre yoksa veya yeterli veri yoksa analiz yapma
    if total < 5 or np.sum(matrix == 0) == 0:
        return {
            'prediction': 0,
            'confidence': 0,
            'p_probability': 0,
            'b_probability': 0
        }
    
    # P ve B oranları
    p_ratio = p_count / total if total > 0 else 0
    b_ratio = b_count / total if total > 0 else 0
    
    # Basit olasılık tahmini (varsayılan)
    if p_ratio > b_ratio:
        prediction = 1  # W
        confidence = p_ratio
    else:
        prediction = 2  # L
        confidence = b_ratio
    
    return {
        'prediction': prediction,
        'confidence': confidence,
        'p_probability': p_ratio,
        'b_probability': b_ratio,
        'p_count': p_count,
        'b_count': b_count,
        'total': total
    }

def get_rop_patterns(matrix):
    """Matristeki yatay satır patternlerini çıkarır"""
    patterns = []
    for row in range(5):
        for col in range(3):  # 3 uzunluğunda patternler için
            pattern = []
            for i in range(3):
                if matrix[row, col + i] > 0:  # Boş olmayan hücreler
                    pattern.append(matrix[row, col + i])
            if len(pattern) == 3:  # Tam patternler
                patterns.append(pattern)
    return patterns

def get_cob_patterns(matrix):
    """Matristeki dikey sütun patternlerini çıkarır"""
    patterns = []
    for col in range(5):
        for row in range(3):  # 3 uzunluğunda patternler için
            pattern = []
            for i in range(3):
                if matrix[row + i, col] > 0:  # Boş olmayan hücreler
                    pattern.append(matrix[row + i, col])
            if len(pattern) == 3:  # Tam patternler
                patterns.append(pattern)
    return patterns

def get_diagonab_patterns(matrix):
    """Matristeki çapraz patternleri çıkarır"""
    patterns = []
    
    # Sol üstten sağ alta
    for i in range(3):
        for j in range(3):
            pattern = []
            for k in range(3):
                if matrix[i + k, j + k] > 0:
                    pattern.append(matrix[i + k, j + k])
            if len(pattern) == 3:
                patterns.append(pattern)
    
    # Sağ üstten sol alta
    for i in range(3):
        for j in range(2, 5):
            pattern = []
            for k in range(3):
                if matrix[i + k, j - k] > 0:
                    pattern.append(matrix[i + k, j - k])
            if len(pattern) == 3:
                patterns.append(pattern)
    
    return patterns

def get_neighbors(matrix, row, col):
    """Belirli bir hücrenin komşularını döndürür"""
    neighbors = []
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 5 and 0 <= c < 5 and matrix[r, c] > 0:
            neighbors.append(matrix[r, c])
    
    return neighbors

def count_pattern_occurrence(patterns, pattern_to_find):
    """Belirli bir patternin kaç kez geçtiğini sayar"""
    count = 0
    for pattern in patterns:
        if pattern == pattern_to_find:
            count += 1
    return count

def get_pattern_probabilities(patterns):
    """Pattern sonrası olasılıkları hesaplar"""
    # İki elemanlı patternler için sonra gelen değerleri tut
    pattern_next = {}
    
    for pattern in patterns:
        if len(pattern) >= 3:
            key = (pattern[0], pattern[1])
            if key not in pattern_next:
                pattern_next[key] = []
            pattern_next[key].append(pattern[2])
    
    # Her pattern için olasılıkları hesapla
    probabilities = {}
    for key, values in pattern_next.items():
        count = Counter(values)
        total = len(values)
        p_prob = count.get(1, 0) / total if total > 0 else 0
        b_prob = count.get(2, 0) / total if total > 0 else 0
        probabilities[key] = {
            'p_prob': p_prob, 
            'b_prob': b_prob,
            'count': total
        }
    
    return probabilities