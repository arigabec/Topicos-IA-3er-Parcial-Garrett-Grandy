// En el archivo frontend/src/App.js
import React, { useState } from "react";
import bannerImage from "../../frontend/src/images/banner.jpg";
import { TextField, Button } from "@mui/material"; // Asegúrate de haber instalado y configurado Material-UI

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState(null);

  const analyzeText = async () => {
    try {
      const requestBody = { text: text };
      console.log("Request Body:", requestBody.text);
      const response = await fetch("http://127.0.0.1:8000/analysis?text=" + requestBody.text, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
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

  const renderEntity = (entity) => (
    <div key={entity.entity}>
      <h3>{entity.entity}</h3>
      <p>{entity.problematic}</p>
    </div>
  );

  return (
    <div>
      <div
        style={{
          backgroundImage: `url(${bannerImage})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          color: "white",
          padding: "20px",
          textAlign: "center",
          height: "600px",
        }}
      >
        <h1
          style={{
            fontSize: "80px",
            fontWeight: "bold",
            marginTop: "250px",
            textShadow: "6px 6px 6px #000000",
          }}
        >
          ANALIZADOR DE TEXTOS JURIDICOS
        </h1>
      </div>

      <div
        style={{
          display: "flex",
          backgroundColor: "#FFDDAB",
          padding: "20px",
          textAlign: "center",
        }}
      >
        {/* Línea Horizontal 1 */}
        <div style={{ flex: 1, borderRight: "1px solid #000", paddingTop: "50px" }}>
          <Button
            variant="contained"
            color="secondary"
            style={{ margin: "10px", height: "60px", fontSize: "20px", backgroundColor: "#B07C30" }}
            onClick={getStatus}
          >
            Get Status
          </Button>
        </div>
        <div style={{ flex: 1, borderRight: "1px solid #000", padding: "10px", textAlign: "justify", fontSize: "20px", fontFamily: "Arial", paddingLeft: "50px", paddingRight: "50px" }}>
          <h2>Descripción:</h2>
          <p>
            Get status se encargará de brindar el estado de la aplicación, proporcionando información como el nombre de los autores, los modelos usados, la versión, etc.
          </p>
        </div>
        <div style={{ flex: 1, padding: "10px" }}>
          {status && (
            <div>
              <h2>Status:</h2>
              <p>
                <strong>Status:</strong> {status.status}
                <br />
                <strong>Message:</strong> {status.message}
                <br />
                <strong>Model:</strong> {status.model}
                <br />
                <strong>Service:</strong> {status.service}
                <br />
                <strong>Version:</strong> {status.version}
                <br />
                <strong>Author:</strong> {status.author}
              </p>
            </div>
          )}
        </div>
      </div>

      <div
        style={{
          display: "flex",
          backgroundColor: "#FFDDAB",
          paddingRight: "10px",
          paddingLeft: "10px",
          paddingTop: "50px",
          paddingBottom: "50px",
          textAlign: "center",
        }}
      >
        {/* Línea Horizontal 2 */}
        <div style={{ flex: 1, borderRight: "1px solid #000", paddingRight: "15px", height: "100%", textAlign: "center" }}>
          <TextField
            variant="outlined"
            multiline
            rows={4}
            fullWidth
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={{ backgroundColor: "#FFFFFF", margin: "5px" }}
          />
          <Button
            variant="contained"
            color="primary"
            style={{ margin: "10px", height: "60px", fontSize: "20px", backgroundColor: "#B07C30" }}
            onClick={analyzeText}
          >
            Analyze Text
          </Button>
        </div>
        <div style={{ flex: 1, borderRight: "1px solid #000", padding: "10px", textAlign: "justify", fontSize: "20px", fontFamily: "Arial", paddingLeft: "50px", paddingRight: "50px" }}>
          <h2>Descripción:</h2>
          <p>
            Ayuda a analizar el texto jurídico.
          </p>
        </div>
        <div style={{ flex: 1, padding: "10px" }}>
          {result && (
            <div>
              <h2>Analysis Result:</h2>
              {result.entities && result.entities.map(renderEntity)}
            </div>
          )}
        </div>
      </div>
    </div>
  );

}

export default App;
