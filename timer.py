from datetime import timedelta


async def timers(update, context):
    """Вывод всех таймеров"""
    chat_id = update.effective_message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        text = 'Время активации по Москве:'
        for i, job in enumerate(current_jobs):
            time = job.trigger.run_date + timedelta(hours=3)
            text += f'\nТаймер {i}: {time.strftime("%Y %m %d %H:%M:%S")}'
    else:
        text = 'У вас нет установленных таймеров.'
    await update.effective_message.reply_text(text)


async def timer(update, context):
    """Добавление таймера"""
    chat_id = update.effective_message.chat_id
    try:
        data = list(map(int, context.args)) + [0, 0, 0]
        time = data[0] + data[1] * 60 + data[2] * 3600 + data[3] * 24 * 3600
        data[1] += data[0] // 60
        data[0] %= 60
        data[2] += data[1] // 60
        data[1] %= 60
        data[3] += data[2] // 24
        data[2] %= 24
        data = f'{data[0]}с. {data[1]}м. {data[2]}ч. {data[3]}д.'
        context.job_queue.run_once(task_timer, time, chat_id=chat_id, name=str(chat_id), data=data)
        text = f'Поставлен таймер на {data}'
    except Exception:
        text = 'Время не указано или указано неверно.'
    await update.effective_message.reply_text(text)


async def task_timer(context):
    """Выводит сообщение"""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f'Дилинь! Дилинь! Таймер! На {job.data} Сработал!')


async def unset(update, context):
    """Удаление таймера"""
    chat_id = str(update.message.chat_id)
    try:
        current_jobs = context.job_queue.get_jobs_by_name(chat_id)
        if current_jobs:
            number = context.args[0]
            if number == 'all':
                for job in current_jobs:
                    job.schedule_removal()
                text = 'Все таймеры удалены.'
            else:
                current_jobs[int(number)].schedule_removal()
                text = f'Таймер номер {number} удален.'
        else:
            text = 'Нет установленных таймеров.'
    except Exception:
        text = 'Не верно указан номер таймеров.'
    await update.message.reply_text(text)
