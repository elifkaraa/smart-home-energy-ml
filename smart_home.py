# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

veri = pd.read_csv("Smart_Home_Dataset.csv")

veri["time"] = pd.to_numeric(veri["time"], errors="coerce")
veri = veri.dropna(subset=["time"])
veri["time"] = pd.to_datetime(veri["time"], unit="s")

veri.fillna(method="ffill", inplace=True)

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


hour_pivot = veri.pivot_table(index="hour", values="use [kW]", aggfunc="mean")
veri["hour_avg_kw"] = veri["hour"].map(hour_pivot["use [kW]"])

day_pivot = veri.pivot_table(index="dayofweek", values="use [kW]", aggfunc="mean")
veri["day_avg_kw"] = veri["dayofweek"].map(day_pivot["use [kW]"])

month_pivot = veri.pivot_table(index="month", values="use [kW]", aggfunc="mean")
veri["month_avg_kw"] = veri["month"].map(month_pivot["use [kW]"])

temp_pivot = veri.pivot_table(index="temperature", values="use [kW]", aggfunc="mean")
veri["temp_avg_kw"] = veri["temperature"].map(temp_pivot["use [kW]"])

features = [
    "hour", "dayofweek", "month",
    "temperature", "humidity",
    "appliance_total_kw",
    "prev_use_kw",
    "hour_avg_kw", "day_avg_kw",
    "month_avg_kw", "temp_avg_kw"
]

X = veri[features]
y = veri["use [kW]"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

y_pred_lr = lr_model.predict(X_test)

print("Linear Regression R²:", r2_score(y_test, y_pred_lr))
print("Linear Regression MAE:", mean_absolute_error(y_test, y_pred_lr))

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=3,
    random_state=0,
    n_jobs=-1
)
model.fit(X_train, y_train)

y_pred_rf= model.predict(X_test)

print("R² Score:", r2_score(y_test, y_pred_rf))
print("MAE:", mean_absolute_error(y_test, y_pred_rf))

plt.figure(figsize=(12,5))
plt.plot(y_test.values[:300], label="Gerçek", linewidth=2)
plt.plot(y_pred_rf[:300], label="Tahmin", linewidth=2)
plt.legend()
plt.title("Gerçek vs Tahmin Elektrik Tüketimi")
plt.xlabel("Zaman")
plt.ylabel("kW")

plt.figure(figsize=(12,5))
plt.plot(y_test.values[:300], label="Gerçek", linewidth=2)
plt.plot(y_pred_lr[:300], label="Linear Regression", linestyle="--")
plt.plot(y_pred_rf[:300], label="Random Forest")
plt.legend()
plt.title("Linear Regression vs Random Forest Tahmin Karşılaştırması")
plt.xlabel("Zaman")
plt.ylabel("kW")
plt.show()


