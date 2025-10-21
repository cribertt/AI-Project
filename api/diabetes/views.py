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

@api_view(['GET'])
def diabetes_roc_data(request):
    try:
        df = pd.read_csv('https://dev.hydrassa.com/inacap/csv/diabetes.csv')
        X = df.drop('outcome', axis=1)
        y = df['outcome']

        X_scaled = scaler.transform(X)
        y_pred_proba = model.predict_proba(X_scaled)[:, 1]

        fpr, tpr, thresholds = roc_curve(y, y_pred_proba)
        auc = roc_auc_score(y, y_pred_proba)

        # Reemplazar inf o NaN por valores válidos
        fpr = np.nan_to_num(fpr, nan=0.0, posinf=1.0, neginf=0.0)
        tpr = np.nan_to_num(tpr, nan=0.0, posinf=1.0, neginf=0.0)
        thresholds = np.nan_to_num(thresholds, nan=0.0, posinf=1.0, neginf=0.0)

        j_scores = tpr - fpr
        j_best_idx = j_scores.argmax()
        best_threshold = thresholds[j_best_idx]
        sensitivity = tpr[j_best_idx]
        specificity = 1 - fpr[j_best_idx]

        return Response({
            'fpr': fpr.tolist(),
            'tpr': tpr.tolist(),
            'thresholds': thresholds.tolist(),
            'auc': float(auc),
            'best_threshold': float(best_threshold),
            'sensitivity': float(sensitivity),
            'specificity': float(specificity)
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['POST'])
def predict_diabetes(request):
    try:
        data = request.data

        # Variables de entrada
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

        X_scaled = scaler.transform(values)
        prob = model.predict_proba(X_scaled)[0, 1]
        threshold = 0.45
        result = int(prob >= threshold)

        return Response({
            'probability': round(float(prob), 3),
            'prediction': result,
            'threshold': threshold
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)