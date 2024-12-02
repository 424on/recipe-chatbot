import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import "../styles/ChatbotPage.css";

function ChatbotPage() {
  const location = useLocation();
  const filters = location.state || {};

  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleSearch = async () => {
    if (!query) {
      alert("요리 재료나 요리 이름을 입력해주세요!");
      return;
    }

    try {
      const result = await axios.post("http://127.0.0.1:8000/chatbot", {
        query,
        filters,
      });
      setResponse(result.data.answer.content || "결과를 가져올 수 없습니다.");
    } catch (error) {
      console.error(error);
      setResponse("오류가 발생했습니다. 다시 시도해주세요.");
    }
  };

  return (
    <div className="chatbot-container">
      <h2 className="chatbot-title">
        안녕하세요, {filters.name || "사용자"}님!
      </h2>
      <div className="chatbot-summary">
        <p>
          <strong>요리 종류:</strong> {filters.dishType || "선택되지 않음"}
        </p>
        <p>
          <strong>난이도:</strong> {filters.difficulty || "선택되지 않음"}
        </p>
        <p>
          <strong>소요 시간:</strong> {filters.time || "선택되지 않음"}분
        </p>
      </div>
      <textarea
        className="chatbot-textarea"
        placeholder="요리 재료나 요리 이름을 입력해주세요"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="chatbot-button" onClick={handleSearch}>
        검색
      </button>
      {response && (
        <div className="chatbot-response">
          <h3>레시피 답변:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default ChatbotPage;
