import joblib
import pandas as pd 
#from feature_engineering import feature_eng
import shap

#LOAD MODEL
model = joblib.load('XGB_model.pkl')

#SHAP EXPLAINER 

xgb_model = model.named_steps['model']
explainer = shap.TreeExplainer(xgb_model)

#PREDICTION FUNCTION 

def predict_churn(data):

    user_df = pd.DataFrame([item.dict() for item in data])
    customer_ids = user_df['CustomerID']

    # Drop ID
    df_filtered = user_df.drop(columns=['CustomerID'])

    # PREDICTION
    predictions = model.predict(df_filtered)

    probabilities = model.predict_proba(df_filtered)

    # TRANSFORM DATA FOR SHAP

    feature_eng_data = model.named_steps['feature_eng'].transform(df_filtered)

    transformed_data = model.named_steps['preprocess'].transform(feature_eng_data)

    # SHAP VALUES

    shap_values = explainer.shap_values(transformed_data)

    feature_names = model.named_steps['preprocess'].get_feature_names_out()
    

    # RESULT

    results = []

    for i in range(len(predictions)):

        pred = predictions[i]
        prob = probabilities[i]
        customer_shap = shap_values[i]

        # Create dataframe of shap values
        shap_df = pd.DataFrame({
            'feature': feature_names,
            'shap_value': customer_shap
        })

        # FILTER IMPORTANT FEATURES
        insights = []

        if pred == 1:
            positive_features = shap_df[shap_df['shap_value'] > 0].sort_values(by='shap_value',ascending=False).head(3)
            feature=positive_features['feature'].values
            for row in feature:
                insights.append(f"{row} increased churn tendency")

            results.append({
            "CustomerID": customer_ids.iloc[i],
            "Prediction":"Churn",
            "Probability":f"{prob[1]*100:.2f}%",
            "Top Factors": insights
            })

        else:
            negative_features = shap_df[shap_df['shap_value'] < 0].sort_values(by='shap_value',ascending=True).head(3)
            feature=negative_features['feature'].values
            for row in feature:
                insights.append(f"{row} reduced churn tendency")

            results.append({
                    "CustomerID": customer_ids.iloc[i],
                    "Prediction":"Not Churn",
                    "Probability":f"{prob[0]*100:.2f}%",
                    "Top Factors": insights
                    })

    return results