import chardet

# 파일 경로
file_path = "/Users/yoonho/Desktop/recipe-chatbot/backend/data/recipes.csv"

# 파일 읽기 및 인코딩 확인 (처음 1MB만 읽기)
with open(file_path, 'rb') as f:
    partial_data = f.read(1024 * 1024)  # 1MB
    result = chardet.detect(partial_data)
    print(result)