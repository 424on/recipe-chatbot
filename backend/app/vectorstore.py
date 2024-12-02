from langchain_community.document_loaders import CSVLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import json

# 환경 변수 로드
load_dotenv()

def create_vectorstore(csv_path: str, output_path: str, progress_file: str):
    print("Step 1: Loading data...")
    loader = CSVLoader(file_path=csv_path)
    data = loader.load()
    print(f"Loaded {len(data)} documents.")

    print("Step 2: Initializing OpenAI API embeddings...")
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # 진행 상태 복구 또는 초기화
    completed_batches = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            completed_batches = set(json.load(f))
    else:
        print(f"{progress_file} not found. Initializing progress file...")
        os.makedirs(os.path.dirname(progress_file), exist_ok=True)
        with open(progress_file, "w") as f:
            json.dump([], f)

    print(f"Resuming from batch {len(completed_batches) + 1}...")

    # 벡터 스토어 생성 및 병합
    vectorstore = None
    batch_size = 10  # 한번에 처리할 문서 개수

    for i in range(0, len(data), batch_size):
        batch_index = i // batch_size
        if batch_index in completed_batches:
            print(f"Skipping batch {batch_index + 1} (already completed)")
            continue

        batch = data[i:i + batch_size]
        print(f"Processing batch {batch_index + 1}: {len(batch)} documents")

        # 현재 배치의 벡터 스토어 생성
        batch_vectorstore = FAISS.from_documents(batch, embeddings)

        # 기존 vectorstore에 병합
        if vectorstore is None:
            vectorstore = batch_vectorstore
        else:
            vectorstore.merge_from(batch_vectorstore)

        # 진행 상태 저장
        completed_batches.add(batch_index)
        with open(progress_file, "w") as f:
            json.dump(list(completed_batches), f)

    print("Step 3: Saving vectorstore to disk...")
    vectorstore.save_local(output_path)
    print(f"Vectorstore saved to {output_path}")