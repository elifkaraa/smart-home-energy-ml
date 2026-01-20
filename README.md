# Smart Home Energy – Ml Projesi
Bu proje, evdeki cihazların elektrik kullanımını ve hava durumunu kullanarak toplam elektrik tüketimini tahmin etmeyi amaçlıyor. Böylece kullanıcılar elektrik kullanımını anlayıp tasarruf edebilir. 

## Veriseti Hakkında 
Kaggle’daki Smart Home Energy ve Weather veri seti kullanıldı. İçinde zaman bilgisi, cihaz tüketimleri ve hava durumu var.

## Veri Ön İşleme
- Hatalı zaman değerleri düzeltildi ve eksik veriler bir önceki değerle dolduruldu.

- Saat, gün ve ay bilgileri çıkarıldı.

- Cihazların toplam tüketimi ve bir önceki zamanın tüketimi eklendi.  
```python  

veri["time"] = pd.to_numeric(veri["time"], errors="coerce")  
veri = veri.dropna(subset=["time"])  
veri["time"] = pd.to_datetime(veri["time"], unit="s")  

veri.fillna(method="ffill", inplace=True)    
```
## Zaman ve Cihaz Tabanlı Özellikler
Zaman bilgisinden saat, gün ve ay çıkarıldı, böylece modelin zamanla değişen tüketim alışkanlıklarını öğrenmesi sağlandı. Evdeki tüm cihazların elektrik tüketimi toplanıp tek sütun yapıldı ve bir önceki zamandaki tüketim de modele eklendi, böylece tahminler daha doğru oldu
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
Pivot tablolar, elektrik tüketiminin saat, gün, ay ve sıcaklığa göre nasıl değiştiğini görmek ve bu bilgileri modele yeni özellikler olarak eklemek için kullanıldı.  
Pivot tablolar sayesinde model sadece anlık verilere değil, geçmişteki tüketim ortalamalarına da erişmiş oldu.  
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
### Linear Regression

- Basit ve temel bir regresyon modelidir.

- Değişkenler arasındaki doğrusal ilişkiyi öğrenir.

- Random Forest’e kıyasla daha düşük performans gösterdi.

### Random Forest Regressor 

- Doğrusal olmayan ilişkileri öğrenebilir.

- Gürültülü ve karmaşık verilerde daha kararlı sonuçlar üretir.

- Daha yüksek R² ve daha düşük hata değerleri verdiği için final model olarak seçildi.

## Model Performans Karşılaştırması

<img width="436" height="124" alt="image" src="https://github.com/user-attachments/assets/78d347ac-a33d-456a-8814-50316ddacc0c" />


| Model | R² Skoru | MAE |
|-------|----------|-----|
| Linear Regression | 0.833 | 0.135 |
| Random Forest Regressor | 0.891 | 0.093 |

## Neden RandomForest En Başarılı Model Oldu ?
Bu projede kullanılan veri setinde hedef değişken ile girdiler arasındaki ilişki doğrusal değil. Linear Regression ise yalnızca doğrusal ilişkileri modelleyebilir.
Random Forest ise:

- Doğrusal olmayan ilişkileri öğrenebilir.

- Birden fazla karar ağacının ortalamasını alarak aşırı öğrenmeyi azaltır.

- Gürültülü ve dengesiz verilerde daha kararlı sonuç verir.

Bu nedenle daha başarılı oldu.

## Sonuç
Bu çalışmada elektrik tüketim verileri analiz edildi ve makine öğrenmesi modelleri ile tahmin edilmeye çalışıldı. Zaman bilgileri, cihaz tüketimleri ve çevresel faktörler kullanılarak model performansı artırıldı. Yapılan denemeler sonucunda Random Forest modelinin en başarılı sonuçları verdiği görüldü. Bu sayede gelecekteki elektrik tüketimi daha doğru şekilde tahmin edilebilir hale gelmiş oldu.



