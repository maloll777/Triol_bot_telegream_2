import requests
import sqlite3
from CONFIG import DataBase

class Triol:
    # класс для работы с amma.pet и добавления данных о товаре в БД
    def __init__(self, item):
        self.id_item = item
        self.link = self.get_page_product_amma()
        if self.link:
            self.name, self.description, self.image = self.get_info_item_amma()
        else:
            self.name = 'Товар не найден'

    def get_page_product_amma(self):
        # поиск товара по id на сайте amma.pet
        # возвращает адрес старницы с товаром

        page = requests.post('https://amma.pet/search/?q=' + self.id_item)

        if 'По вашему запросу ничего не найдено' in page.text:
            return None

        for page_line in page.text.replace('>', '>\n').split():

            if 'href="/product' in page_line:
                return 'https://amma.pet' + page_line[6:-1]

    def get_info_item_amma(self):
        # сбор информации о товаре со траницы

        text: str = requests.post(self.link).text \
            .replace('<', '\n<') \
            .replace('>', '>\n').replace('&quot;', '')

        text = text[text.find('Главная'):text.find('Торговая марка')].splitlines()

        # чистим страницу от мусора
        text = [i for i in text if len(i) > 7 and
                i != '' and
                '</' not in i and
                "90x130_q90.jpg" not in i and
                'class' not in i]

        for i, val in enumerate(text):
            if 'jpg' not in val:
                continue
            text[i] = val[14:-2]

        return text[-3], text[-2], ['https://amma.pet/' + i for i in text if 'jpg' in i]


class Product(Triol):

    def __init__(self, item):
        self.id_item = item
        self.name, self.description = self.get_info_db()
        self.image = self.get_image_db()

    def get_info_db(self):
        # Ищет информацию в БД

        con = sqlite3.connect(DataBase)
        cursor = con.cursor()
        cursor.execute('select name, description FROM Product where item_number = ' + self.id_item)
        try:
            out = cursor.fetchall()[0]
        except IndexError:
            return 'Описание товара не найдено'

        return out

    def get_image_db(self):
        # ищет фото торава по id
        con = sqlite3.connect(DataBase)
        cursor = con.cursor()

        cursor.execute('SELECT Image FROM Image WHERE item_number =' + self.id_item)
        return cursor.fetchone()
