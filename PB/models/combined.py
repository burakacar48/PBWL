#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Karma Analiz Modeli
"""

import numpy as np
from models.base_model import BaseAnalysisModel
from models.diagonal import DiagonalAnalysis
from models.rectangle import RectangleAnalysis
from models.lshape import LShapeAnalysis
from models.tshape import TShapeAnalysis
from models.spiral import SpiralAnalysis
from models.neighborhood import NeighborhoodAnalysis
from models.zigzag import ZigzagAnalysis
from models.scatter import ScatterAnalysis
from models.quadrant import QuadrantAnalysis
from models.symmetry import SymmetryAnalysis
from models.border import BorderAnalysis
from models.heatmap import HeatmapAnalysis

class CombinedAnalysis(BaseAnalysisModel):
    """Tüm modelleri birleştiren karma model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Karma Analiz"
        self.description = "Tüm analiz modellerini birleştirerek en güvenilir tahmini yapar."
        self.min_data_points = 5
        
        # Tüm alt modelleri oluştur
        self.models = [
            DiagonalAnalysis(),
            RectangleAnalysis(),
            LShapeAnalysis(),
            TShapeAnalysis(),
            SpiralAnalysis(),
            NeighborhoodAnalysis(),
            ZigzagAnalysis(),
            ScatterAnalysis(),
            QuadrantAnalysis(),
            SymmetryAnalysis(),
            BorderAnalysis(),
            HeatmapAnalysis()
        ]
    
    def analyze(self, matrix, history=None):
        """
        Tüm modelleri kullanarak karma analiz yapar
        
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
        
        # Her modelden tahmin al
        results = {}
        for model in self.models:
            prediction = model.analyze(matrix, history)
            
            if prediction not in results:
                results[prediction] = 0
            
            results[prediction] += 1
        
        # Tahmin çoğunluğuna göre karar ver
        if 0 in results:
            del results[0]  # Belirsiz tahminleri çıkar
        
        if not results:
            return stats['prediction']  # Hiçbir model tahmin yapamadıysa genel istatistik
        
        # En çok oy alan tahmini bul
        max_votes = max(results.values())
        top_predictions = [pred for pred, votes in results.items() if votes == max_votes]
        
        if len(top_predictions) == 1:
            return top_predictions[0]  # Tekil en iyi tahmin
        else:
            # Eşit oy varsa genel istatistiklere göre karar ver
            if stats['p_probability'] > stats['b_probability']:
                return 1  # P
            else:
                return 2  # B