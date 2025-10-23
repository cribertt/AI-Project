from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
import pandas as pd
import joblib
import os
import numpy as np


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargar modelo y scaler
model = joblib.load(os.path.join(BASE_DIR, 'diabetes_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'diabetes_scaler.pkl')) 

def calcular_threshold_optimo():
    df = pd.read_csv('https://dev.hydrassa.com/inacap/csv/diabetes.csv')
    X = df.drop('outcome', axis=1)
    y = df['outcome']

    X_scaled = scaler.transform(X)
    y_pred_proba = model.predict_proba(X_scaled)[:, 1]

    fpr, tpr, thresholds = roc_curve(y, y_pred_proba)
    j_scores = tpr - fpr
    best_idx = np.argmax(j_scores)
    best_threshold = thresholds[best_idx]

    return float(best_threshold), tpr[best_idx], (1 - fpr[best_idx])


@api_view(['POST'])
def predict_diabetes(request):
    try:
        data = request.data

        # Entradas del paciente
        values = np.array([[  
            float(data.get('Pregnancies', 0)),
            float(data.get('Glucose', 0)),
            float(data.get('BloodPressure', 0)),
            float(data.get('SkinThickness', 0)),
            float(data.get('Insulin', 0)),
            float(data.get('BMI', 0)),
            float(data.get('DiabetesPedigreeFunction', 0)),
            float(data.get('Age', 0))
        ]])

        # Escalar entrada
        X_scaled = scaler.transform(values)
        prob = model.predict_proba(X_scaled)[0, 1]

        # Obtener threshold óptimo (dinámico)
        threshold, sensitivity, specificity = calcular_threshold_optimo()
        result = int(prob >= threshold)

        return Response({
            'probability': round(float(prob), 3),
            'prediction': result,
            'threshold': threshold,
            'sensitivity': round(float(sensitivity), 3),
            'specificity': round(float(specificity), 3)
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)