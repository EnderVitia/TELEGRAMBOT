import telebot
from telebot import types
import config
from time import sleep
import sqlite3


def waiting(chatid, messageid):
    global a
    while a != 1:
        sleep(0.5)
    bot.delete_message(chatid, messageid)
    a = 0


a = 0

db = sqlite3.connect('rewievs.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user TEXT,
    rewiev TEXT,
    stars TINYINT
)""")

db.commit()

bot = telebot.TeleBot(config.TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
btn_order = types.KeyboardButton("Заказать")
btn_getRewievs = types.KeyboardButton("Посмотреть отзывы")
btn_writeRewiev = types.KeyboardButton("Написать отзыв")
markup_menu.add(btn_order, btn_getRewievs, btn_writeRewiev)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет, {0.first_name}!\nХочешь купить хорошей жижи? Тогда тебе сюда! Нажми кнопку заказать, "
                 "чтобы заказать жижу".format(
                     message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True)
def dialog(message):
    while message.text == "Заказать":
        global a
        markup_krep = types.InlineKeyboardMarkup(row_width=3)
        krep1 = types.InlineKeyboardButton("36", callback_data='36')
        krep2 = types.InlineKeyboardButton("50", callback_data='50')
        krep3 = types.InlineKeyboardButton("70", callback_data='70')

        markup_krep.add(krep1, krep2, krep3)

        botmessage = bot.send_message(chat_id=message.chat.id, text="Выберете крепость", reply_markup=markup_krep)
        waiting(message.chat.id, botmessage.message_id)

        markup_flavour = types.InlineKeyboardMarkup(row_width=4)
        flavour1 = types.InlineKeyboardButton("Клубника", callback_data='strawberry')
        flavour2 = types.InlineKeyboardButton("Ананас", callback_data='pineapple')
        flavour3 = types.InlineKeyboardButton("Вишня", callback_data='cherry')
        flavour4 = types.InlineKeyboardButton("Черника", callback_data='blackberry')
        markup_flavour.add(flavour1, flavour2, flavour3, flavour4)

        botmessage = bot.send_message(chat_id=message.chat.id, text="Выберете вкус", reply_markup=markup_flavour)
        waiting(message.chat.id, botmessage.message_id)

        markup_cooler = types.InlineKeyboardMarkup(row_width=2)
        coolyes = types.InlineKeyboardButton("Да", callback_data='есть')
        coolno = types.InlineKeyboardButton("Нет", callback_data='нет')
        markup_cooler.add(coolyes, coolno)

        botmessage = bot.send_message(chat_id=message.chat.id, text="Добавить куллер?", reply_markup=markup_cooler)
        waiting(message.chat.id, botmessage.message_id)

        markup_sugar = types.InlineKeyboardMarkup(row_width=2)
        sugaryes = types.InlineKeyboardButton("Да", callback_data='есть')
        sugarno = types.InlineKeyboardButton("Нет", callback_data='нет')
        markup_sugar.add(sugaryes, sugarno)

        botmessage = bot.send_message(chat_id=message.chat.id, text="Добавить подсластитель?", reply_markup=markup_sugar)
        waiting(message.chat.id, botmessage.message_id)

        markup_apply = types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton("Правильно", callback_data="Правильно")
        no = types.InlineKeyboardButton("Заказать заново", callback_data="Заказать заново")
        markup_apply.add(yes, no)

        f = open("order1.txt", 'r+')
        order1 = [str(line.strip()) for line in f]
        order2 = order1
        botmessage = bot.send_message(message.chat.id, text=("Ваш заказ:\n"+"Крепость: "+ order1[0] +"\nВкус: " + order1[1]+"\nКулер: "+ order1[2] +"\nПодсластитель: "+ order1[3]), reply_markup=markup_apply)
        waiting(message.chat.id, botmessage.message_id)
        order1 = [str(line.strip()) for line in f]
        if order1[0] == "Правильно":
            f.seek(0)
            f.truncate()
            f.close()
            f = open("orders.txt", 'a')
            f.write(str(order2))
            f.close
            break
        elif order1[0] == "Заказать заново":
            f.seek(0)
            f.truncate()
            f.close()

@bot.message_handler(func=lambda message: True)
def rewiev(message):
    bot.send_message(message.chat.id, "Введите имя")
    username = message.text
    print(username)





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            f = open('order1.txt', 'a')
            f.write(call.data + '\n')
            f.close()
            global a
            a = 1
    except Exception as e:
        print(repr(e))


# RUN
bot.polling()
