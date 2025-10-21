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

        age = float(data.get('age', 0))
        sex = 1 if data.get('sex', 'male') == 'male' else 0
        bmi = float(data.get('bmi', 0))
        children = float(data.get('children', 0))
        smoker = 1 if data.get('smoker', 'no') == 'yes' else 0
        region = data.get('region', 'northeast').lower()

        # Crear variables dummy igual que en el entrenamiento
        region_northwest = 1 if region == 'northwest' else 0
        region_southeast = 1 if region == 'southeast' else 0
        region_southwest = 1 if region == 'southwest' else 0

        # El orden debe coincidir con el del entrenamiento
        X = np.array([[age, sex, bmi, children, smoker,
                       region_northwest, region_southeast, region_southwest]])

        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]

        return Response({'predicted_cost': round(float(prediction), 2)})

    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
def get_insurance_data(request):
    df = pd.read_csv('https://dev.hydrassa.com/inacap/csv/insurance.csv')
    df['sex'] = df['sex'].map({'male': 1, 'female': 0})
    df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})
    df = pd.get_dummies(df, columns=['region'], drop_first=True)

    X = df.drop('charges', axis=1)
    y = df['charges']

    rf = RandomForestRegressor()
    rf.fit(X, y)

    importances = rf.feature_importances_
    features = X.columns.tolist()

    return Response({
        "features": features,
        "importance": importances.tolist()
    })