import telebot
from loguru import logger
from TRIOL2_lib import Product
from CONFIG import TOKEN
from CONFIG import LogError
from CONFIG import LogInfo

import time

bot = telebot.TeleBot(TOKEN)
logger.add(LogError, format="{time} {level} {message}", level='ERROR')
logger.add(LogInfo, format="{time} {level} {message}", level='INFO')

@bot.message_handler(content_types=["text"])
def send_info_product(message):

    id_item = message.text

    if len(id_item) > 8:
        # Ограничение на длину id товара более 9 знаков
        bot.send_message(message.chat.id, 'Товар не найден' )
        logger.error('Превышена максимальная длинна артикула: %s' % id_item)
        return None  # прекращаем обработку артикула, что бы избежать обращения к БД

    if not id_item.isdigit():
        bot.send_message(message.chat.id, 'Товар не найден' )
        logger.error('Неверный формат артикула: %s' % id_item )
        return None  # прекращаем обработку артикула, что бы избежать обращения к БД
    start = time.time()
    item = Product(id_item)
    logger.info('Поиск артикула: %s' % id_item)
    logger.info('Запрос к БД занял: %f' % -(start - time.time()))

    if item.name:
        bot.send_message(message.chat.id, '\n'.join([item.name, item.description]))
        logger.info('Описание отправлено')

    else:
        bot.send_message(message.chat.id, 'Товар не найден')
        logger.error('Не найдено описание для артикул: %s' % id_item)
        return None #прекращаем обработку артикула, что бы избежать обращения к БД для поика картинки

    if item.image:
        bot.send_photo(message.chat.id, item.image[0])
        logger.info('Изображение отправлено')
    else:
        logger.error('Не найдено изображение дял артикула: %s' % id_item)


if __name__ == '__main__':
    bot.infinity_polling()
