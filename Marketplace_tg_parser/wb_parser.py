import datetime
import requests
import csv
import json
from fake_useragent import UserAgent


# если пошариться по запросам, закинуть в online-reader json, можно увидеть shard.. или как-то так, для обозначения
# категории при переходе на другие категории. т.е можно все запросы делать с помощью бота - выберите категорию -
# перейти на такую-то ссылку и тд


def get_data_from_url(category=None, size=None):
    """html код страницы"""
    ua = UserAgent()
    headers = {
        "Accept": "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": ua.random,
    }
    cookies = {
        'city': 'ÐÑÐ°ÑÐ½Ð¾ÐºÐ°Ð¼ÑÐºÐÐµÑÐ¼ÑÐºÐ¸Ð¹ ÐºÑÐ°Ð¹, ÐÑÐ°ÑÐ½Ð¾ÐºÐ°Ð¼ÑÐºÐ¸Ð¹ Ñ-Ð½ ÑÐ»Ð¸ÑÐ° '
                'Ð­Ð½ÑÑÐ·Ð¸Ð°ÑÑÐ¾Ð² 19 '
    }
    session = requests.Session()
    category_switcher = {
        'Платья': 'xsubject=69',
        'Сарафаны': 'xsubject=70',
    }
    if category in category_switcher:
        user_size = get_user_size(size)
        url = f'https://catalog.wb.ru/catalog/dresses/v4/filters?appType=1&couponsGeo=2,12,7,3,6,' \
              f'21&curr=rub&dest=-1075831,-115135,-1084695,123586177&emp=0&' \
              f'fsize={user_size}&kind=2&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&regions=64,83,4,38,80,33,70,82,' \
              f'86,30,69,22,66,31,48,1,40&spp=0&stores=117673,122258,122259,117986,1733,117501,507,3158,204939,' \
              f'120762,159402,2737,130744,686,1193,124731,121709&subject=69;70&{category_switcher[category]} '
    elif category == 'Все вместе':
        user_size = get_user_size(size)
        url = f'https://catalog.wb.ru/catalog/dresses/v4/filters?appType=1&couponsGeo=2,12,7,3,6,' \
              f'21&curr=rub&dest=-1075831,-115135,-1084695,123586177&emp=0&' \
              f'fsize={user_size}&kind=2&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&regions=64,83,4,38,80,33,70,82,' \
              f'86,30,69,22,66,31,48,1,40&spp=0&stores=117673,122258,122259,117986,1733,117501,507,3158,204939,' \
              f'120762,159402,2737,130744,686,1193,124731,121709&subject=69;70 '
    data = session.get(url, headers=headers, cookies=cookies)
    with open(f'index.html', 'w', encoding='utf-8') as f:
        f.write(data.text)


def get_user_size(user_size):
    sizes = requests.get('https://catalog.wb.ru/catalog/dresses/v4/filters?appType=1&couponsGeo=2,12,7,3,6,'
                         '21&curr=rub&dest=-1075831,-115135,-1084695,'
                         '123586177&emp=0&kind=2&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&regions=64,83,4,38,80,'
                         '33,70,82,86,30,69,22,66,31,48,1,40&spp=0&stores=117673,122258,122259,117986,1733,117501,'
                         '507,3158,204939,120762,159402,2737,130744,686,1193,124731,121709&subject=69;70').json()
    for size in sizes['data']['filters'][6]['items']:
        if size['name'] == str(user_size):
            size_id = size['id']
            return size_id

    # основная ссылка на платья+сарафаны без фильтра. настраиваем фильтрацию
    # https://catalog.wb.ru/catalog/dresses/v4/filters?appType=1&couponsGeo=2,12,7,3,6,21&curr=rub&dest=-1075831,-115135,-1084695,123586177&emp=0&kind=2&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&regions=64,83,4,38,80,33,70,82,86,30,69,22,66,31,48,1,40&spp=0&stores=117673,122258,122259,117986,1733,117501,507,3158,204939,120762,159402,2737,130744,686,1193,124731,121709&subject=69;70
    # если юзер хочет выбрать размер - добавить к ссылке после параметра 'emp' &fsize=size_id
    # если юзер хочет выбрать категорию - добавить к ссылке в конце &xsubject=user_category, либо предложить не выбирать



def parser(url):
    """основная функция"""
    response = requests.get('https://catalog.wb.ru/catalog/dresses/catalog?appType=1&cardsize=c516x688&couponsGeo=2,'
                            '12,7,3,6,21&curr=rub&dest=-1075831,-115135,-1084695,'
                            '123586177&emp=0&fsize=37404&kind=2&lang=ru&locale=ru&page=1&pricemarginCoeff=1.0&reg=0'
                            '&regions=64,83,4,38,80,33,70,82,86,30,69,22,66,31,48,1,'
                            '40&sort=popular&spp=0&stores=117673,122258,122259,117986,1733,117501,507,3158,204939,'
                            '120762,159402,2737,130744,686,1193,124731,121709&subject=69;70&xsubject=70')
    data = response.json()
    with open(f'index.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return 'ok'



if __name__ == "__main__":
    print(get_user_size(42))

# def city_decoder(s):
#     test_data = 'Краснокамск, Энтузиастов 19'.encode()
#     norm_data = s.encode('ISO-8859-1')
#     return norm_data.decode(), test_data.decode('ISO-8859-1')
