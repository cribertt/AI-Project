from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Cargar dataset
df = pd.read_csv('https://dev.hydrassa.com/inacap/csv/insurance.csv')

# 2. Preprocesar datos
df['sex'] = df['sex'].map({'male': 1, 'female': 0})
df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})
df = pd.get_dummies(df, columns=['region'], drop_first=True)

X = df.drop('charges', axis=1)
y = df['charges']

# 3. Escalar datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Entrenar modelo Random Forest
model = RandomForestRegressor(
    n_estimators=300,       # cantidad de árboles
    max_depth=None,        # profundidad ilimitada
    random_state=42,       # para reproducibilidad
    n_jobs=-1              # usar todos los núcleos
)
model.fit(X_scaled, y)

# 5. Guardar modelo y scaler
joblib.dump(model, os.path.join(BASE_DIR, 'insurance_model.pkl'))
joblib.dump(scaler, os.path.join(BASE_DIR, 'insurance_scaler.pkl'))

print("✅ Modelo Random Forest entrenado y guardado correctamente.")
