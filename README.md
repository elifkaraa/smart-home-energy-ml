# Smart Home Energy – Ml Projesi
Bu çalışmanın amacı, Smart Home Energy veri setinden elde edilen zaman, cihaz kullanımı ve hava durumu verilerini kullanarak toplam elektrik tüketimini tahmin 
eden bir makine öğrenmesi modeli geliştirmektir. Böylece kullanıcılar elektrik tüketimlerini daha iyi analiz edebilir ve enerji tasarrufu sağlayacak kararlar alabilir.  

## Veriseti Hakkında 
Bu projede Kaggle üzerinde paylaşılan Smart Home Energy Consumption and Weather veri seti kullanılmıştır. Veri seti; zaman bilgisi, evdeki farklı cihazların elektrik tüketimleri ve hava durumu değişkenlerini içermektedir.

## Veri Ön İşleme
Veri setindeki time sütununda bazı hatalı değerler bulunduğu için önce sayısal formata çevrilmiş ve geçersiz satırlar temizlenmiştir. Daha sonra zaman bilgisi tarih  formatına dönüştürülerek analiz için uygun hale getirilmiştir. Aynı zamanda bazı sütunlarda eksik değerler bulunduğu için bu boşluklar bir önceki geçerli değerle doldurulmuştur. Böylece veri kaybı yaşanmadan modelleme sürecine devam edilmiştir.  
```python  

veri["time"] = pd.to_numeric(veri["time"], errors="coerce")  
veri = veri.dropna(subset=["time"])  
veri["time"] = pd.to_datetime(veri["time"], unit="s")  

veri.fillna(method="ffill", inplace=True)    
```
## Zaman ve Cihaz Tabanlı Özellikler
Zaman bilgisinden saat, gün ve ay bilgileri çıkarılarak modelin zamanla değişen tüketim alışkanlıklarını öğrenmesi sağlanmıştır. Ayrıca evdeki tüm cihazların elektrik tüketimleri toplanarak tek bir sütun haline getirilmiştir. Son olarak, bir önceki zamandaki elektrik tüketimi modele eklenerek tahminlerin daha doğru yapılması amaçlanmıştır.   
```python
veri["hour"] = veri["time"].dt.hour
veri["dayofweek"] = veri["time"].dt.dayofweek
veri["month"] = veri["time"].dt.month

appliance_cols = [
    "Dishwasher [kW]", "Furnace 1 [kW]", "Furnace 2 [kW]",
    "Home office [kW]", "Fridge [kW]", "Wine cellar [kW]",
    "Garage door [kW]", "Kitchen 12 [kW]", "Kitchen 14 [kW]",
    "Kitchen 38 [kW]", "Barn [kW]", "Well [kW]",
    "Microwave [kW]", "Living room [kW]"
]

veri["appliance_total_kw"] = veri[appliance_cols].sum(axis=1)

veri["prev_use_kw"] = veri["use [kW]"].shift(1)
veri["prev_use_kw"].fillna(method="bfill", inplace=True)
```

## Pivot Tablolar 
Pivot tablolar, elektrik tüketiminin saat, gün, ay ve sıcaklığa göre nasıl değiştiğini görmek ve bu bilgileri modele yeni özellikler olarak eklemek için kullanılmıştır.  
Pivot tablolar sayesinde model sadece anlık verilere değil, geçmiş tüketim ortalamalarına da erişmiş ve bu durum tahmin performansını önemli ölçüde artırmıştır.  
```python

hour_pivot = veri.pivot_table(index="hour", values="use [kW]", aggfunc="mean")
veri["hour_avg_kw"] = veri["hour"].map(hour_pivot["use [kW]"])

day_pivot = veri.pivot_table(index="dayofweek", values="use [kW]", aggfunc="mean")
veri["day_avg_kw"] = veri["dayofweek"].map(day_pivot["use [kW]"])

month_pivot = veri.pivot_table(index="month", values="use [kW]", aggfunc="mean")
veri["month_avg_kw"] = veri["month"].map(month_pivot["use [kW]"])

temp_pivot = veri.pivot_table(index="temperature", values="use [kW]", aggfunc="mean")
veri["temp_avg_kw"] = veri["temperature"].map(temp_pivot["use [kW]"])  
```
## Kullanılan Modeller
#### Linear Regression

- Basit ve temel bir regresyon modelidir.

- Değişkenler arasındaki doğrusal ilişkiyi öğrenir.

- Random Forest’e kıyasla daha düşük performans göstermiştir.

#### Random Forest Regressor (Final Model)

- Doğrusal olmayan ilişkileri öğrenebilir.

- Gürültülü ve karmaşık verilerde daha kararlı sonuçlar üretir.

- Daha yüksek R² ve daha düşük hata değerleri verdiği için final model olarak seçilmiştir.

## Model Performans Karşılaştırması

| Model | R² Skoru | MAE |
|-------|----------|-----|
| Linear Regression | 0.833 | 0.135 |
| Random Forest Regressor | 0.891 | 0.093 |





