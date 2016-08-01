import time
import datetime
from PySide.QtCore import *
from PySide.QtGui import *
import ui
import json
import requests
import vk
import vk_api
import os
from PySide import QtCore, QtGui
from addPostLibs import get

class exampleWindowClass(QWidget, ui.Ui_AddPostVK):
    def __init__(self):
        super(exampleWindowClass, self).__init__()
        self.setupUi(self)

        # self.generate_b.clicked.connect(self.testDef)
        self.imgUrl_b.clicked.connect(self.get_img_urt)
        self.url_b.clicked.connect(self.get_inf_from_url)

        self.post_data = ''
        self.img_url = ''
        self.year_le.setText(time.strftime("%Y"))
        self.month_le.setText(time.strftime("%m"))
        self.day_le.setText(time.strftime("%d"))
        self.hour_le.setText(time.strftime("%H"))
        self.minut_le.setText(time.strftime("%M"))

        #del##########################################
        self.login_le.setText('Login')
        self.password_le.setText('Pass')
        self.id_group_l.setText('IDg')


        #authorization##########################################
        self.status = 'OFF'
        self.login = ''
        self.password = ''
        self.access_token = ''
        self.user_id = ''
        self.autorization_b.clicked.connect(self.aut_click)

        #add post##########################################
        self.send_b.clicked.connect(self.send_click)

    #authorization##########################################
    def get_token(self):
        print('---def get_token---')

        try:
            f = open('vk_config.json')
            d = json.loads(f.read())
            self.access_token =  d[self.login]['token']['access_token']
            self.user_id = d[self.login]['token']['user_id']
            print('---def get_token: OK---')
        except:
            print("Can't read vk_config.json")
            print('---def get_token: ERROR---')

    # попытка авторизации
    def vk_auth(self, login, password):
        print('###')
        print('Запуск функции: vk_auth')
        print('###')
        ###
        print(login, password)
        print('---def vk_auth---')
        vk = vk_api.VkApi(login, password)
        try:
            vk.authorization()
            self.status_l.setText('Now you are logged in!')
            self.status = 'ON'
            self.login = login
            self.password = password
            self.get_token()
            ###
            print()
            print('\tРезультат выполнения:')
            print('\tself.status =', self.status)
            print('\tself.login =', self.login)
            print('\tself.passwor =', self.password)
            print()
            print()
            ###
        except:
            self.status_l.setText('Authorisation Error! Check your data and access to the Internet!')
            self.status = 'OFF'
            ###
            print()
            print('\tФункция завершилась с ошибкой!')
            print()
            print()
    # попытка авторизации #

    # удаление старых данны авторизации
    def cleaning_authorization_inf(self):
        print('###')
        print('Запуск функции: cleaning_authorization_inf')
        print('###')
        ###
        self.login = ''
        self.password = ''
        self.access_token = ''
        self.user_id = ''
        ###
        print()
        print('\tРезультат выполнения:')
        print('\tself.login =', self.login)
        print('\tself.password =', self.password)
        print('\tself.access_token =', self.access_token)
        print('\tself.user_id =', self.user_id)
        print()

    # удаление старых данны авторизации #

    def aut_click(self):
        print('---def aut_click---')

        self.cleaning_authorization_inf()

        login = self.login_le.text()
        password = self.password_le.text()
        self.vk_auth(login, password)
    #add post##########################################
    def send_click(self):
        # print('---def send_click---')
        text = self.title_l.text() + '\n\n' + self.tegs_l.text() + '\n\n' + self.text_t.toPlainText() + '\n\n' + self.url_le.text()
        self.get_post_data()
        data = self.post_data

        #Проверка авторизации
        if self.status == 'OFF':
            self.send_status_l.setText("NOT AUTHORIZATION!")
        else:
            self.send_status_l.setText("")
        #Проверка авторизации

        method_url = ''
        print('----------')
        print(self.imgUrl_le.text(), type(self.imgUrl_le.text()))
        print('----------')
        # if self.img_url != '':
        if self.imgUrl_le.text() != '':
            # путь к вашему изображению
            # img = {'photo': (self.img_url, open(self.img_url, 'rb'))}
            img = {'photo': (self.imgUrl_le.text(), open(self.imgUrl_le.text(), 'rb'))}
            # Получаем ссылку для загрузки изображений
            method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
            data = dict(access_token=str(self.access_token), gid=self.id_group_l.text())
            response = requests.post(method_url, data)
            result = json.loads(response.text)
            upload_url = result['response']['upload_url']
            # Загружаем изображение на url
            response = requests.post(upload_url, files=img)
            result = json.loads(response.text)
            # Сохраняем фото на сервере и получаем id
            method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
            data = dict(access_token=str(self.access_token), gid=self.id_group_l.text(), photo=result['photo'], hash=result['hash'], server=result['server'])
            response = requests.post(method_url, data)
            result = json.loads(response.text)['response'][0]['id']
            # Теперь этот id остается лишь прикрепить в attachments метода wall.post
            method_url = 'https://api.vk.com/method/wall.post?'
            data = dict(access_token=str(self.access_token), owner_id='-' + self.id_group_l.text(), attachments=result, message=text, publish_date=self.post_data)
        else:
            method_url = 'https://api.vk.com/method/wall.post?'
            data = dict(access_token=str(self.access_token), owner_id='-' + self.id_group_l.text(), message=text, publish_date=self.post_data)
        response = requests.post(method_url, data)
        result = json.loads(response.text)

        r = result.get('error')
        if r == None:
            self.send_status_l.setText("POST SEND!", time.strftime("%M"))
        else:
            self.send_status_l.setText("ERROR SEND!", time.strftime("%M"))

        # очистка
        get.ALL_TEXT = ''
        get.TITLE_TEXT = ''
        get.BODY_TEXT = ''
        self.title_l.setText('')
        self.text_t.setText('')
        self.tegs_l.setText('')
        self.imgUrl_le.setText('')

    def get_post_data(self):
        year = int(self.year_le.text())
        month = int(self.month_le.text())
        day = int(self.day_le.text())
        hour = int(self.hour_le.text())
        minut = int(self.minut_le.text())
        d = datetime.datetime(year, month, day, hour, minut, 0)
        data = d.strftime("%s")
        data = str(data)
        self.post_data = data

    def get_img_urt(self):
        path, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.basename('.'))
        path = path.split("/")
        self.imgUrl_le.setText(str(path[-1]))
        self.img_url = str(path[-1])

    def get_inf_from_url(self):
        print('###')
        print('Запуск функции: cleaning_authorization_inf')
        print('###')
        ###
        try:
            # вся страница
            get.ALL_TEXT = get.all_page(self.url_le.text())
            # заголовок
            get.TITLE_TEXT = get.post_title(self.url_le.text())
            self.title_l.setText(get.TITLE_TEXT)
            #текст
            get.BODY_TEXT = get.post_text(self.url_le.text())
            self.text_t.setText(get.BODY_TEXT)
            # теги
            tegs = get.post_tegs(self.url_le.text())
            self.tegs_l.setText(tegs)
            # картинка
            self.img_url = get.post_img('http://nnmclub.to/forum/viewtopic.php?t=964634')
            # self.img_url = get.post_img(self.url_le.text())
            self.imgUrl_le.setText(self.img_url)

            self.send_status_l.setText("OK URL!" + time.strftime("%M"))
        except:
            self.send_status_l.setText("ER URL!" + time.strftime("%M"))
            ###
            print('\tОшибка, проверьте url')
        print()


        #     #заголовок
        # title = get.post_title(self.url_le.text())
        # self.title_l.setText(title)
        #     #теги
        # tegs = get.post_tegs(self.url_le.text())
        # self.tegs_l.setText(tegs)
        #     #картинка
        # img_u = get.post_img(self.url_le.text())
        # self.img_url = img_u
        # self.imgUrl_le.setText(img_u)
        # #     #текст
        # text = get.post_text(self.url_le.text())
        # self.text_t.setText(text)

if __name__ == '__main__':
    app = QApplication([])
    w = exampleWindowClass()
    w.show()
    app.exec_()