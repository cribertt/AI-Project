import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Cargar dataset desde tu dominio (o Kaggle)
df = pd.read_csv('https://dev.hydrassa.com/inacap/csv/diabetes.csv')

# 2. Separar variables y objetivo
X = df.drop('outcome', axis=1)
y = df['outcome']

# 3. Dividir en train/test (opcional, solo para validar)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Escalado
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Entrenar modelo de regresión logística
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# 6. Guardar modelo y scaler como .pkl
joblib.dump(model, os.path.join(BASE_DIR, 'diabetes_model.pkl'))
joblib.dump(scaler, os.path.join(BASE_DIR, 'diabetes_scaler.pkl'))
