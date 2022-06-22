import asyncio
import datetime
import json
import asyncio.proactor_events
from aiocsv import AsyncWriter
import aiofiles
import aiohttp
from fake_useragent import UserAgent


async def get_data_from_url(category=None, size=None):
    """html код страницы"""
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()
    headers = {
        "Accept": "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": ua.random,
        "Content-Type": "text/plain; charset=utf-8"
    }
    cookies = {
        'city': 'ÐÑÐ°ÑÐ½Ð¾ÐºÐ°Ð¼ÑÐºÐÐµÑÐ¼ÑÐºÐ¸Ð¹ ÐºÑÐ°Ð¹, ÐÑÐ°ÑÐ½Ð¾ÐºÐ°Ð¼ÑÐºÐ¸Ð¹ Ñ-Ð½ ÑÐ»Ð¸ÑÐ° '
                'Ð­Ð½ÑÑÐ·Ð¸Ð°ÑÑÐ¾Ð² 19 '
    }
    category_switcher = {
        'Платья': 'xsubject=69',
        'Сарафаны': 'xsubject=70',
    }
    user_size = 37404
    if category in category_switcher:
        url = f'https://catalog.wb.ru/catalog/dresses/catalog?appType=1&couponsGeo=2,12,7,3,6,' \
              f'21&curr=rub&dest=-1075831,-115135,-1084695,123586177&emp=0&' \
              f'fsize={user_size}&kind=2&lang=ru&locale=ru&page=1&pricemarginCoeff=1.0&reg=0&regions=64,83,4,38,80,' \
              f'33,70,82,86,30,69,22,66,31,48,1,40&sort=popular&spp=0&subject=69;70&{category_switcher[category]}'
    # elif category == 'Все вместе':
    #     # user_size = await get_user_size(size)
    #     url = f'https://catalog.wb.ru/catalog/dresses/catalog?appType=1&couponsGeo=2,12,7,3,6,21&curr=rub&dest=-1075831,-115135,-1084695,123586177&emp=0&fsize={user_size}&kind=2&lang=ru&locale=ru&page=1&pricemarginCoeff=1.0&reg=0&regions=64,83,4,38,80,33,70,82,86,30,69,22,66,31,48,1,40&sort=popular&spp=0&subject=69;70'
    async with aiohttp.ClientSession() as session:

        async with session.get(url, headers=headers, cookies=cookies) as resp:
            formatted_data = []
            raw = await resp.read()
            content = json.loads(raw)
            for card in content['data']['products']:
                card_id = card.get('id')
                card_name = card.get('name')
                card_brand = card.get('brand')
                card_price = card.get('priceU') / 100
                card_discount_price = card.get('salePriceU') / 100
                for s in card.get('sizes'):
                    if str(size) in s.get('origName'):
                        card_size = size
                        break
                card_link = f'https://www.wildberries.ru/catalog/{card_id}/detail.aspx?targetUrl=GP'
                formatted_data.append(
                    [card_id, card_name, card_brand, card_price, card_discount_price, card_size, card_link])

        # Добавить переменные с нужными категориями, чтобы красиво записывать в .csv файл с помощью aiocsv..
        async with aiofiles.open(f'Katya_{card_name}_{cur_time}.csv', 'w', encoding='UTF-8') as file:
            writer = AsyncWriter(file)

            await writer.writerow(
                [
                    'Артикул',
                    'Категория',
                    'Бренд',
                    'Цена без скидки',
                    'Цена со скидкой',
                    'Размер',
                    'Ссылка на товар'
                ]
            )
            await writer.writerows(formatted_data)


async def get_user_size(user_size):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://catalog.wb.ru/catalog/dresses/v4/filters?appType=1&couponsGeo=2,12,7,3,6,'
                             '21&curr=rub&dest=-1075831,-115135,-1084695,'
                             '123586177&emp=0&kind=2&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&regions=64,83,4,38,80,'
                             '33,70,82,86,30,69,22,66,31,48,1,40&spp=0&stores=117673,122258,122259,117986,1733,117501,'
                             '507,3158,204939,120762,159402,2737,130744,686,1193,124731,121709&subject=69;70') as sizes:
            raw = await sizes.read()
            content = json.loads(raw)
            for size in content['data']['filters'][6]['items']:
                if size['name'] == str(user_size):
                    size_id = size['id']
                    return size_id


# def silence_event_loop_closed(func):
#     # Заглушил исключение 'Event loop is closed'
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         try:
#             return func(self, *args, **kwargs)
#         except RuntimeError as e:
#             if str(e) != 'Event loop is closed':
#                 raise
#     return wrapper

async def main():
    await get_data_from_url("Сарафаны", 42)


if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(get_data_from_url("Сарафаны", 42))
    # if platform.system() == 'Windows':
    #     _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
    # print(asyncio.get_event_loop_policy())
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # print(asyncio.get_event_loop_policy())
    asyncio.run(main())

