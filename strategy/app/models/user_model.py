import joblib
import numpy as np

# Load model and encoders
model = joblib.load('app/models/user_strategy_model.joblib')
goal_encoder = joblib.load('app/models/goal_encoder.joblib')
risk_encoder = joblib.load('app/models/risk_encoder.joblib')
horizon_encoder = joblib.load('app/models/horizon_encoder.joblib')
strategy_encoder = joblib.load('app/models/strategy_encoder.joblib')

def predict_strategy(goal, risk, horizon):
    goal_enc = goal_encoder.transform([goal])[0]
    risk_enc = risk_encoder.transform([risk])[0]
    horizon_enc = horizon_encoder.transform([horizon])[0]

    input_features = np.array([[goal_enc, risk_enc, horizon_enc]])
    prediction = model.predict(input_features)[0]

    return strategy_encoder.inverse_transform([prediction])[0]
