import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import History from "./History";

function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const theme =
    !result
      ? "blue"
      : result.prediction === "Fake"
      ? "red"
      : "green";

  const handlePredict = async () => {
    if (!text.trim()) {
      setError("Please enter some text");
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const res = await fetch("https://fake-news-detection-vk6y.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text }),
        cache: "no-store" // 🔥 prevent caching
      });

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();

      // 🔥 DEBUG (VERY IMPORTANT)
      console.log("API RESPONSE:", data);

      // ✅ SAFE SET (avoid stale/wrong data)
      setResult({
        prediction: data.prediction,
        confidence: Number(data.confidence),
        reasons: data.reasons || []
      });

      // Save history
      const newEntry = {
        text,
        prediction: data.prediction,
        confidence: data.confidence,
      };

      const existing = JSON.parse(localStorage.getItem("history")) || [];
      localStorage.setItem("history", JSON.stringify([newEntry, ...existing]));

    } catch (err) {
      console.error(err);
      setError("⚠️ Unable to connect to backend.");
    }

    setLoading(false);
  };

  return (
    <div
      className={`min-h-screen flex flex-col items-center p-6 transition-all duration-500 ${
        theme === "blue"
          ? "bg-gradient-to-br from-blue-50 to-indigo-100"
          : theme === "red"
          ? "bg-gradient-to-br from-red-50 to-red-200"
          : "bg-gradient-to-br from-green-50 to-emerald-200"
      }`}
    >

      <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">
        🧠 AI-Powered Fake News Analysis System
      </h1>

      <p className="text-gray-500 text-sm mb-6 text-center">
        Detects misinformation using machine learning
      </p>

      {/* INPUT */}
      <div className="bg-white shadow-lg rounded-xl p-6 w-full max-w-2xl">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste news article here..."
          className="w-full p-4 border rounded-lg resize-none"
          rows="5"
        />

        <button
          onClick={handlePredict}
          disabled={loading}
          className={`w-full mt-4 text-white py-3 rounded-lg font-semibold transition ${
            theme === "blue"
              ? "bg-blue-600 hover:bg-blue-700"
              : theme === "red"
              ? "bg-red-500 hover:bg-red-600"
              : "bg-green-600 hover:bg-green-700"
          } ${loading ? "opacity-70 cursor-not-allowed" : ""}`}
        >
          {loading ? "Analyzing..." : "Analyze News"}
        </button>

        {loading && (
          <div className="flex justify-center mt-4">
            <div className="w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}

        {error && (
          <div className="mt-4 text-red-600 text-sm">
            {error}
          </div>
        )}
      </div>

      {/* RESULT */}
      {result && (
        <div className="mt-6 bg-white shadow-lg rounded-xl p-6 w-full max-w-2xl">

          <h2
            className={`text-xl font-bold mb-2 ${
              result.prediction === "Fake"
                ? "text-red-500"
                : "text-green-600"
            }`}
          >
            {result.prediction === "Fake"
              ? "⚠️ Fake News Detected"
              : "✔️ Likely Real News"}
          </h2>

          <p className="text-gray-700 mb-2">
            Confidence: <strong>{result.confidence}%</strong>
          </p>

          <div className="text-sm text-gray-500 italic mb-4">
            ⚠️ Model performs better on longer, detailed news articles.
          </div>

          {result.reasons && (
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">
                Analysis:
              </h3>

              <ul className="list-disc ml-5 text-gray-700 space-y-1">
                {result.reasons.map((reason, i) => (
                  <li key={i}>{reason}</li>
                ))}
              </ul>
            </div>
          )}

        </div>
      )}

      <div className="mt-8">
        <Link to="/history" className="text-blue-600 underline">
          View Prediction History →
        </Link>
      </div>

    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Router>
  );
}

export default App;