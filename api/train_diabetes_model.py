import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Cargar dataset
df = pd.read_csv('https://dev.hydrassa.com/inacap/csv/diabetes.csv')

# 2. Separar variables y objetivo
X = df.drop('outcome', axis=1)
y = df['outcome']

# 3. Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Escalado (opcional para Random Forest, pero lo dejamos para mantener consistencia)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Entrenar modelo Random Forest
model = RandomForestClassifier(
    n_estimators=300,   # cantidad de árboles
    max_depth=None,    # profundidad ilimitada
    random_state=42,
    n_jobs=-1          # usa todos los núcleos disponibles
)
model.fit(X_train_scaled, y_train)

# 6. Evaluar modelo (opcional)
y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {acc:.4f}")
print("📊 Matriz de confusión:\n", confusion_matrix(y_test, y_pred))
print("📋 Reporte de clasificación:\n", classification_report(y_test, y_pred))

# 7. Guardar modelo y scaler
joblib.dump(model, os.path.join(BASE_DIR, 'diabetes_model.pkl'))
joblib.dump(scaler, os.path.join(BASE_DIR, 'diabetes_scaler.pkl'))

print("Modelo Random Forest de diabetes guardado correctamente ✅")
