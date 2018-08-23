banned_words = ['хуй', 'пидор', 'долбоеб', 'уебан', 'уебище']
hello_words = ['прив', 'привет', 'здарова', 'здравстуй']
whatsup = ['дела']

def answer(message):
    message=message.text.lower()
    print(message.find('прив'))
    for w in banned_words:
        if message.find(w)>=0:
            return ('...')

    for w in hello_words:
        if message.find(w)>=0:
            return ('Привет!')

    for w in whatsup:
        if message.find(w)>=0:
            return 'Отлично! Будет еще лучше, если ты забронируешь наш Лофт :)'

    return 'Чтобы воспользоваться ботом, напиши "/start"'
