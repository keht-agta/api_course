from urllib.parse import urlencode
from pprint import pprint
from vk import *
from yandex import *
from urllib import parse
import datetime
from tqdm import trange, tqdm



if __name__ == '__main__':
    print('ПРивет!!! Давай поработаем\nНиже ссылка на страницу ВК. Авторизуйся. Разреши доступ и в ответ отправь полученную адресную строку.')
    print(url)
    resp = input('Введите ответ:')
    resp = resp[resp.find('#')+1:]
    decode = parse.parse_qs(resp)
    TOKEN = decode.get('access_token',{})[0]
    USER_ID = decode.get('user_id',{})[0]
    if TOKEN:
        vk_client = VKAPIClient(TOKEN, user_id=USER_ID)
        print(f'{vk_client.get_user_name()}, чем могу быть полезен? Пошаримся по фоткам?')
        photos_info = vk_client.get_profile_photos()
        print(f"У Вас в профиле {photos_info.get('response', {}).get('count', {})} фотографий")
        count = int(input('Сколько фотографйи Вы хотите сохранить?:'))
        if int(count) < 0  and int(count) >= int(photos_info.get('response', {}).get('count', {})):
            print('Не верное значение. Значение по умолчанию = 5')
            count = 5
        photo_list = photos_info.get('response', {}).get('items')
        photo_list_url = [[photo.get('likes', {}).get('count', {}),
                        photo.get('sizes' , {})[-1].get('type',{}), 
                        photo.get('sizes' , {})[-1].get('url',{}),
                        datetime.datetime.fromtimestamp(photo.get('date', {})).strftime('%Y-%m-%d')] 
                        for photo in photo_list][0:count]
        file_json=[]
        file_name_list = []
        for i in tqdm(range(count)): #Делаем прогресс бар по кол-ву фото
            file_dict = {}
            file_dict['file_name'] = f"{photo_list_url[i][0]}.jpg"
            file_dict['size'] = photo_list_url[i][1]
            photo_url = photo_list_url[i][2]
            file_name = f"files/{file_dict.get('file_name', {})}"
            if file_name in file_name_list:
                file_dict.update(file_name=f"{photo_list_url[i][3]}_{file_dict.get('file_name', {})}") 
                # file_name = f"files/{photo_list_url[i][3]}_{file_dict.get('file_name', {})}"
                file_name = file_dict['file_name']
            file_name_list.append(file_name)
            file_json.append(file_dict)
            with open(file_name, 'wb') as f:
                f.write(requests.get(photo_url).content)
        print("""Ваши фотографии скачалиь на компьютер.\n
              Загрузим на Яндекс диск? Переходите по ссылке""")
        print(yandex_oauth_url)
        ya_token = input('Введите ответ:')
        yadisk_client = YANDEXAPIClient(ya_token)
        print('Загружаем файлы на яндекс диск в папку files')
        yadisk_client.create_folder('files')
        for i in tqdm(range(count)): #Делаем прогресс бар по кол-ву фото
            yadisk_client.upload_files(file_name_list[i],photo_list_url[i][2])
        print('Не желаете посмотреть результат? https://disk.yandex.ru/client/disk/files')
        rate = input("Оцените работу от 1 до 5. ")
        print('Спасибо')

        pprint(file_json)
