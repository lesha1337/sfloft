from telebot import types


def init_buttons(cmds, rw=2):
    markup = types.ReplyKeyboardMarkup(row_width=rw)
    btns = [types.KeyboardButton(name) for name in cmds]
    markup.add(*btns)
    if cmds != defcats:
        markup.add('/назад')
    return markup

people_sizes = ['0-20', '20-40', '40-80', '100+']
defcats = ['/вечеринка', '/тренинг_лекция', '/свадьба', '/другое']

categories = init_buttons(defcats)
categories_more = init_buttons(['/съемки','/детский_праздник'])
how_many_people = init_buttons(people_sizes)

