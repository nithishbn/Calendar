import os
import requests
from bs4 import BeautifulSoup


def get_images():
    r = requests.get("https://lvtemple.org/gallery/")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    count = 0

    for link in soup.find_all('img'):
        count += 1
        image = link.get("src")
        print(image)
        if image != None:
            # question_mark = image.find("?")
            # print("?",question_mark)
            # image = image[:question_mark]
            image_name = os.path.split(image)[1]
            print(image_name)
            r2 = requests.get(image)
            with open("./images/{0}".format(image_name), "wb") as f:
                f.write(r2.content)
        image = link.get("data-src")
        print(image)
        if image != None:
            # question_mark = image.find("?")
            # print("?",question_mark)
            # image = image[:question_mark]
            image_name = os.path.split(image)[1]
            print(image_name)
            r2 = requests.get(image)
            with open("./images/{0}".format(image_name), "wb") as f:
                f.write(r2.content)
    for link in soup.find_all('a'):
        image_data = link.get('data-rel')
        # print(image_data)
        if image_data == None:
            continue
        start = image_data.find("[")
        # print(start)
        end = image_data.find("]")
        image = image_data[start + 1:end ]
        print(image)
    print(count)
get_images()