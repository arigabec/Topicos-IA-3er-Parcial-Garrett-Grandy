// En el archivo frontend/src/App.js
import React, { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState(null);

  const analyzeText = async () => {
    try {
      const requestBody = { text: text };
      console.log("Request Body:", requestBody);
      const response = await fetch("http://127.0.0.1:8000/analysis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });
  
      if (!response.ok) {
        throw new Error(`Failed with status: ${response.status}`);
      }
  
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error analyzing text:", error.message);
    }
  };
  
  

  const getStatus = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/status");
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error("Error getting status:", error);
    }
  };
  
  return (
    <div>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={analyzeText}>Analyze Text</button>
      <button onClick={getStatus}>Get Status</button>

      {result && (
        <div>
          <h2>Analysis Result:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {status && (
        <div>
          <h2>Status:</h2>
          <pre>{JSON.stringify(status, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
