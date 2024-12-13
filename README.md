# 🍳 Recipe Chatbot

**Recipe Chatbot**은 사용자가 입력한 재료와 필터 조건을 기반으로 개인화된 레시피를 추천하는 웹 애플리케이션입니다. RAG(Retrieval-Augmented Generation) 기술과 OpenAI API를 활용하여 방대한 레시피 데이터에서 적합한 레시피를 검색하고, 사용자 맞춤형 답변을 제공합니다.

---

## 📌 주요 기능
- **재료 기반 검색**: 사용자가 입력한 재료를 최우선으로 고려하여 레시피 추천.
- **다양한 필터 기능**:
  - **식사 종류**: 식사, 메인 요리, 사이드, 디저트
  - **식사 시간대**: 아침, 점심, 저녁, 간식
  - **난이도**: 초급, 중급, 고급
  - **소요 시간**: 5분 ~ 120분
- **AI 기반 레시피 답변 생성**: OpenAI GPT API를 활용해 친절하고 상세한 답변 제공.
- **웹 기반 인터페이스**: 직관적이고 간단한 UI/UX 설계.

---

## 🚀 기술 스택
### **프론트엔드**
- **React.js**: 사용자 인터페이스 구현
- **CSS**: 반응형 디자인
- **Axios**: API 요청 및 데이터 통신

### **백엔드**
- **FastAPI**: RESTful API 서버
- **FAISS**: 벡터 기반 데이터 검색
- **OpenAI GPT API**: 텍스트 생성 및 답변 포맷팅

### **데이터**
- **농식품 빅데이터 거래소**:
  - 18만 건 이상의 레시피 데이터
  - OpenAI Embeddings를 활용한 벡터화
  - FAISS를 통한 빠르고 정확한 데이터 검색

---

## 📂 프로젝트 구조
```plaintext
recipe-chatbot/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React 컴포넌트
│   │   ├── styles/          # CSS 스타일링
│   │   └── App.js           # 메인 애플리케이션 파일
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI 서버
│   │   ├── vectorstore.py   # 데이터 벡터화 및 검색 로직
│   └── requirements.txt     # Python 패키지 목록
└── README.md

💡 설치 및 실행 방법

1. 프로젝트 클론 및 환경 설정

git clone https://github.com/424on/recipe-chatbot.git
cd recipe-chatbot

2. 백엔드 설정

cd backend
pip install -r requirements.txt
python main.py

3. 프론트엔드 설정

cd ../frontend
npm install
npm start

🎯 필터 동작 원리
	1.	재료 기반 필터링:
	•	사용자가 입력한 재료를 최우선 조건으로 설정.
	2.	추가 필터 조건 적용:
	•	식사 종류, 난이도, 소요 시간 등 사용자가 설정한 조건을 추가적으로 반영.
	3.	벡터 스토어 검색:
	•	OpenAI Embeddings로 벡터화된 레시피 데이터를 FAISS를 사용하여 검색.
	•	필터 조건에 부합하는 데이터를 빠르게 검색.
	4.	AI 답변 생성:
	•	검색된 레시피 데이터를 GPT 모델로 전달해 사용자 맞춤형 답변 생성.

🌟 RAG 활용
	•	FAISS(Vector Store):
	•	방대한 레시피 데이터를 임베딩해 벡터로 변환.
	•	검색 효율성을 높이기 위해 FAISS를 사용.
	•	GPT-3.5:
	•	필터링된 검색 결과를 사용자 질문에 맞게 자연스러운 언어로 답변 생성.
	•	데이터 처리:
	•	레시피 데이터셋에서 유효한 필드를 추출하고, Embeddings를 활용하여 유사도를 기반으로 검색.

🌐 주요 페이지 및 UI
	•	필터 섹션:
	•	사용자가 설정한 조건에 맞게 레시피를 검색.
	•	직관적인 버튼 인터페이스로 설계.
	•	답변 섹션:
	•	사용자가 입력한 조건과 검색된 데이터를 기반으로 상세한 요리 레시피 제공.
	•	단계별 레시피 가독성을 높인 스타일링.

📋 한계점 및 개선 방향
	•	한계점:
	•	입력 재료가 적을수록 결과가 간단한 요리로만 제한되는 경우 발생.
	•	외부 웹 크롤링 및 추가 데이터 소스 활용 기능 미구현.
	•	개선 방향:
	•	외부 데이터 소스(블로그, 요리 사이트) 통합을 통한 검색 결과 확장.
	•	사용자 피드백 기반으로 추천 알고리즘 개선.

© 2024 Recipe Chatbot. All rights reserved.
