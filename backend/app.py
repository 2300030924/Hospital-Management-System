from flask import Flask, request, render_template, jsonify
import joblib, numpy as np, os
import traceback

app = Flask(__name__)

# ---------- Load model & scaler ----------
MODEL_PATH = os.path.join('model', 'heart_disease_model.pkl')
SCALER_PATH = os.path.join('model', 'scaler.pkl')
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# NOTE: these must match what you trained on
TRAIN_COLS = ['age','gender','impluse','pressurehight','pressurelow','glucose','kcm','troponin']

@app.route('/')
def index():
    return render_template('index.html')

# ---------- JSON API for AJAX ----------
@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json(force=True)  # expects JSON payload

        # Map frontend keys -> training column order
        # (frontend uses "impulse", "highbp", "lowbp")
        row = [
            float(data['age']),
            float(data['gender']),
            float(data['impulse']),
            float(data['highbp']),
            float(data['lowbp']),
            float(data['glucose']),
            float(data['kcm']),
            float(data['troponin']),
        ]

        X = np.array(row, dtype=float).reshape(1, -1)
        Xs = scaler.transform(X)
        # Binary model: proba for class 1 (disease)
        if hasattr(model, "predict_proba"):
            p1 = float(model.predict_proba(Xs)[0][1])
        else:
            # fallback: decision_function or plain predict
            pred = int(model.predict(Xs)[0])
            p1 = 0.85 if pred == 1 else 0.15

        # Friendly buckets
        if p1 >= 0.66:
            bucket = "High"
            tips = [
                "Consult a clinician for a full evaluation.",
                "Review blood pressure & lipid control.",
                "Consider lifestyle changes (diet, exercise, tobacco).",
            ]
        elif p1 >= 0.33:
            bucket = "Moderate"
            tips = [
                "Track BP, cholesterol, glucose regularly.",
                "Increase physical activity gradually.",
                "Discuss preventive steps with your provider.",
            ]
        else:
            bucket = "Low"
            tips = [
                "Maintain healthy habits and routine checkups.",
                "Keep an eye on BP, cholesterol, and glucose.",
            ]

        return jsonify({
            "risk_category": bucket,
            "probability": round(p1, 3),
            "tips": tips
        })
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
