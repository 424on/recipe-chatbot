import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/HomePage.css";

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1 className="home-title">레시피 추천 챗봇에 오신 것을 환영합니다!</h1>
      <button className="home-button" onClick={() => navigate("/filter")}>
        시작하기
      </button>
    </div>
  );
}

export default HomePage;
