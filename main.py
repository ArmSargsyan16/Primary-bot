import telebot
from telebot import types
import sqlite3
import threading

db_lock = threading.Lock()

def get_db_connection():
    conn = sqlite3.connect('new_database.db')
    return conn

def user_exists(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_user_id(user_id, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def on_startup():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)")
    conn.commit()
    conn.close()


bot = telebot.TeleBot('6558603300:AAEJG_DJT7k7b44dyiy6_NfQvZKos_KkgGk')

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    if not user_exists(user_id):
     save_user_id(user_id, username)  
 
    markup = types.InlineKeyboardMarkup()
    btn1 = markup.add(types.InlineKeyboardButton("Ссылка на сайт", url='https://gramtele.ru/ref467646'))
    btn2 = markup.add(types.InlineKeyboardButton("Как зарегистрироваться", callback_data='register'))
    btn3 = markup.add(types.InlineKeyboardButton("Как сделать заказ", callback_data='order'))
    btn4 = markup.add(types.InlineKeyboardButton("Как пополнить баланс", callback_data='balance'))
    btn5 = markup.add(types.InlineKeyboardButton("Обратная связь", url='https://t.me/gramtele_ru_support'))
    file = open('./main/photo.jpg', 'rb')
    bot.send_photo(message.chat.id, file, "Добро пожаловать!", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    current_state = user_states.get(chat_id, None)

    if callback.data == 'register':
        user_states[chat_id] = 'register'
        markup = types.InlineKeyboardMarkup()
        btn1 = markup.add(types.InlineKeyboardButton("Создать аккаунт", url='https://gramtele.ru/ref467646'))
        btn2 = markup.add(types.InlineKeyboardButton("Назад", callback_data='back'))
        file = open('./main/register.jpg', 'rb')
        bot.send_photo(chat_id, file, "1. Вводите свой email.\n2. Придумываете имя пользователя.\n3. Придумываете пароль.\n4. Вводите свой логин от телеграмма \nИ все" , reply_markup=markup)
    elif callback.data == 'order':
        user_states[chat_id] = 'order'
        markup = types.InlineKeyboardMarkup()
        btn1 = markup.add(types.InlineKeyboardButton("Создать заказ", url='https://gramtele.ru/ref467646'))
        btn2 = markup.add(types.InlineKeyboardButton("Назад", callback_data='back'))
        file = open('./main/order.jpg', 'rb')
        bot.send_photo(chat_id, file, "Выбираете нужную вам услугу: \nTelegram \nYouTube \nTwitter \nSoundCloud \nTikTok \nInstagram \nИ создаете заказ" , reply_markup=markup)
    elif callback.data == 'balance':
        user_states[chat_id] = 'balance'
        markup = types.InlineKeyboardMarkup()
        btn1 = markup.add(types.InlineKeyboardButton("Подробнее", url='https://gramtele.ru/ref467646'))
        btn2 = markup.add(types.InlineKeyboardButton("Назад", callback_data='back'))
        file = open('./main/balance.jpg', 'rb')
        bot.send_photo(chat_id, file, "Выбираете любой удобный вам способ \n1.Крипто \n2.Лава (киви/карты/и т.д) \n3. Binance ID " , reply_markup=markup)
    elif callback.data == 'back':
        if current_state == 'register':
            start(callback.message)
        elif current_state == 'order':
            start(callback.message)
        elif current_state == 'balance':
            start(callback.message)


if __name__ == "__main__":
    on_startup()
    bot.polling()
