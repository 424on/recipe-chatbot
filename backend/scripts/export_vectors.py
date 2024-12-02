import sys
import os

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vectorstore import create_vectorstore

csv_path = os.path.join(os.path.dirname(__file__), "../data/recipes_utf8.csv")
output_path = os.path.join(os.path.dirname(__file__), "../data/processed/recipe_vectorstore")
progress_file = os.path.join(os.path.dirname(__file__), "../data/progress.json")

create_vectorstore(
    csv_path=csv_path,
    output_path=output_path,
    progress_file=progress_file
)