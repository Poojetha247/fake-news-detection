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

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# 🔥 DEBUG: print model file info
print("🚀 Loading model from:", model_path)
print("📦 MODEL SIZE:", os.path.getsize(model_path), "bytes")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
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
# 🤖 Prediction API
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    processed = clean_text(text)
    vector = vectorizer.transform([processed])

    prediction = model.predict(vector)[0]
    probabilities = model.predict_proba(vector)[0]

    confidence = round(max(probabilities) * 100, 2)
    label = "Real" if prediction == 1 else "Fake"

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