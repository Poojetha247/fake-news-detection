import { useEffect, useState } from "react";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const data = JSON.parse(localStorage.getItem("history")) || [];
    setHistory(data);
  }, []);

  // 🔥 NEW: Clear History Function
  const clearHistory = () => {
    localStorage.removeItem("history");
    setHistory([]);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        📜 Prediction History
      </h1>

      {/* 🔥 CLEAR BUTTON */}
      {history.length > 0 && (
        <div className="text-center mb-6">
          <button
            onClick={clearHistory}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
          >
            Clear History
          </button>
        </div>
      )}

      <div className="max-w-3xl mx-auto">
        {history.length === 0 ? (
          <p className="text-center text-gray-500">No history yet</p>
        ) : (
          history.map((item, index) => (
            <div
              key={index}
              className="bg-white p-4 mb-4 rounded-lg shadow"
            >
              <p className="text-gray-700 mb-2">
                <strong>Text:</strong> {item.text}
              </p>

              <p>
                <strong>Result:</strong>{" "}
                <span
                  className={
                    item.prediction === "Fake"
                      ? "text-red-500"
                      : "text-green-600"
                  }
                >
                  {item.prediction}
                </span>
              </p>

              <p>Confidence: {item.confidence}%</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default History;