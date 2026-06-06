
import { useState } from "react";
import axios from "axios";

function App() {

  const [videoA, setVideoA] = useState("");
  const [videoB, setVideoB] = useState("");

  const [question, setQuestion] = useState("");

  const [analysis, setAnalysis] = useState(null);

  const [chatResponse, setChatResponse] = useState(null);

  const analyzeVideos = async () => {

    try {

      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/analyze`,
        {
          video_a: videoA,
          video_b: videoB
        }
      );

      setAnalysis(response.data);

    } catch (error) {

      console.log(error);
    }
  };

  const askQuestion = async () => {

    try {

      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/chat`,
        {
          question: question,

          metadata_a: {
            ...analysis.video_a.metadata,
            engagement_rate:
              analysis.video_a.engagement_rate
          },

          metadata_b: {
            ...analysis.video_b.metadata,
            engagement_rate:
              analysis.video_b.engagement_rate
          }
        }
      );

      const text = response.data.answer;

      let current = "";

      for (let i = 0; i < text.length; i++) {

        current += text[i];

        setChatResponse({
          ...response.data,
          answer: current
        });

        await new Promise((resolve) =>
          setTimeout(resolve, 5)
        );
      }

    } catch (error) {

      console.log(error);
    }
  };

  return (

    <div
      style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "40px",
        fontFamily: "Arial"
      }}
    >

      <h1 style={{ marginBottom: "30px" }}>
        RAG Video Analyzer
      </h1>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "12px"
        }}
      >

        <input
          type="text"
          placeholder="First Video URL"
          value={videoA}
          onChange={(e) => setVideoA(e.target.value)}
          style={{
            padding: "12px"
          }}
        />

        <input
          type="text"
          placeholder="Second Video URL"
          value={videoB}
          onChange={(e) => setVideoB(e.target.value)}
          style={{
            padding: "12px"
          }}
        />

        <button
          onClick={analyzeVideos}
          style={{
            padding: "12px",
            cursor: "pointer"
          }}
        >
          Analyze Videos
        </button>

      </div>

      {analysis && (

        <div
          style={{
            marginTop: "40px"
          }}
        >

          <div
            style={{
              display: "flex",
              gap: "20px",
              marginBottom: "30px"
            }}
          >

            <div
              style={{
                flex: 1,
                padding: "20px",
                border: "1px solid #ccc",
                borderRadius: "10px"
              }}
            >

              <h2>Video A</h2>

              <p>
                <strong>Views:</strong>{" "}
                {analysis.video_a.metadata.views}
              </p>

              <p>
                <strong>Likes:</strong>{" "}
                {analysis.video_a.metadata.likes}
              </p>

              <p>
                <strong>Comments:</strong>{" "}
                {analysis.video_a.metadata.comments}
              </p>

              <p>
                <strong>Creator:</strong>{" "}
                {analysis.video_a.metadata.creator}
              </p>

              <p>
                <strong>Engagement Rate:</strong>{" "}
                {analysis.video_a.engagement_rate}%
              </p>

            </div>

            <div
              style={{
                flex: 1,
                padding: "20px",
                border: "1px solid #ccc",
                borderRadius: "10px"
              }}
            >

              <h2>Video B</h2>

              <p>
                <strong>Views:</strong>{" "}
                {analysis.video_b.metadata.views}
              </p>

              <p>
                <strong>Likes:</strong>{" "}
                {analysis.video_b.metadata.likes}
              </p>

              <p>
                <strong>Comments:</strong>{" "}
                {analysis.video_b.metadata.comments}
              </p>

              <p>
                <strong>Creator:</strong>{" "}
                {analysis.video_b.metadata.creator}
              </p>

              <p>
                <strong>Engagement Rate:</strong>{" "}
                {analysis.video_b.engagement_rate}%
              </p>

            </div>

          </div>

          <div
            style={{
              background: "#f4f4f4",
              padding: "20px",
              borderRadius: "10px"
            }}
          >

            <h2>Analysis Result</h2>

            <h3>Video A Transcript</h3>

            <p>
              {analysis.video_a.transcript_preview}
            </p>

            <hr />

            <h3>Video B Transcript</h3>

            <p>
              {analysis.video_b.transcript_preview}
            </p>

          </div>

        </div>
      )}

      {analysis && (

        <div
          style={{
            marginTop: "40px",
            display: "flex",
            flexDirection: "column",
            gap: "12px"
          }}
        >

          <input
            type="text"
            placeholder="Ask a question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            style={{
              padding: "12px"
            }}
          />

          <button
            onClick={askQuestion}
            style={{
              padding: "12px",
              cursor: "pointer"
            }}
          >
            Ask Question
          </button>

        </div>
      )}

      {chatResponse && (

        <div style={{ marginTop: "40px" }}>

          <h2>Chat Response</h2>

          <div
            style={{
              background: "#f4f4f4",
              padding: "20px",
              borderRadius: "10px"
            }}
          >

            <p
              style={{
                whiteSpace: "pre-wrap",
                lineHeight: "1.8"
              }}
            >
              {chatResponse.answer}
            </p>

            <h3 style={{ marginTop: "20px" }}>
              References
            </h3>

            <ul>

              {chatResponse.references.map((ref, index) => (

                <li key={index}>
                  Video: {ref.video} |
                  Chunk: {ref.chunk}
                </li>

              ))}

            </ul>

          </div>

        </div>
      )}

    </div>
  );
}

export default App;
