from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re

app = Flask(__name__)
CORS(app)

# -------------------------------
# 📦 Load model
# -------------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# -------------------------------
# 🧹 Text Cleaning
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text


# -------------------------------
# 🔍 Dynamic Explanation
# -------------------------------
def generate_explanation(text, prediction):
    text_lower = text.lower()

    sensational_words = ["breaking", "shocking", "exclusive", "urgent", "alert"]
    emotional_words = ["hate", "fear", "anger", "panic"]

    reasons = []

    # 🔴 Fake case
    if prediction == 0:
        if any(word in text_lower for word in sensational_words):
            reasons.append("Uses sensational or attention-grabbing words")

        if any(word in text_lower for word in emotional_words):
            reasons.append("Contains emotionally charged language")

        if not reasons:
            reasons.append("Lacks strong factual indicators and appears uncertain")

    # 🟢 Real case
    else:
        if len(text.split()) > 10:
            reasons.append("Contains detailed and structured information")

        if not any(word in text_lower for word in sensational_words):
            reasons.append("No sensational or misleading language detected")

        if not reasons:
            reasons.append("Appears to be neutral and informational")

    return reasons


# -------------------------------
# 🏠 Home
# -------------------------------
@app.route("/")
def home():
    return "Backend is running"


# -------------------------------
# 🤖 Prediction API
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # 🧹 Clean text
    processed = clean_text(text)
    vector = vectorizer.transform([processed])

    # 🤖 Model prediction
    prediction = model.predict(vector)[0]
    prob = model.predict_proba(vector)[0]

    label = "Real" if prediction == 1 else "Fake"
    confidence = round(max(prob) * 100, 2)

    # 🔥 Improved override logic
    if prediction == 0:
        text_lower = text.lower()

        if not any(word in text_lower for word in ["breaking", "shocking", "urgent", "alert", "exclusive"]):
            label = "Real"
            confidence = round(100 - confidence, 2)

    # 🔍 Explanation (based on FINAL prediction)
    final_prediction = 1 if label == "Real" else 0
    reasons = generate_explanation(text, final_prediction)

    return jsonify({
        "prediction": label,
        "confidence": confidence,
        "reasons": reasons
    })


# -------------------------------
# 🚀 Run app
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)