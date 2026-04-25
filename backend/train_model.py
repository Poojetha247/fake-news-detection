import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load data
fake = pd.read_csv("../dataset/Fake.csv")
true = pd.read_csv("../dataset/True.csv")

fake["label"] = 0
true["label"] = 1

# Balance dataset
min_count = min(len(fake), len(true))
fake = fake.sample(min_count)
true = true.sample(min_count)

df = pd.concat([fake, true])
df = df.sample(frac=1).reset_index(drop=True)

df["content"] = df["title"] + " " + df["text"]
df = df[["content", "label"]]

# Preprocessing
try:
    stopwords.words("english")
except:
    nltk.download("stopwords")

stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

df["content"] = df["content"].apply(preprocess)

# Split
X = df["content"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Vectorization
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model
model = SGDClassifier(loss='log_loss')
model.fit(X_train_vec, y_train)

# 🔥 Evaluation
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

print("✅ Accuracy:", accuracy)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained and saved!")