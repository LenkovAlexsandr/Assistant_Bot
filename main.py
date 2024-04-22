import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from timer import timers, timer, unset
from password_generation import password_generation
from translate import translation_settings, translation
from help import help_bot, commands


# Запускаем логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                    filename='log.log')


async def start(update, context):  # /start
    await help_bot(update, context)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    # Команды для таймера
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(CommandHandler("timers", timers))
    application.add_handler(CommandHandler("unset", unset))
    # Команда генерации пароляв
    application.add_handler(CommandHandler("generation", password_generation))
    # Команды для переводчика
    application.add_handler(CommandHandler("tr_set", translation_settings))
    application.add_handler(CommandHandler("tr", translation))
    # Команда помощи
    application.add_handler(CommandHandler("help", help_bot))
    # Команда старт
    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == '__main__':
    main()
