├── main.py                # Ana uygulama başlatıcısı
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py     # Ana pencere uygulaması (WLPatternAnalyzer sınıfı)
│   └── matrix_ui.py       # Matris gösterimi (MatrixUI ve CellLabel sınıfları)
│
├── core/
│   ├── __init__.py
│   └── pattern_analyzer.py  # Temel analiz fonksiyonları
│
└── models/
    ├── __init__.py
    ├── base_model.py      # BaseAnalysisModel sınıfı
    ├── diagonal.py        # DiagonalAnalysis sınıfı
    ├── rectangle.py       # RectangleAnalysis sınıfı
    ├── lshape.py          # LShapeAnalysis sınıfı
    ├── tshape.py          # TShapeAnalysis sınıfı
    ├── spiral.py          # SpiralAnalysis sınıfı
    ├── neighborhood.py    # NeighborhoodAnalysis sınıfı
    ├── zigzag.py          # ZigzagAnalysis sınıfı
    ├── scatter.py         # ScatterAnalysis sınıfı
    ├── quadrant.py        # QuadrantAnalysis sınıfı
    ├── symmetry.py        # SymmetryAnalysis sınıfı
    ├── border.py          # BorderAnalysis sınıfı
    ├── heatmap.py         # HeatmapAnalysis sınıfı
    └── combined.py        # CombinedAnalysis sınıfı
    └── hibrit.py          # HibritAnalysis sınıfı
    
    W ve L Pattern analiz yazılımı oluştur 
    
Pyqt5 kullan
Karanlık Mod 
En Modern şık bir tasarım emoji vs. kullanabilirsin
500x400 max pencere boyutu 
analiz için modeller
Çapraz (Diagonal) Pattern Analizi: 5x5 matriste sol üstten sağ alta ve sağ üstten sol alta çapraz olarak ilerleyen patternleri analiz eder.
Dikdörtgen/Kare Bölge Analizi: Matris üzerinde 2x2, 2x3, 3x2, 3x3 gibi dikdörtgen alanlar içindeki sonuçların bir pattern olarak analiz edilmesi.
L-Şekli Pattern Analizi: Matris üzerinde L şeklinde (yatay ve dikey birleşim) ilerleyen satır ve sütunlardaki patternleri analiz eder.
T-Şekli Pattern Analizi: Matris üzerinde T şeklinde ilerleyen sonuçların analiz edilmesi.
Spiral Pattern Analizi: Matrisin merkezinden dışa doğru veya dıştan merkeze doğru spiral şeklinde ilerleyen sonuçları inceler.
Komşuluk Pattern Analizi: Bir hücrenin 8 komşusu içinde W veya L oranının bir sonraki sonucu nasıl etkilediğini analiz eder.
Zig-Zag Pattern Analizi: Matris üzerinde zig-zag şeklinde ilerleyen sonuçların incelenmesi.
Serpme Analizi: Belirli bir sonucun (W veya L) matristeki dağılımını ve kümelenme seviyesini ölçerek bir sonraki sonucu tahmin eder.
Kuadran Analizi: Matrisi 4 eşit parçaya bölerek her bölgedeki W/L oranının diğer bölgelere göre nasıl değiştiğini inceler.
Simetri Analizi: Matristeki sonuçların yatay, dikey veya çapraz simetri gösterip göstermediğini ve bunun bir sonraki sonucu nasıl etkilediğini inceler.
Sınır Analizi: Matrisin kenar ve köşelerindeki sonuçların iç kısımdan farklı olup olmadığını analiz eder.
Yoğunluk Haritası Analizi: W ve L sonuçlarının matris üzerindeki yoğunluğunu ısı haritası olarak görselleştirerek yoğun bölgelerdeki değişimleri analiz eder.
Bu kod, bir baccarat oyununda kazanma/kaybetme örüntülerini analiz eden ve tahminlerde bulunan bir arayüz uygulamasıdır. Uygulamada üç ana tahmin modeli ve bir karma model bulunmaktadır:
Pattern Analysis (Örüntü Analizi):
Geçmiş sonuçların belirli uzunluktaki dizilerini analiz eder
Belirli bir örüntünün ardından ne geldiğini takip edip istatistik oluşturur
Örneğin "WWLWL" örüntüsünden sonra çoğunlukla "W" geliyorsa, bu örüntüyü tekrar gördüğünde "W" tahmininde bulunur
Kullanıcının belirlediği maksimum örüntü uzunluğuna göre çalışır (3-7 arası)
Matrix Analysis (Matris Analizi):
Sonuçları 5x5'lik bir matrise yerleştirir
Yatay ve dikey satırlardaki örüntüleri analiz eder
Matristeki belirli pozisyonların tahmin güçlerini hesaplar
En az 25 sonuç gerektirir
Adaptive Analysis (Uyarlanabilir Analiz):
Farklı pencere boyutlarında (10, 20, 50) trendleri analiz eder
Üç trend tipini tanımlar: "Yukselis" (Yükseliş), "Dusus" (Düşüş) ve "Denge" (Denge)
Trend tiplerinin sonraki sonuçları nasıl etkilediğini hesaplar
Ağırlıklı bir kombinasyon kullanarak tahmin yapar
En az 20 sonuç gerektirir
Combined Analysis (Karma Analiz):
Yukarıdaki üç modelin sonuçlarını birleştirir
Her modelden gelen tahminlerin olasılıklarını karşılaştırır
En yüksek olasılığa ve örnek sayısına sahip tahmini seçer
Hibrit Model:
1. Dinamik Model Ağırlıklandırma

