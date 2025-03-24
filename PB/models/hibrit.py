#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P ve B Pattern Analiz Uygulaması
Yeni Hibrit Analiz Modeli
En başarılı 3 modelin ortalamasını alır
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

class HibritAnalysis(BaseAnalysisModel):
    """En başarılı 3 modelin ortalamasını alan hibrit model"""
    
    def __init__(self):
        super().__init__()
        self.name = "Hibrit Analiz"
        self.description = "En başarılı 3 modelin tahminlerini kullanarak ortalama hesaplar."
        self.min_data_points = 5
        
        # Tüm alt modelleri oluştur
        self.models = {
            "Çapraz (Diagonal)": DiagonalAnalysis(),
            "Dikdörtgen": RectangleAnalysis(),
            "L-Şekli": LShapeAnalysis(),
            "T-Şekli": TShapeAnalysis(),
            "Spiral": SpiralAnalysis(),
            "Komşuluk": NeighborhoodAnalysis(),
            "Zig-Zag": ZigzagAnalysis(),
            "Serpme": ScatterAnalysis(),
            "Kuadran": QuadrantAnalysis(),
            "Simetri": SymmetryAnalysis(),
            "Sınır": BorderAnalysis(),
            "Isı Haritası": HeatmapAnalysis(),
        }
        
        # Minimum tahmin sayısı (bu sayıdan az olan modeller dikkate alınmaz)
        self.min_predictions = 3
    
    def analyze(self, matrix, history=None, model_stats=None):
        """
        Hibrit analiz yapar
        
        Args:
            matrix (numpy.ndarray): 5x5 matris, 0=boş, 1=W, 2=L
            history (list, optional): Geçmiş hamlelerin listesi (row, col, value)
            model_stats (dict, optional): Mevcut model istatistikleri (UI tarafından sağlanır)
            
        Returns:
            int: Tahmin (0=belirsiz, 1=W, 2=L)
        """
        # Temel istatistikler
        stats = self._calculate_basic_stats(matrix)
        
        if stats['total'] < self.min_data_points:
            return 0  # Yetersiz veri
        
        # Model istatistikleri sağlanmadıysa, veri yetersiz
        if not model_stats:
            # Varsayılan tahmin: Matristeki çoğunluğa göre
            return stats['prediction']
        
        # En başarılı 3 modeli bul
        top_models = []
        
        for model_name, model_stat in model_stats.items():
            # Hibrit modeli ve Karma modelini dahil etme
            if model_name == "Hibrit Analiz" or model_name == "Karma Analiz":
                continue
                
            # Sadece en az belirlenen sayıda tahmin yapan modelleri değerlendir
            if model_stat["total"] >= self.min_predictions:
                top_models.append({
                    "name": model_name,
                    "success_rate": model_stat["success_rate"]
                })
        
        # Başarı oranına göre sırala ve en iyi 3'ü al
        top_models = sorted(top_models, key=lambda x: x["success_rate"], reverse=True)[:3]
        
        # Hata ayıklama - hangi modellerin seçildiğini görmek için
        print("En başarılı 3 model:")
        for model in top_models:
            print(f"{model['name']}: %{model['success_rate']}")
        
        # Eğer 3 model seçilemezse, mevcut modelleri kullan
        if len(top_models) < 1:
            # Yeterli model yoksa, güven düşük
            return stats['prediction']  # Varsayılan tahmin
        
        # Top 3 modellerin tahminleri
        model_predictions = []
        
        for model_info in top_models:
            model_name = model_info["name"]
            model = self.models[model_name]
            
            # Modelin tahminini al
            prediction = model.analyze(matrix, history)
            
            # Eğer model bir tahmin yaptıysa, kaydet
            if prediction != 0:  # 0 = belirsiz tahmin, almamalıyız
                model_predictions.append({
                    "name": model_name,
                    "prediction": prediction,
                    "success_rate": model_info["success_rate"]
                })
        
        # Eğer hiçbir model tahmin yapamadıysa
        if not model_predictions:
            return stats['prediction']
            
        # Oy sayılarını hesapla
        w_votes = 0
        l_votes = 0
        w_weight = 0
        l_weight = 0
        
        # Tahminleri ve ağırlıkları topla
        for pred in model_predictions:
            success_rate = pred["success_rate"]
            if pred["prediction"] == 1:  # W
                w_votes += 1
                w_weight += success_rate
            elif pred["prediction"] == 2:  # L
                l_votes += 1
                l_weight += success_rate
        
        # Hata ayıklama
        print(f"W oyları: {w_votes}, L oyları: {l_votes}")
        print(f"W ağırlık: {w_weight}, L ağırlık: {l_weight}")
        
        # Toplam ağırlık
        total_weight = w_weight + l_weight
        
        # Sonuç ve güven seviyesi
        result = 0
        confidence = 0.5  # Varsayılan güven seviyesi
        
        # Ağırlıklı oylamaya göre tahmin
        if w_weight > l_weight:
            result = 1  # W tahmini
            confidence = w_weight / total_weight if total_weight > 0 else 0.6
        elif l_weight > w_weight:
            result = 2  # L tahmini
            confidence = l_weight / total_weight if total_weight > 0 else 0.6
        else:
            # Ağırlıklar eşitse, oy sayısına bak
            if w_votes > l_votes:
                result = 1  # W tahmini
                confidence = 0.55  # Düşük güven
            elif l_votes > w_votes:
                result = 2  # L tahmini
                confidence = 0.55  # Düşük güven
            else:
                # Her şey eşitse, genel istatistiklere göre tahmin yap
                result = stats['prediction']
                confidence = 0.5  # Belirsiz durum
        
        # Güven seviyesi ve tahmin sonucunu döndür
        return {
            'prediction': result,
            'confidence': confidence
        }