from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd 
from feature_engineering import feature_eng
from schema import CustomerData

app=FastAPI()
model=joblib.load('XGB_model.pkl')
@app.get('/')
def home():
    return 'Welcome to the home page \n Banking Churn Prediction System'

@app.post('/predict')
def predict(data:CustomerData):
    user_df=pd.DataFrame([data.dict()])
    prediction=model.predict(user_df)[0]
    probability=model.predict_proba(user_df)[0]
    return ( f'Churn<\n>Chance of Churn is:{probability[1]*100:.2f}%' if prediction ==1 
              else f'Not Churn<\n>Chance of Not Churn is:{probability[0]*100:.2f}%' )