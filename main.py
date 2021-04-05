from TRIOL2_lib import Product
import telebot
from CONFIG import TOKEN

import time

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=["text"])
def send_info_product(message):
    start = time.time()
    id_item = message.text
    if len(id_item) > 9:
        # Ограничение на длину id товара более 9 знаков
        return 0
    item = Product(id_item)
    bot.send_message(message.chat.id, '\n'.join([item.name, item.description]))
    bot.send_photo(message.chat.id, item.image[0])
    print(time.time() - start)

if __name__ == '__main__':
    bot.infinity_polling()