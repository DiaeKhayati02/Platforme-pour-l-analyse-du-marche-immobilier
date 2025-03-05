# predictor/utils.py
import joblib

def load_model():
    path = r'C:\Users\Asus PC\Desktop\model+data\best_price_prediction_model2.joblib'
    model = joblib.load(path)
    return model

def load_model2():
    path = r'C:\Users\Asus PC\Desktop\model+data\modelterrain4.joblib'
    model = joblib.load(path)
    return model

from sklearn.preprocessing import StandardScaler
import pandas as pd

def preprocess_data5(df):
    # Apply the same preprocessing steps as during model training
    
    # Standardize numerical features
    scaler = StandardScaler()
    df[['Surface', 'Nombre de chambres', 'Nombre de toilettes', 'Surface per room']] = scaler.fit_transform(df[['Surface', 'Nombre de chambres', 'Nombre de toilettes', 'Surface per room']])
    
    # Encode categorical features
    df = pd.get_dummies(df, drop_first=True)
    
    return df