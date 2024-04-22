from yandexfreetranslate import YandexFreeTranslate
import sqlite3

yt = YandexFreeTranslate(api="ios")


async def translation_settings(update, context):
    """Настройки перевода"""
    chat_id = update.effective_message.chat_id
    con = sqlite3.connect("db/database.sqlite")
    cur = con.cursor()
    target = cur.execute(f"""SELECT * FROM target WHERE id = {chat_id}""").fetchone()
    in_db = bool(target)
    if not target:
        target = ('auto', 'en')
    data = context.args
    if len(data) >= 1:  # Проверка наличия аргумента
        if data[0].lower() == 'all':  # при аргумента "all" передает все языки доступные для перевода
            text = 'Доступные языки для перевода:\n'
            language = cur.execute(f"""SELECT * FROM languages""").fetchall()
            text += '\n'.join(list(map(lambda x: f'{x[0]} - {x[1]}', language)))
        else:
            if len(data[0]) > 2:
                data[0] = data[0].lower().capitalize()
            language = cur.execute(f"""SELECT * FROM languages WHERE code = '{data[0]}' 
                                                        OR language = '{data[0]}'""").fetchone()
            if language:  # если аргумент был передан верно меняем язык перевода
                if in_db:
                    if language[0] != 'en':
                        cur.execute(f"""UPDATE target SET target = '{language[0]}' WHERE id = {chat_id}""")
                    else:
                        cur.execute(f"""DELETE FROM target WHERE id = {chat_id}""")
                elif language[0] != 'en':
                    cur.executemany("INSERT INTO target VALUES(?, ?);", [(chat_id, language[0])])
                con.commit()
                text = f'Язык перевода изменен на {language[0]} - {language[1]}'
            else:
                text = 'Язык не найден в базе данных.'
    else:  # если нет аргумента выводим текущий язык перевода
        language = cur.execute(f"""SELECT * FROM languages WHERE code = '{target[1]}'""").fetchone()
        text = f'Переводит на {language[0]} - {language[1]}'
    await update.effective_message.reply_text(text)


async def translation(update, context):
    """Перевод"""
    if context.args:
        translated_text = ' '.join(context.args)
        chat_id = update.effective_message.chat_id
        con = sqlite3.connect("db/database.sqlite")
        cur = con.cursor()
        target = cur.execute(f"""SELECT * FROM target WHERE id = {chat_id}""").fetchone()
        if not target:
            target = ('auto', 'en')
        text = yt.translate('auto', target[1], translated_text)
    else:
        text = 'Текст для перевода не указан.'
    await update.effective_message.reply_text(text)
