#
# Скрипт на Python для запуска локального сервера
# на примере сайта пекарни
#
# задача: добавить новую булочку
#

# pip install legacy-cgi

import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer

items = [
    {
        "name": "Вкусная булочка 1",
        "desc": "Описание вкусной булочки",
        "link": "item-1",
        "img": "first.jpg",
        "price": 200,
    },
    {
        "name": "Вкусная булочка 2",
        "desc": "Описание вкусной булочки",
        "link": "item-2",
        "img": "second.jpg",
        "price": 300,
    },

    # [ЗАДАЧА 1] Добавить объект 3 булочки
]

def get_source_image(path_to_pic):
        f = open(path_to_pic, 'rb')
        return f.read()

def show_items():
    res = ""
    for i in range(len(items)):
        res += """
            <div class="item">
                <img src='/img/""" + items[i]["img"] + """' />
                <h3>""" + items[i]["name"] + """</h3>
                <p>""" + items[i]["desc"] + """</p>
                <span>""" + str(items[i]["price"]) + """</span>
                <a href="/""" + items[i]["link"] + """">Открыть</a>
            </div>
        """
    return res

class WebServerHandler(BaseHTTPRequestHandler):
        def do_GET(self):

                # Главная страница
                if self.path.endswith("/"):
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                        self.end_headers()
                        output = """
                        <html>
                        <head>
                        <title>Сайт пекарни</title>
                        <meta charset="utf8">
                        <style>
                            .items {
                                display: flex;
                                flex-wrap: wrap;
                                gap: 16px;
                            }

                            .item {
                                width: 200px;
                                border: 1px solid #ccc;
                                border-radius: 24px;
                                padding: 12px;
                                display: flex;
                                flex-direction: column;
                            }

                            .item img {
                                width: 100%;
                                border-radius: 12px;
                            }
                        </style>
                        </head>
                        <body>
                        <h1>Добро пожаловать на сайт пекарни «Вкусняш»!</h1>
                        <p>Пожалуйста, выберите изделие из представленных:</p>
                        <div class="items">""" + show_items() + """</div>
                        </body>
                        </html>
                        """
                        self.wfile.write(output.encode("utf8"))
                        return

                # Страница любой булочки
                for item in items:
                    if self.path == "/" + item["link"]:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                        self.end_headers()
                        output = """
                        <html>
                        <head><title>""" + item["name"] + """</title><meta charset="utf8"></head>
                        <body>
                        <img src='/img/""" + item["img"] + """' width='300'>
                        <h1>""" + item["name"] + """</h1>
                        <p>""" + item["desc"] + """</p>
                        <span>""" + str(item["price"]) + """ ₽</span><br>
                        <a href="/">Назад</a>
                        </body>
                        </html>
                        """
                        self.wfile.write(output.encode("utf8"))
                        return

                # Любая картинка
                for item in items:
                    if self.path == "/img/" + item["img"]:
                        self.send_response(200)
                        self.send_header('Content-type', 'image/jpeg')
                        self.end_headers()
                        self.wfile.write(get_source_image("./img/" + item["img"]))
                        return

#
# Запуск сервера
#

port = 8000
server = HTTPServer(('', port), WebServerHandler)
print("Web Server running on port: "+str(port))
server.serve_forever()
