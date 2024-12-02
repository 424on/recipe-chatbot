from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, Union
import os
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 벡터 스토어 로드
vectorstore_path = os.path.join(os.path.dirname(__file__), "../data/processed/recipe_vectorstore")
vectorstore = FAISS.load_local(
    vectorstore_path,
    OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")),
    allow_dangerous_deserialization=True
)

# GPT 모델 초기화
gpt_model = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
    temperature=0.7
)

class Query(BaseModel):
    query: str
    filters: Optional[Dict[str, Union[str, int]]] = None

@app.post("/chatbot")
async def chatbot(payload: Query):
    try:
        user_query = payload.query
        filters = payload.filters or {}

        if not user_query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Step 1: 벡터 스토어에서 유사 데이터 검색
        results = vectorstore.similarity_search(user_query, k=10)
        print(f"Retrieved documents: {results}")

        # Step 2: 필터 적용 (필터 조건 일부 완화)
        filtered_results = [
            res for res in results if all([
                not filters.get("dishType") or filters["dishType"] in res.metadata.get("CKG_KND_ACTO_NM", ""),
                not filters.get("difficulty") or filters["difficulty"] == res.metadata.get("CKG_DODF_NM", ""),
                not filters.get("time") or int(filters["time"]) >= int(res.metadata.get("CKG_TIME_NM", "0")),
            ])
        ]

        print(f"Filtered Results: {filtered_results}")

        # Step 3: 컨텍스트 생성
        context = "\n".join([res.page_content for res in filtered_results[:5]])

        # 필터를 만족하는 결과가 없는 경우 기본 메시지 추가
        if not filtered_results:
            context += "\n기본적으로 계란과 관련된 요리를 추천합니다."

        # Step 4: GPT 모델 호출
        prompt = f"""
        아래는 사용자 요청과 관련된 레시피 데이터입니다:
        {context}

        사용자의 질문: {user_query}
        위 정보를 참고하여 적절한 레시피를 단계별로 작성해 주세요.
        """
        gpt_response = gpt_model.invoke(prompt)

        # gpt_response가 BaseMessage 객체일 경우, content 속성 추출
        answer_content = gpt_response.content if hasattr(gpt_response, 'content') else str(gpt_response)

        return {"query": user_query, "answer": {"content": answer_content}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))