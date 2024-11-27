import parameters
import requests
import json
from bs4 import BeautifulSoup

counter = 0
parser = BeautifulSoup(requests.get(parameters.link_to_parse).content, features="html.parser")
teachers = parser.find_all("div", class_="content taj")
json_list = list()
json_file = open("data.json", "w", encoding="utf-8")
for teacher in teachers:
    counter += 1
    name = teacher.find_next("h3").contents[0]
    post = teacher.find_next("li", class_="tss").contents[0][11:]
    json_list.append({"teacher": f"{name}", "post": f"{post}"})
    print(f"{counter}. Teacher: {name}; Post: {post}")
json.dump(json_list, json_file, indent=4, ensure_ascii=False)
json_file.close()
parser = BeautifulSoup(parameters.sample_html_output, features="html.parser")
json_file = json.load(open("data.json", "r", encoding='utf-8'))
table = parser.table
head_element = parser.new_tag("th")
head_element.string = parameters.header_teachear_text
header_table = parser.new_tag("tr")
header_table.append(head_element)
head_element = parser.new_tag("th")
head_element.string = parameters.header_post_text
header_table.append(head_element)
table.append(header_table)
for json_object in json_file:
    table_element_parent = parser.new_tag("tr")
    teacher_name = parser.new_tag("td")
    teacher_post = parser.new_tag("td")
    teacher_name.string = json_object['teacher']
    teacher_post.string = json_object['post']
    table_element_parent.append(teacher_name)
    table_element_parent.append(teacher_post)
    table.append(table_element_parent)
data_original = parser.new_tag("tr")
data_text = parser.new_tag("th")
data_text.string = parameters.original_data_text
data_original.append(data_text)
data_text = parser.new_tag("th")
link = parser.new_tag("a", href=parameters.link_to_parse)
link.string = "Перейти"
data_text.append(link)
data_original.append(data_text)
table.append(data_original)
with open("index.html", "w", encoding='utf-8') as index:
    index.write(parser.prettify(formatter="minimal"))