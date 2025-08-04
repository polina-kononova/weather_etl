import glob
import os

folder_path = "./data/transform"
pattern = "*.csv"  # шаблон для поиска файлов CSV

files = glob.glob(os.path.join(folder_path, pattern))

if files:
    print(f"Найдено {len(files)} CSV-файлов:")
    for file in files:
        print(f"- {file}")
else:
    print("CSV-файлы не найдены в папке.")
