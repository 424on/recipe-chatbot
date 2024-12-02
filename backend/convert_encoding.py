input_file = "/Users/yoonho/Desktop/recipe-chatbot/backend/data/recipes.csv"
output_file = "/Users/yoonho/Desktop/recipe-chatbot/backend/data/recipes_utf8.csv"

# CP949로 읽어서 UTF-8로 저장
with open(input_file, 'r', encoding='cp949', errors='replace') as infile:
    content = infile.read()

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write(content)

print(f"Converted {input_file} to UTF-8 and saved as {output_file}")