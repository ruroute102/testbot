# -*- coding: utf-8 -*-
import logging
import telebot
from bot_tg import config
# from telebot import apihelper

# PROXY = 'https://200.69.70.133:9991'
# apihelper.proxy = {'https': PROXY}
# Создам экземпляр класса TeleBot, который находится в telebot:
bot = telebot.TeleBot(config.TOKEN)  # (В качестве аргумента передадим токен бота)

"""
Бот должен реагировать на сообщения и команды, 
в библиотеке для этого есть хандлеры (handlers), 
которые описывают, на какие сообщения и как должен отвечать бот.
"""


# Обязательным является обработчик команды /start. Реализую его следующим образом:


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, config.start_message)


"""
Первая строчка – это handler, который будет срабатывать при команде /start 
(это указано в аргументе commands=[‘start’]). 
Затем идёт функция, которая будет вызвана. 
Она принимает только один аргумент, в котором будет информация о полученном сообщении, пользователе, 
который его отправил и тд. Сама функция очень простая: 
с помощью метода send_message мы отправляем приветственное сообщение пользователю, по его id.
"""


# Создадим обработчик для команды /help, он будет почти что таким, за исключением пары моментов:
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, config.help_message)


"""
Мы создали два базовых обработчика, теперь самое время перейти к решению основной задачи 
– пересылке сообщений в приватный чат, а также возможности отвечать на них прямо из чата. 
Код очень простой, не будем принимать в расчёт разные пограничные ситуации.
"""


@bot.message_handler(func=lambda message: True)
def forward_handler(message):
    try:
        if message.chat.id == int(config.CHAT):
            bot.send_message(message.reply_to_message.forward_from.id, message.text)
        else:
            bot.forward_message(config.CHAT, message.chat.id, message.message.id)
    except Exception as error:
        print('Exception in forward handler. Info: ()'.format(error))


"""
В обработчик передадим функцию, которая всегда возвращает True 
(это значит, что данный обработчик будет срабатывать на все сообщения, за исключением команд /start и /help). 
На всякий случай добавим обработку ошибок try – except, и, если будет какая-то ошибка, 
то с помощью print выведем её в консоль. В блоке try проверяем id чата, из которого получили сообщение, 
и, если это id специального, приватного чата, то пробуем переслать сообщение тому, 
кому мы пытаемся ответить (напомню, что это нужно делать с помощью reply). 
Используем тот же send_message: первый аргумент – id того, на чьё сообщение хотим ответить 
(id находится в свойстве reply_to_message.forward_from.id), второй аргумент – текст нашего сообщения.
Если id чата отличается от специального (для сбора сообщений), 
то пересылаем полученное сообщение в наш чат используя метод forward_message 
(первый аргумент – чат, куда нужно переслать сообщение, второй – id сообщения, которое нужно переслать).
"""
# Теперь узнаем id того чата, в который мы добавили бота.
# Само по себе добавление бота в чат – это событие,
# и его можно «поймать». Добавьте в самый низ файла bot.py следующую строку:

# print(bot.get_updates()[0].message.chat.id)

# Несколько предупреждений: может возникнуть ошибка доступа к Telegram из-за того,
# что он заблокирован в некоторых странах, в таком случае включите VPN
# и повторите запрос.

"""
Откройте терминал в той директории, в которой находиться исходный код бота 
(смотрите на путь в строке поиска) и введите команду python3 bot.py (может быть python bot.py). 
Если все успешно, то в консоле появиться id чата, это должно быть отрицательное число, 
у приватных чатов перед id всегда стоит «минус». 
Скопируйте это id и сохраните в переменной CHAT (можно как строку, а можно как число).
Небольшая ремарка: если вы получаете пустой массив и нет никаких обновлений, 
то попробуйте удалить бота из чата и добавить его снова, при этом вместо [0] укажите [1]. 
Если всё равно на этом этапе возникают проблемы, то переходите к следующему шагу.
"""

# Удалите строку для получения обновлений!

"""
Осталось чуть-чуть, создадим функцию, для запуска бота. 
Мы не будем создавать сервер, и использовать web hooks, а ограничимся методом polling. 
Также мы добавим логирование, оно уже добавлено в библиотеку PyTelegramBotApi, 
им довольно просто пользоваться. В самый верх файла bot.py добавьте строку: import logging
"""


# Код функции будет следующий:
def main(use_logging, level_name):
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop=True, interval=.5)


# Она принимает два аргумента: первым «включаем» или «выключаем» логирование, вторым выбираем «уровень» логирования.

# Осталось вызвать функцию и проверить, работает ли бот.

if __name__ == '__main__':
    main(True, 'DEBUG')

"""
Теперь проверим бота, благодаря логингу мы сможем отловить ошибки, если они возникнут, 
а также получать всю информацию о обновлениях. Откройте бота и нажмите Start. 
Бот должен пристать приветственное сообщение (start_mess). 
Введите команду /help – бот должен пристать сообщение help_mess. Теперь самое главное, напишите что-нибудь, 
и это сообщение должно появиться в приватном чате. А теперь с помощью reply ответьте на него, 
и, если бот прислал сообщение, которое вы написали, то всё отлично!
Если что-то не работает, то посмотрите логи, проверьте, правильный ли id чата указан в переменной 
(его можно посмотреть в логах). Удалите бота из чата и добавьте его снова, 
и при этом посмотрите логи в консоле. Так вы сможете узнать id приватного чата.
"""
