from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, Union
import os
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


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


gpt_model = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.7
)

# 식사 종류 매핑
MEAL_TYPE_MAPPING = {
    "식사": ["밥/죽/떡", "국/탕", "찌개", "양식"],
    "메인 요리": ["메인반찬", "면/만두", "퓨전"],
    "사이드": ["밑반찬", "양념/소스/잼", "샐러드", "김치/젓갈/장류"],
    "디저트": ["디저트", "빵", "과자", "차/음료/술"],
}

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

        # 필터 확인 로그 출력
        print(f"Received Query: {user_query}")
        print(f"Received Filters: {filters}")

        # Step 1: 벡터 스토어에서 유사 데이터 검색
        results = vectorstore.similarity_search(user_query, k=10)
        print(f"Retrieved documents: {results}")

        # Step 2: 필터 적용 (식사 종류, 난이도, 소요 시간)
        filtered_results = [
            res for res in results if all([
                # 식사 종류 필터 (매핑된 종류로 필터링)
                not filters.get("mealType") or any(
                    category in MEAL_TYPE_MAPPING.get(filters["mealType"], [])
                    for category in res.metadata.get("CKG_KND_ACTO_NM", "").split("/")
                ),
                # 난이도 필터
                not filters.get("difficulty") or filters["difficulty"] == res.metadata.get("CKG_DODF_NM", ""),
                # 소요 시간 필터
                not filters.get("time") or int(filters["time"]) >= int(res.metadata.get("CKG_TIME_NM", "0")),
            ])
        ]

        # 필터 결과 로그 출력
        print(f"Filtered Results Count: {len(filtered_results)}")
        print(f"Filtered Results: {[res.metadata for res in filtered_results]}")

        # Step 3: 컨텍스트 생성
        context = "\n".join([res.page_content for res in filtered_results[:5]])

        # 필터를 만족하는 결과가 없는 경우 기본 메시지 추가
        if not filtered_results:
            context += "\n필터에 맞는 레시피가 없어 기본적인 추천을 제공합니다."

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

        # 응답에 필터 정보 포함
        return {
            "query": user_query,
            "filters": filters,
            "answer": {"content": answer_content},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))