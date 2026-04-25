from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import os

app = Flask(__name__)
CORS(app)

# -------------------------------
# 📦 Load model safely
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)


# -------------------------------
# 🧹 Text Cleaning
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text


# -------------------------------
# 🔍 Explanation
# -------------------------------
def generate_explanation(text, prediction):
    text_lower = text.lower()

    sensational_words = ["breaking", "shocking", "exclusive", "urgent", "alert"]
    emotional_words = ["hate", "fear", "anger", "panic"]

    reasons = []

    if prediction == 0:
        if any(word in text_lower for word in sensational_words):
            reasons.append("Uses sensational or attention-grabbing words")

        if any(word in text_lower for word in emotional_words):
            reasons.append("Contains emotionally charged language")

        if not reasons:
            reasons.append("Lacks strong factual indicators")

    else:
        if len(text.split()) > 10:
            reasons.append("Contains detailed and structured information")

        if not any(word in text_lower for word in sensational_words):
            reasons.append("No sensational language detected")

        if not reasons:
            reasons.append("Appears neutral and informational")

    return reasons


# -------------------------------
# 🏠 Home
# -------------------------------
@app.route("/")
def home():
    return "Backend is running"


# -------------------------------
# 🤖 Prediction API (FIXED)
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Clean
    processed = clean_text(text)

    # Vectorize
    vector = vectorizer.transform([processed])

    # 🔥 Proper ML prediction
    prediction = model.predict(vector)[0]
    probabilities = model.predict_proba(vector)[0]

    # Confidence
    confidence = round(max(probabilities) * 100, 2)

    # Label
    label = "Real" if prediction == 1 else "Fake"

    # Explanation
    reasons = generate_explanation(text, prediction)

    return jsonify({
        "prediction": label,
        "confidence": confidence,
        "reasons": reasons
    })


# -------------------------------
# 🚀 Run
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)