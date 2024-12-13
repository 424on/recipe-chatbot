import React, { useState } from "react";
import axios from "axios";
import "./styles/App.css";

function App() {
  // 필터 상태 관리
  const [filters, setFilters] = useState({
    mealType: "", // 식사 종류 필터
    mealTime: "", // 식사 시간대 필터
    difficulty: "", // 난이도 필터
    time: 30, // 소요 시간 필터 (기본값: 30분)
  });
  const [query, setQuery] = useState(""); // 사용자 입력 쿼리
  const [response, setResponse] = useState(""); // GPT 응답
  const [loading, setLoading] = useState(false); // 로딩 상태

  // 필터 업데이트 함수
  const handleFilterChange = (key, value) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      [key]: prevFilters[key] === value ? "" : value, // 동일한 버튼 클릭 시 해제
    }));
  };

  // 소요 시간 필터 업데이트
  const handleTimeChange = (e) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      time: parseInt(e.target.value, 10), // 숫자로 변환
    }));
  };

  // GPT API 호출
  const handleSearch = async () => {
    if (!query) {
      alert("요리 재료나 요리 이름을 입력해주세요!");
      return;
    }

    setLoading(true);
    setResponse("");

    try {
      const result = await axios.post("http://127.0.0.1:8000/chatbot", {
        query,
        filters,
      });
      setResponse(result.data.answer.content || "결과를 가져올 수 없습니다.");
    } catch (error) {
      console.error("Error fetching data:", error);
      setResponse("오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* 헤더 */}
      <header className="header">
        <h1>🍳 레시피 추천 챗봇</h1>
        <p>필터를 선택하고 원하는 요리를 입력해 주세요.</p>
      </header>

      {/* 메인 콘텐츠 */}
      <main className="main-content">
        {/* 필터 섹션 */}
        <section className="filter-section">
          <h2>필터 입력</h2>

          {/* 식사 종류 필터 */}
          <div className="input-group">
            <label>식사 종류:</label>
            <div className="button-group">
              {["식사", "메인 요리", "사이드", "디저트"].map((mealType) => (
                <button
                  key={mealType}
                  className={`filter-btn ${
                    filters.mealType === mealType ? "active" : ""
                  }`}
                  onClick={() => handleFilterChange("mealType", mealType)}
                >
                  {mealType}
                </button>
              ))}
            </div>
          </div>

          {/* 식사 시간대 필터 */}
          <div className="input-group">
            <label>식사 시간대:</label>
            <div className="button-group">
              {["아침", "점심", "저녁", "간식"].map((mealTime) => (
                <button
                  key={mealTime}
                  className={`filter-btn ${
                    filters.mealTime === mealTime ? "active" : ""
                  }`}
                  onClick={() => handleFilterChange("mealTime", mealTime)}
                >
                  {mealTime}
                </button>
              ))}
            </div>
          </div>

          {/* 난이도 필터 */}
          <div className="input-group">
            <label>난이도:</label>
            <div className="button-group">
              {["초급", "중급", "고급"].map((difficulty) => (
                <button
                  key={difficulty}
                  className={`filter-btn ${
                    filters.difficulty === difficulty ? "active" : ""
                  }`}
                  onClick={() => handleFilterChange("difficulty", difficulty)}
                >
                  {difficulty}
                </button>
              ))}
            </div>
          </div>

          {/* 소요 시간 필터 */}
          <div className="input-group">
            <label>소요 시간 (분):</label>
            <input
              type="range"
              min="5"
              max="120"
              step="5"
              value={filters.time}
              onChange={handleTimeChange}
            />
            <span>{filters.time}분</span>
          </div>
        </section>

        {/* 사용자 입력 섹션 */}
        <section className="query-section">
          <h2>요리 재료나 이름을 입력해 주세요</h2>
          <textarea
            placeholder="예: 계란이 들어간 메인반찬"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? "검색 중..." : "검색"}
          </button>
        </section>

        {/* 응답 섹션 */}
        {response && (
          <section className="response-section">
            <h2>레시피 답변:</h2>
            <div className="recipe-container">
              {response.split("\n").map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </section>
        )}
      </main>

      {/* 푸터 */}
      <footer className="footer">
        <p>&copy; 2024 레시피 챗봇. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
