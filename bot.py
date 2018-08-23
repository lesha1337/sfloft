import telebot
import time

from api import chat
import datetime
from api import answers
from api import buttons
from api import amo

import pickle
from telebot.types import *

import json
import pprint


def dump_hist(hist):
    with open('history.json', 'wb') as f:
        pickle.dump(hist, f)

def load_hist():
    with open('history.json', 'rb') as f:
        data = pickle.load(f)
    return data

def suggest_loft(id, msg=''):
    if hist[id]['how_many_people'] == '0-20':
        name = 'на м. Бауманская и на м. Красные ворота'
        msg = 'Для Ваших задач идеально подойдут #soulfulloft ' + name + '!'
        kb = buttons.init_buttons(['/Бауманская', '/Красные_ворота'])
        bot.send_message(id, msg, reply_markup=kb)
        return

    if hist[id]['how_many_people'] == '20-40':
        name = 'на м. Бауманская и на м. Красные ворота'
        msg = 'Для Ваших задач идеально подойдут #soulfulloft ' + name + '!'
        kb = buttons.init_buttons(['/Бауманская', '/Красные_ворота'])
        bot.send_message(id, msg, reply_markup=kb)
        return

    if hist[id]['how_many_people'] == '40-80':
        name = 'на м. Чистые пруды и на м. Красные ворота'
        msg = 'Для Ваших задач идеально подойдут #soulfulloft ' + name + '!'
        kb = buttons.init_buttons(['/Чистые_пруды', '/Красные_ворота'])
        bot.send_message(id, msg, reply_markup=kb)
        return

    if hist[id]['how_many_people'] == '100+':
        name = 'на м. Чистые пруды'
        msg = 'Для Ваших задач идеально подойдет #soulfulloft ' + name + '!'
        kb = buttons.init_buttons(['/Чистые_пруды'])
        bot.send_message(id, msg, reply_markup=kb)
        return

    bot.send_message(id, msg)


def int_validation(num):
    try:
        int(num)
        return True
    except Exception as e:
        return False

def date_validation(text_list):
    ans = 0
    for i in text_list:
        ans+=int(int_validation(i))
    return ans

# first stage
@bot.message_handler(commands=['adpics'])
def sendpic(message):
    picarr=[]
    l = answers.lofts
    for i in range(0,9):
        try:
            ans = str(bot.send_photo(message.chat.id, photo=open(l['Чистые_пруды']['pic'][i], 'rb')).photo[2].file_id)

        except Exception as e:
            pass
            ans = str(bot.send_photo(message.chat.id, photo=open(l['Чистые_пруды']['pic'][i], 'rb')).photo[2].file_id)


@bot.message_handler(commands=['start', 'мероприятие'])
def start_answer(message, troubles=False):
    try:
        uname = str(message.from_user.first_name)+' '+str(message.from_user.last_name) + ' '+str(message.from_user.username)
    except Exception as e:
        uname = str(message.from_user.username)
    hist[message.chat.id] = {'id': message.chat.id,
                             'flname': uname,
                             'uname': message.from_user.username,
                             'phone': 000,
                             }
    dump_hist(hist)

    if not troubles:
        bot.reply_to(message, answers.start, reply_markup=buttons.categories)


@bot.message_handler(commands=['другое'])
def oth_answer(message):
    bot.reply_to(message, answers.other, reply_markup=buttons.categories_more)


@bot.message_handler(commands=['назад'])
def backbutt(message):
    #smartback
    bot.reply_to(message, answers.back, reply_markup=buttons.categories)

# second stage
@bot.message_handler(commands=['вечеринка', 'съемки', 'тренинг_лекция', 'свадьба', 'съемки','детский_праздник'])
def activity(message):
    try:
        hist[message.chat.id]['target'] = message.text
    except Exception as e:
        start_answer(message, troubles=True)
        hist[message.chat.id]['target'] = message.text

    dump_hist(hist)

    bot.reply_to(message, answers.chosen, reply_markup=buttons.how_many_people)

@bot.message_handler(commands=['Чистые_пруды', 'Красные_ворота', 'Бауманская'])
def current_loft(message):

    msg = message.text.replace('/', '')
    hist[message.chat.id]['loft'] = msg
    dump_hist(hist)

    bot.send_chat_action(message.chat.id, 'typing')

    picarr=[]
    if hist[message.chat.id]['target'] == '/тренинг_лекция':
        for i in answers.lofts[msg]['тренинг_лекция']:
            picarr.append(InputMediaPhoto(i))
    else:
        for i in answers.lofts[msg]['вечеринка']:
            picarr.append(InputMediaPhoto(i))

    bot.send_message(message.chat.id, answers.lofts[msg]['description'])
    bot.send_chat_action(message.chat.id, 'upload_photo')
    bot.send_media_group(message.chat.id, picarr)
    bot.send_message(message.chat.id, answers.lofts[msg]['adress'])
    bot.send_chat_action(message.chat.id, 'find_location')
    bot.send_location(message.chat.id, *answers.lofts[msg]['geo'])
    bot.send_message(message.chat.id, "Подошел лофт?\nНапиши дату, когда хочешь провести мероприятие.\nВ формате: 14.08.2020")#, reply_markup=keyboard)

# text
@bot.message_handler(content_types='text')
def handle_text(message):

    if message.text in set(buttons.people_sizes):
        hist[message.chat.id]['how_many_people'] = message.text
        dump_hist(hist)
        suggest_loft(message.chat.id, message.text)
    elif (message.text[0] == '+') and len(message.text) == 12:
        hist[message.chat.id]['phone'] = message.text
        dump_hist(hist)

        keyboard = InlineKeyboardMarkup()
        ansmsg = "Ваш заказ:\n" + str(hist[message.chat.id]['target']) + ' в #Soulfulloft "' + str(hist[message.chat.id]['loft']) + '", ' + str(hist[message.chat.id]['date'])
        
        callback_button = InlineKeyboardButton(text='Да, все верно! Подтвердить заказ', callback_data="commit_application")
        keyboard.add(callback_button)

        bot.send_message(message.chat.id, ansmsg, reply_markup=keyboard)

    elif len(message.text.split('.')) == 3 and date_validation(message.text.split('.')) == 3:
        hist[message.chat.id]['date'] = message.text
        dump_hist(hist)

        bot.send_message(message.chat.id, 'Хорошо, теперь введи свой номер телефона.\nВ формате: +79154443322')
    else:
        msg = chat.answer(message)
        bot.send_message(message.chat.id, msg, reply_markup=buttons.categories)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message and call.data == "commit_application": #amocrm
        u_params = hist[call.message.chat.id]

        amo.send_lead(phone=u_params['phone'],
            loft=u_params['loft'],
            date=u_params['date'],
            members=u_params['how_many_people'],
            event_type=u_params['target'],
            name=u_params['flname'])

        bot.answer_callback_query(call.id, text="Заказ отправлен!")
        bot.send_message(call.message.chat.id, 'Ура! Заказ отправлен! \nВскоре c Вами свяжется менеджер для уточнения деталей!')

def reformdate(date_dashed):
    nice_date = ''
    for i in date_dashed.split('-'):
        nice_date = nice_date + i + ' '
    return nice_date


if __name__ == '__main__':
    bot = telebot.TeleBot("***")
    hist = load_hist()
    bot.polling(none_stop=True)