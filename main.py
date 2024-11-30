import requests  # Импортируем библиотеку requests для выполнения HTTP-запросов
from bs4 import BeautifulSoup as bs  # Импортируем BeautifulSoup из библиотеки bs4 для парсинга HTML
import json  # Импортируем библиотеку json для работы с JSON-данными

url = 'https://news.ycombinator.com/'  # Указываем URL-адрес сайта Hacker News
response = requests.get(url)  # Выполняем GET-запрос к указанному URL и сохраняем ответ в переменной response
if response.status_code != 200:  # Проверяем, успешен ли запрос (код 200 означает успех)
    print(f"Ошибка при запросе к сайту: {response.status_code}")  # Если нет, выводим сообщение об ошибке
    exit()  # Завершаем выполнение программы

soup = bs(response.text, 'html.parser')  # Создаем объект BeautifulSoup для парсинга HTML-кода страницы

rows = soup.find_all('tr', class_='athing')  # Находим все строки таблицы с классом 'athing'
print(f"Найдено строк таблицы: {len(rows)}")  # Выводим количество найденных строк

list_titles = []  # Создаем пустой список для хранения заголовков новостей
list_comments = []  # Создаем пустой список для хранения количества комментариев

for row in rows:  # Проходим по каждой строке таблицы
    title_tag = row.select_one('span.titleline > a')  # Находим элемент заголовка новости
    if title_tag:  # Если элемент найден
        title = title_tag.get_text(strip=True)  # Получаем текст заголовка, убирая лишние пробелы
        list_titles.append(title)  # Добавляем заголовок в список
    else:  # Если элемент не найден
        list_titles.append("No title")  # Добавляем "No title" в список заголовков
    
    subtext_row = row.find_next_sibling('tr')  # Находим следующую строку, которая содержит дополнительные данные
    if subtext_row:  # Если следующая строка найдена
        subtext = subtext_row.find('td', class_='subtext')  # Находим элемент с классом 'subtext'
        if subtext:  # Если элемент найден
            comments_tag = subtext.find_all('a')[-1]  # Находим последний элемент 'a', который содержит количество комментариев
            if comments_tag and 'comment' in comments_tag.get_text():  # Проверяем, что элемент существует и содержит слово 'comment'
                comments = comments_tag.get_text(strip=True).split()[0]  # Получаем текст и извлекаем количество комментариев
            else:  # Если элемент не найден или не содержит 'comment'
                comments = '0'  # Устанавливаем количество комментариев в 0
        else:  # Если элемент 'subtext' не найден
            comments = '0'  # Устанавливаем количество комментариев в 0
    else:  # Если следующая строка не найдена
        comments = '0'  # Устанавливаем количество комментариев в 0
    list_comments.append(comments)  # Добавляем количество комментариев в список

for i in range(len(list_titles)):  # Проходим по индексам заголовков
    print(f"{i + 1}. Title: {list_titles[i]}; Comments: {list_comments[i]};")  # Выводим заголовок и количество комментариев

file_json = "data.json"  # Указываем имя файла для сохранения данных в формате JSON
writer_list = []  # Создаем пустой список для хранения словарей с заголовками и комментариями

for i in range(len(list_titles)):  # Проходим по индексам заголовков
    writer = {'Title': list_titles[i], 'Comments': list_comments[i]}  # Создаем словарь с заголовком и количеством комментариев
    writer_list.append(writer)  # Добавляем словарь в список

print("Записываем данные в файл data.json")  # Выводим сообщение о начале записи данных в файл
with open(file_json, "w", encoding='utf-8') as file:  # Открываем файл для записи с кодировкой UTF-8
    json.dump(writer_list, file, indent=4, ensure_ascii=False)  # Записываем данные в файл в формате JSON с отступами

print("Проверяем содержимое файла data.json:")  # Выводим сообщение о проверке содержимого файла
with open(file_json, "r", encoding='utf-8') as file:  # Открываем файл для чтения с кодировкой UTF-8
    data = json.load(file)  # Загружаем данные из файла в переменную data
    print(json.dumps(data, indent=4, ensure_ascii=False))  # Выводим содержимое файла в формате JSON с отступами

file_index = "index.html"  # Указываем имя файла для сохранения HTML-страницы

with open(file_index, "w", encoding='utf-8') as file:  # Открываем файл для записи с кодировкой UTF-8
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
""")  # Записываем начальную часть HTML-кода в файл

    with open(file_json, "r", encoding='utf-8') as input_file:  # Открываем файл JSON для чтения
        data_writer = json.load(input_file)  # Загружаем данные из файла в переменную data_writer
        for i, item in enumerate(data_writer):  # Проходим по элементам данных
            file.write(f"<tr><td>{item['Title']}</td><td>{item['Comments']}</td><td>{i + 1}</td></tr>\n")  # Записываем строки таблицы с заголовками и комментариями

    file.write("""  # Записываем завершающую часть HTML-кода в файл
    </table>
    <p style="text-align: center;"><a href="https://news.ycombinator.com/">Источник данных</a></p>
</body>
</html>
""")

print("HTML файл создан: index.html")  # Выводим сообщение о завершении создания HTML-файла