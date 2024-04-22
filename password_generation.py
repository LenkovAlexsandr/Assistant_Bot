from random import choices, randint, shuffle


def compilation(complexity):
    """Составление пароля в зависимости от сложности"""
    if complexity == 'easy':
        a = randint(4, 6)
        b = 8 - a
        c = 0
    elif complexity == 'normal':
        a = randint(6, 7)
        c = randint(1, 3)
        b = 12 - a - c
    else:
        a = randint(10, 13)
        c = randint(2, 5)
        b = 20 - a - c
    sigls = choices('qwertyuiopasdfghjklzxcvbnm', k=a)
    for i in choices(range(a), k=int(a * 0.6)):
        sigls[i] = sigls[i].upper()
    digits = choices('1234567890', k=b)
    symbols = choices('-_+=!@#/.,&:;()', k=c)
    password = sigls + digits + symbols
    shuffle(password)
    return ''.join(password)


async def password_generation(update, context):
    """Генерация пароля"""
    try:
        complexity = context.args[0]
        assert complexity in ['easy', 'normal', 'hard']
    except Exception:
        complexity = 'normal'
    text = f'Варианты паролей сложности-{complexity}:'
    for i in range(10):
        text += f'\n`{compilation(complexity)}`'
    await update.message.reply_text(text, parse_mode="MARKDOWN")
