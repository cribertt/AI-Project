from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import numpy as np
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, 'insurance_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'insurance_scaler.pkl'))

@api_view(['POST'])
def predict_insurance(request):
    try:
        data = request.data

        # 1. Obtener valores de entrada
        age = float(data.get('age', 0))
        sex = 1 if data.get('sex', 'male') == 'male' else 0
        bmi = float(data.get('bmi', 0))
        children = float(data.get('children', 0))
        smoker = 1 if data.get('smoker', 'no') == 'yes' else 0
        region = data.get('region', 'northeast').lower()

        # 2. Crear variables dummy igual que en el entrenamiento
        region_northwest = 1 if region == 'northwest' else 0
        region_southeast = 1 if region == 'southeast' else 0
        region_southwest = 1 if region == 'southwest' else 0

        # 3. Orden idéntico al entrenamiento
        X = np.array([[age, sex, bmi, children, smoker,
                       region_northwest, region_southeast, region_southwest]])

        # 4. Escalar y predecir
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]

        return Response({'predicted_cost': round(float(prediction), 2)})

    except Exception as e:
        return Response({'error': str(e)}, status=400)
