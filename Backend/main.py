from fastapi import FastAPI
from Backend.schema import CustomerData
from typing import List
from Backend.model_inference import predict_churn


app=FastAPI(title='Banking Churn Prediction API', 
            description='API for predicting customer churn in banking sector')

@app.get('/',tags=['Home Page'])
def home():
    return {'message': 'Welcome to the home page, Banking Churn Prediction System'}

@app.post('/predict',tags=['Prediction'])
def predict(data:List[CustomerData]):
    result = predict_churn(data)
    return {'status':'success', 'predictions': result}