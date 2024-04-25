from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import sqlite3
import random

BOT_API = '6697550537:AAF7VWU2ZIJqlZa837zoNQrJrEwUaJJWizQ'


def start(update, context):
    update.message.reply_text("Здравствуйте! Сегодня я ваш шеф-повар. Чтобы узнать, чем я могу вам помочь,"
                              " используйте команду /help")


def help(update, context):
    update.message.reply_text("/breakfast — список блюд на завтрак, которые станут ярким началом вашего дня\n"
                              "/first — салаты и супы, отлично подходящие для начала застолья\n"
                              "/second — основные блюда\n"
                              "/snacks — закуски, если день полон интересных событий, "
                              "и времени на готовку остается немного\n"
                              "/drinks — напитки, прекрасно дополняющие вашу трапезу\n"
                              "/recipe <блюдо/напиток> — ссылка на подробный рецепт приглянувшегося вам "
                              "блюда или напитка\n"
                              "/random_meal — я составлю для вас комплексный прием пищи на свой вкус\n"
                              "/random_snack — когда у вас нет времени даже на подумать, я готов помочь вам в выборе"
                              "легкого перекуса\n"
                              "/advice — моя личная рекомендация\n"
                              "/music — музыкальный плейлист, делающий процесс готовки еще приятней")


def breakfast(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT dish, time FROM breakfast ORDER BY time")
    dishes = cursor.fetchall()

    conn.close()

    message = 'Список блюд на завтрак:\n' + "\n".join(
        [f'"{dish.capitalize()}", время на приготовление — {time}мин.' for dish, time in dishes])
    update.message.reply_text(message)


def first(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT dish, time FROM first ORDER BY time")
    dishes = cursor.fetchall()

    conn.close()

    message = 'Список блюд на первое:\n' + "\n".join(
        [f"{dish.capitalize()}, время на приготовление — {time}мин." for dish, time in dishes])
    update.message.reply_text(message)


def second(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT dish, time FROM second ORDER BY time")
    dishes = cursor.fetchall()

    conn.close()

    message = 'Список блюд на второе:\n' + "\n".join(
        [f"{dish.capitalize()}, время на приготовление — {time}мин." for dish, time in dishes])
    update.message.reply_text(message)


def drinks(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT dish, time FROM drinks ORDER BY time")
    dishes = cursor.fetchall()

    conn.close()

    message = 'Список напитков:\n' + "\n".join(
        [f"{dish.capitalize()}, время на приготовление — {time}мин." for dish, time in dishes])
    update.message.reply_text(message)


def snacks(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT dish, time FROM drinks ORDER BY time")
    dishes = cursor.fetchall()

    conn.close()

    message = 'Список закусок:\n' + "\n".join(
        [f"{dish.capitalize()}, время на приготовление — {time}мин." for dish, time in dishes])
    update.message.reply_text(message)


def recipe(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db', check_same_thread=False)
    cursor = conn.cursor()
    dish_name = ' '.join(context.args).lower()
    tables = ['breakfast', 'first', 'second', 'snacks', 'drinks']
    result = None
    for i in tables:
        cursor.execute(f"SELECT url FROM {i} WHERE dish=?", (dish_name,))
        result = cursor.fetchone()
        if result:
            update.message.reply_text(f'Рецепт для приготовления блюда "{dish_name.capitalize()}": {result[0]}')
    if not result:
        update.message.reply_text("Хмм... Я такое блюдо не знаю...")
    conn.close()


def random_meal(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db', check_same_thread=False)
    cursor = conn.cursor()
    tables = ['first', 'second', 'snacks', 'drinks']
    dict_temp = {'first': 'Сегодня у вас на первое: ',
                 'second': 'В этот раз на второе вы попробуете: ',
                 'snacks': 'В качестве закуски у вас: ',
                 'drinks': 'Ваш стол сегодня украсит напиток: '}
    result = ''
    for i in tables:
        cursor.execute(f"SELECT MIN(id) FROM {i}")
        min_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT MAX(id) FROM {i}")
        max_id = cursor.fetchone()[0]

        num = random.randint(min_id, max_id)
        cursor.execute(f"SELECT dish, url FROM {i} WHERE id=?", (num,))
        dish, url = cursor.fetchone()

        message = f'{dict_temp[i]} "{dish.capitalize()}"\n {url}'
        result = result + message + '\n' * 2
    update.message.reply_text(result)
    conn.close()


def random_snack(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db', check_same_thread=False)
    cursor = conn.cursor()
    tables = ['snacks', 'drinks']
    dict_temp = {'snacks': 'Ваш перекус: ',
                 'drinks': 'Запьёте вы его напитком: '}
    result = ''
    for i in tables:
        cursor.execute(f"SELECT MIN(id) FROM {i}")
        min_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT MAX(id) FROM {i}")
        max_id = cursor.fetchone()[0]

        num = random.randint(min_id, max_id)
        cursor.execute(f"SELECT dish, url FROM {i} WHERE id=?", (num,))
        dish, url = cursor.fetchone()

        message = f'{dict_temp[i]} "{dish.capitalize()}"\n {url}'
        result = result + message + '\n' * 2
    update.message.reply_text(result)
    conn.close()


def advice(update: Update, context: CallbackContext):
    conn = sqlite3.connect('recipes.db', check_same_thread=False)
    cursor = conn.cursor()
    tables = ['first', 'second', 'snacks', 'drinks']
    dict_temp = {'first': 'Из категории супов и салатов я рекомендую: ',
                 'second': 'Это одно из моих любимых основных блюд: ',
                 'snacks': 'Могу порекомендовать отличную закуску: ',
                 'drinks': 'Вам определенно стоит попробовать: '}
    table = tables[random.randint(0, 3)]

    cursor.execute(f"SELECT MIN(id) FROM {table}")
    min_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT MAX(id) FROM {table}")
    max_id = cursor.fetchone()[0]
    num = random.randint(min_id, max_id)
    cursor.execute(f"SELECT dish, url FROM {table} WHERE id=?", (num,))
    dish, url = cursor.fetchone()
    message = f'{dict_temp[table]} "{dish.capitalize()}"\n {url}'
    update.message.reply_text(message)
    conn.close()


def music(update: Update, context: CallbackContext):
    update.message.reply_text("Вот ваш плейлист для готовки: \n https://music.yandex.ru/users/Gryphoniy/playlists/1000")



def main():
    updater = Updater(BOT_API, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler("recipe", recipe))
    dp.add_handler(CommandHandler("random_meal", random_meal))
    dp.add_handler(CommandHandler("random_snack", random_snack))
    dp.add_handler(CommandHandler('advice', advice))
    dp.add_handler(CommandHandler('music', music))
    dp.add_handler(CommandHandler('breakfast', breakfast))
    dp.add_handler(CommandHandler('first', first))
    dp.add_handler(CommandHandler('second', second))
    dp.add_handler(CommandHandler('drinks', drinks))
    dp.add_handler(CommandHandler('snacks', snacks))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