Öğrenme Temelli Ağırlıklandırma: Her modelin geçmiş performansını takip ederek, doğru tahminler yapan modellerin ağırlıklarını zaman içinde artırın.
Bağlam Temelli Ağırlıklandırma: Belirli durumlarda daha iyi performans gösteren modelleri tespit edin. Örneğin, bazı modeller belirli desenlerde (örn. W yoğunluğu yüksek olduğunda) daha iyi çalışabilir.
Küme Temelli Ağırlıklandırma: Benzer tahminleri yapan modelleri gruplandırın, böylece çoğunluğa uymayan modellerden daha düşük etkilenirsiniz.

2. Farklı Birleştirme Stratejileri

Çoğunluk Oylaması: En basit yöntem, her modelin bir oyu olduğunu varsayarak en çok oy alan tahmini seçmektir.
Ağırlıklı Oylama: Her modelin oyunun, modelin güven düzeyiyle ağırlıklandırılmasıdır.
Bayes Birleştirmesi: Modellerin tahminlerini Bayes teoremi kullanarak birleştirin. Bu, her modelin hata oranlarını ve güvenilirliğini hesaba katmanızı sağlar.
Stacking (Meta-Öğrenme): Modellerin tahminlerini bir meta-modele girdi olarak kullanarak daha yüksek seviyede bir tahmin yapın.

3. Güven Seviyesi Kalibrasyonu

Model Güvenini Normalleştirme: Bazı modeller yapısal olarak daha yüksek güven seviyeleri rapor edebilir. Güven seviyelerini her model için normalleştirin veya kalibre edin.
Güven Eşikleri: Yalnızca belirli bir güven eşiğinin üzerindeki tahminleri hesaba katın.

4. Örüntü Durumu Tespiti

Trend Analizi: Mevcut verilerde bir trend olup olmadığını tespit edip, trende göre model ağırlıklarını ayarlayın.
Volatilite Analizi: Sonuçların istikrarlı mı yoksa değişken mi olduğunu tespit edin ve buna göre farklı modelleri öne çıkarın.

5. Zaman Penceresi Analizi

Son Sonuçlara Ağırlık Verme: En yakın geçmişteki sonuçlara daha yüksek ağırlık verin.
Pencere Temelli Analiz: Farklı büyüklükteki zaman pencerelerini analiz ederek kısa vadeli ve uzun vadeli desenleri tespit edin.

6. Özel Durum Tespiti ve İşleme

İstisna Durumları: Sıra dışı örüntüleri tespit edip özel işlem uygulayın.
Dalgalanma Tespiti: Sonuçlarda normal olmayan dalgalanmaları tespit edin ve buna uygun modellere daha fazla ağırlık verin.

7. Geribildirim Döngüsü

Sürekli Öğrenme: Her yeni sonuç geldiğinde model ağırlıklarını güncelleyin.
Periyodik Yeniden Kalibrasyon: Belirli aralıklarla tüm model ağırlıklarını yeniden değerlendirin.

8. Eşleşme Analizi

Şablon Eşleştirme: Mevcut durumu geçmişteki benzer durumlara eşleştirerek hangi modelin bu durumlarda daha iyi performans gösterdiğini belirleyin.
Sekans Analizi: Son birkaç sonucu bir sekans olarak ele alın ve benzer sekansların sonuçlarını analiz edin.

Hibrit Model Örnek Uygulaması
İdeal bir hibrit model şu şekilde çalışabilir:

Her model kendi tahminini ve güven seviyesini üretir
Model güvenleri model geçmiş performansına göre kalibre edilir
Mevcut duruma benzer geçmiş durumlar tespit edilir
Mevcut durumda daha iyi performans göstermiş modellere daha yüksek ağırlık verilir
Ağırlıklı bir oylama sistemi ile nihai tahmin oluşturulur
Sonuç geldiğinde, her modelin performansı değerlendirilir ve ağırlıklar güncellenir

Uygulamayı oluşturduktan sonra bütün py dosylarını isimleri ile paylaş takip etmem kolay olsun