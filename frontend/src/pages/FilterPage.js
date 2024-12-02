import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/FilterPage.css";

function FilterPage() {
  const [filters, setFilters] = useState({
    name: "",
    dishType: "",
    difficulty: "",
    time: "",
  });

  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleNext = () => {
    navigate("/chatbot", { state: filters });
  };

  return (
    <div className="filter-container">
      <h2 className="filter-title">필터를 설정해주세요</h2>
      <label className="filter-label">이름:</label>
      <input
        className="filter-input"
        name="name"
        value={filters.name}
        onChange={handleInputChange}
        placeholder="사용자 이름을 입력하세요"
      />
      <label className="filter-label">요리 종류:</label>
      <select
        className="filter-select"
        name="dishType"
        value={filters.dishType}
        onChange={handleInputChange}
      >
        <option value="">선택하세요</option>
        <option value="밑반찬">밑반찬</option>
        <option value="메인반찬">메인반찬</option>
      </select>
      <label className="filter-label">난이도:</label>
      <select
        className="filter-select"
        name="difficulty"
        value={filters.difficulty}
        onChange={handleInputChange}
      >
        <option value="">선택하세요</option>
        <option value="초급">초급</option>
        <option value="중급">중급</option>
      </select>
      <label className="filter-label">소요 시간 (분):</label>
      <input
        className="filter-input"
        name="time"
        type="number"
        value={filters.time}
        onChange={handleInputChange}
      />
      <button className="filter-button" onClick={handleNext}>
        다음
      </button>
    </div>
  );
}

export default FilterPage;
