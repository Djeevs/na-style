import sys
import random
import traceback
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove #InlineQueryResult
from telegram.bot import Bot
from telegram import *
from storage import Storage

SEND_NEXT_PHOTO = range(1)

USER_INPUT = {}
USER_LOCATION = {}

storage = Storage()
lastImage = {}

def show_error(bot, update, error):
    print('Update "{}" caused error "{}"'.format(update, error))


def greet_user(bot , update):
    print('Вызван /start')
    variants = [['👦', '👧']]
    rm = ReplyKeyboardMarkup(variants)
    bot.sendMessage(update.message.chat_id, text="Are you a boy or a girl?",
                    reply_markup=rm)
    return SEND_NEXT_PHOTO

def send_next_photo(bot, update):
    input = update.message.text
    chatId = update.message.chat_id
    variants = [['💩', '😍'], ['save']]
    rm = ReplyKeyboardMarkup(variants)
    
    user = storage.getUser(chatId)

    print('{0}:{1}'.format(input, chatId))

    def sendPhoto():
        image = storage.getImage(user)
        lastImage[chatId] = image
        bot.sendPhoto(chatId, photo = image.text, reply_markup = rm)

    def addView(score):
        if chatId in lastImage:
            storage.addView(user, lastImage[chatId], score)

    if input == '👦' or input == '👧':
        bot.sendMessage(chatId, text = "Ok, got it", reply_markup = rm)
        sendPhoto()
    if input == 'save':
        bot.sendMessage(chatId, text = "Saved", reply_markup = rm)
        storage.save()
    if input == '💩':
        addView(-1)
        sendPhoto()
        return SEND_NEXT_PHOTO
    if input == '😍':
        addView(1)
        sendPhoto()
        return SEND_NEXT_PHOTO

def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, 'Пока! Надеюсь, я помог тебе!', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    updater = Updater("361737979:AAE47wwOFxxKRsxPrAfuVUT7qljgSdR4rqM")
    dp = updater.dispatcher
    conv_handler = ConversationHandler(entry_points = [CommandHandler('start', greet_user)],
    states = 
    {
        SEND_NEXT_PHOTO: [MessageHandler([Filters.text], send_next_photo)]
    },
    fallbacks = [CommandHandler('cancel', cancel)])

    dp.add_handler(conv_handler)
    dp.add_error_handler(show_error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
