# Smart Home Energy – Ml Projesi
Bu çalışmanın amacı, Smart Home Energy veri setinden elde edilen zaman, cihaz kullanımı ve hava durumu verilerini kullanarak toplam elektrik tüketimini tahmin 
eden bir makine öğrenmesi modeli geliştirmektir. Böylece kullanıcılar elektrik tüketimlerini daha iyi analiz edebilir ve enerji tasarrufu sağlayacak kararlar alabilir.  

## Veriseti Hakkında 
Bu projede Kaggle üzerinde paylaşılan Smart Home Energy Consumption and Weather veri seti kullanılmıştır. Veri seti; zaman bilgisi, evdeki farklı cihazların elektrik tüketimleri ve hava durumu değişkenlerini içermektedir.

## Veri Ön İşleme
Veri setindeki time sütununda bazı hatalı değerler bulunduğu için önce sayısal formata çevrilmiş ve geçersiz satırlar temizlenmiştir. Daha sonra zaman bilgisi tarih  formatına dönüştürülerek analiz için uygun hale getirilmiştir. Aynı zamanda bazı sütunlarda eksik değerler bulunduğu için bu boşluklar bir önceki geçerli değerle doldurulmuştur. Böylece veri kaybı yaşanmadan modelleme sürecine devam edilmiştir.
` python ` `
veri["time"] = pd.to_numeric(veri["time"], errors="coerce")
veri = veri.dropna(subset=["time"])
veri["time"] = pd.to_datetime(veri["time"], unit="s")

veri.fillna(method="ffill", inplace=True) ` ` `


