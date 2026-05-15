import streamlit as st
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("📊 Banking Customer Churn Prediction System")

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Prediction"]
)

# =========================================================
# OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.header("📖 Project Overview")

    st.write("""
This application predicts customer churn in the banking sector using Machine Learning techniques.

The final prediction system was developed using an XGBoost model integrated with a preprocessing pipeline and SHAP-based explainability to interpret customer churn predictions.
""")

    st.header("🧠 Features Used")

    col1, col2 = st.columns(2)

    with col1:

        st.write("✅ Credit Score")
        st.write("✅ Geography")
        st.write("✅ Gender")
        st.write("✅ Age")
        st.write("✅ Tenure")

    with col2:

        st.write("✅ Balance")
        st.write("✅ Number of Products")
        st.write("✅ Credit Card Status")
        st.write("✅ Active Member")
        st.write("✅ Estimated Salary")

    st.header("🤖 Model Information")

    st.write("""
- Final Model: XGBoost Classifier
- ROC-AUC Score: 0.87
- Baseline Model: Logistic Regression
- Explainability Technique: SHAP
""")

# =========================================================
# PREDICTION PAGE
# =========================================================

elif page == "Prediction":

    st.header("📊 Enter Customer Details")

    col1, col2 = st.columns(2)

    # ---------------- LEFT COLUMN ---------------- #

    with col1:

        customer_id = st.number_input(
            "Customer ID",
            min_value=1,
            value=1001
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=650
        )

        geography = st.selectbox(
            "Geography",
            ["France", "Germany", "Spain"]
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        age = st.slider(
            "Age",
            min_value=18,
            max_value=100,
            value=35
        )

    # ---------------- RIGHT COLUMN ---------------- #

    with col2:

        tenure = st.slider(
            "Tenure",
            min_value=0,
            max_value=10,
            value=5
        )

        balance = st.number_input(
            "Balance",
            min_value=0.0,
            value=50000.0
        )

        num_products = st.slider(
            "Number of Products",
            min_value=1,
            max_value=4,
            value=2
        )

        has_card = st.selectbox(
            "Has Credit Card",
            ["Yes", "No"]
        )

        active_member = st.selectbox(
            "Is Active Member",
            ["Yes", "No"]
        )

        salary = st.number_input(
            "Estimated Salary",
            min_value=0.0,
            value=100000.0
        )

    # =========================================================
    # PREDICT BUTTON
    # =========================================================

    if st.button("Predict Churn"):

        # ---------------- MAPPING ---------------- #

        has_card = 1 if has_card == "Yes" else 0

        active_member = 1 if active_member == "Yes" else 0

        # ---------------- PAYLOAD ---------------- #

        payload = [
            {
                "CustomerID": customer_id,
                "CreditScore": credit_score,
                "Geography": geography,
                "Gender": gender,
                "Age": age,
                "Tenure": tenure,
                "Balance": balance,
                "NumOfProducts": num_products,
                "HasCrCard": has_card,
                "IsActiveMember": active_member,
                "EstimatedSalary": salary
            }
        ]

        # ---------------- API URL ---------------- #

        url = "YOUR_RENDER_API_URL/predict"

        response = requests.post(
            url,
            json=payload
        )

        # =========================================================
        # RESPONSE
        # =========================================================

        if response.status_code == 200:

            result = response.json()

            prediction_data = result['predictions'][0]

            prediction = prediction_data['Prediction']

            probability = prediction_data['Probability']

            top_factors = prediction_data['Top Factors']

            # ---------------- PREDICTION RESULT ---------------- #

            st.header("📈 Prediction Result")

            if prediction == "Churn":

                st.error(
                    "⚠️ Customer is likely to CHURN"
                )

            else:

                st.success(
                    "✅ Customer is likely to RETAIN"
                )

            st.metric(
                label="Prediction Probability",
                value=probability
            )

            # ---------------- SHAP INSIGHTS ---------------- #

            st.header("🧠 SHAP-Based Insights")

            for factor in top_factors:

                st.write(f"🔹 {factor}")

        else:

            st.error("❌ Failed to connect to API")