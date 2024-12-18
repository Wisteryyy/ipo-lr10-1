import requests
from bs4 import BeautifulSoup
import json

url = 'https://news.ycombinator.com/'

response = requests.get(url)
if response.status_code != 200:
    print(f"Ошибка при запросе к сайту: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find_all('tr', class_='athing')

print(f"Найдено строк таблицы: {len(rows)}")

list_titles = []
list_comments = []
for row in rows:
    title_tag = row.select_one('span.titleline > a')
    if title_tag:
        title = title_tag.get_text(strip=True)
        list_titles.append(title)
    else:
        list_titles.append("No title")
    
    subtext_row = row.find_next_sibling('tr')
    if subtext_row:
        subtext = subtext_row.find('td', class_='subtext')
        if subtext:
            comments_tag = subtext.find_all('a')[-1]
            if comments_tag and 'comment' in comments_tag.get_text():
                comments = comments_tag.get_text(strip=True).split()[0]
            else:
                comments = '0'
        else:
            comments = '0'
    else:
        comments = '0'
    list_comments.append(comments)

for i in range(len(list_titles)):
    print(f"{i + 1}. Title: {list_titles[i]}; Comments: {list_comments[i]};")

file_json = "data.json"
writer_list = []

for i in range(len(list_titles)):
    writer = {'Title': list_titles[i], 'Comments': list_comments[i]}
    writer_list.append(writer)

print("Записываем данные в файл data.json")
with open(file_json, "w", encoding='utf-8') as file:
    json.dump(writer_list, file, indent=4, ensure_ascii=False)

print("Проверяем содержимое файла data.json:")
with open(file_json, "r", encoding='utf-8') as file:
    data = json.load(file)
    print(json.dumps(data, indent=4, ensure_ascii=False))

file_index = "index.html"

with open(file_index, "w", encoding='utf-8') as file:
    file.write("""<html>
<head>
    <title>Hacker News</title>
    <style>
        body {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            background-color: #fff;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Hacker News Top Stories</h1>
    <table>
        <tr>
            <th>Title</th>
            <th>Comments</th>
            <th>Number</th>
        </tr>
""")

    with open(file_json, "r", encoding='utf-8') as input_file:
        data_writer = json.load(input_file)
        for i, item in enumerate(data_writer):
            file.write(f"<tr><td>{item['Title']}</td><td>{item['Comments']}</td><td>{i + 1}</td></tr>\n")

    file.write("""
    </table>
    <p style="text-align: center;"><a href="https://news.ycombinator.com/">Источник данных</a></p>
</body>
</html>
""")

print("HTML файл создан: index.html")
