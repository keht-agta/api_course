from urllib.parse import urlencode
from pprint import pprint
from vk import *
from yandex import *
from urllib import parse
import datetime
from tqdm import trange, tqdm
import configparser
import os


def config_read(file_config, part, work_type):
    if work_type == 'config':
        config = configparser.ConfigParser()  # создаём объекта парсера
        config.read(file_config)  # читаем конфиг
        TOKEN = config["VK"]["TOKEN"]
        # if config["VK"]["USER_ID"].isdigit():
        USER_ID= config["VK"]["USER_ID"]
        count = config["VK"]["count"]
        if int(count) < 0  and int(count) >= int(photos_info.get('response', {}).get('count', {})):
            print('Не верное значение кол-ва фото. Значение по умолчанию = 5')
            count = 5
        ya_token = config["YANDEX"]["ya_token"]
        client_id = config["YANDEX"]["client_id"]
        path = config["YANDEX"]["path"]
        if part == 'VK':
            result = TOKEN, USER_ID, count
        elif part == 'YANDEX':
            result = ya_token, path

    elif work_type == 'hand' and part == 'VK':
        print(f"""Ну что ж, продолжим?\nНиже ссылка на страницу ВК. 
              Авторизуйся. Разреши доступ и в ответ отправь полученную адресную строку.\n{url}""")
        # print(url)
        resp = input('Введите ответ:')
        resp = resp[resp.find('#')+1:]
        decode = parse.parse_qs(resp)
        TOKEN = decode.get('access_token',{})[0]
        # USER_ID = decode.get('user_id',{})[0]
        USER_ID = input("Введите имя пользователя, в чьих фоточках мы хотим порыться :):")
        count = input("Чуть не забыл. А сколько фоточек вытаскиваем? По умолчанию 5")
        if int(count) < 0  and int(count) >= int(photos_info.get('response', {}).get('count', {})):
            print('Не верное значение кол-ва фото. Значение по умолчанию = 5')
            count = 5
        result = TOKEN, USER_ID, count
    elif work_type == 'hand' and part == 'YANDEX':
        print(f"Перейдите по ссылке {yandex_oauth_url}")
        ya_token = input('Введите ответ:')
        path = input("Укажите директорию куда Вам сохранить фото:")
        result = ya_token, path
    return result


if __name__ == '__main__':
    file_config = input("""Привет. Введи название конфигурационного файла, если не найду то будем ручками вводить. Не переживай это не страшно :)""")
    if (os.path.isfile (file_config) and '' not in config_read(file_config, 'VK','config')
        not in config_read(file_config, 'YANDEX','config')):
        # TOKEN, USER_ID, count = config_read(file_config, 'VK')
        work_type = 'config'
        print("Конфигурационный файл найден, программа переведена в автоматический режим работы. Ожидайте.")
    else:
        print("Что-то пошло не так. Мы уже разбираемся. Но пока прийдется вручную ввести данные")
        work_type = 'hand'
    # VK формируем список с кол-во лайков, тип размера, ссылкой и датой фото
    TOKEN, USER_ID, count = config_read(file_config, part='VK', work_type=work_type)
    vk_client = VKAPIClient(TOKEN, user_id=USER_ID)
    photos_info = vk_client.get_profile_photos()
    photo_list = photos_info.get('response', {}).get('items')
    photo_list_url = []
    for photo in photo_list:
        photo_list_url_ = [photo.get('likes', {}).get('count', {}),
            photo.get('sizes' , {})[-1].get('type',{}), 
            photo.get('sizes' , {})[-1].get('url',{}),
            datetime.datetime.fromtimestamp(photo.get('date', {})).strftime('%Y-%m-%d')]
        photo_list_url.append(photo_list_url_)  
    # YANDEX Создаем папку и записываем файлы на яндекс диск
    ya_token, path = config_read(file_config, part='YANDEX', work_type=work_type)
    yadisk_client = YANDEXAPIClient(ya_token)
    yadisk_client.create_folder(path)
    # Формируем файл json и список имен файлов
    file_json=[]
    file_name_list = []
    for i in tqdm(range(int(count))): #Делаем прогресс бар по кол-ву фото
        file_dict = {}
        file_dict['file_name'] = f"{photo_list_url[i][0]}.jpg"
        file_dict['size'] = photo_list_url[i][1]
        photo_url = photo_list_url[i][2]
        file_name = f"{path}/{file_dict.get('file_name', {})}"
        # Проверка на повторяемость имен файлов
        if file_name in file_name_list:
            file_dict.update(file_name=f"{photo_list_url[i][3]}_{file_dict.get('file_name', {})}") 
            file_name = file_dict['file_name']
        file_name_list.append(file_name)
        file_json.append(file_dict)
        yadisk_client.upload_files(file_name_list[i],photo_list_url[i][2])
    print(f'Не желаете посмотреть результат? https://disk.yandex.ru/client/disk/{path}')
    rate = input("Оцените работу от 1 до 5. ")
    print('Спасибо')
    pprint(file_json)
