import sys
import random
import traceback
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove #InlineQueryResult
from telegram.bot import Bot
from telegram import *
from storage import Storage
from threading import Thread
from time import sleep


SEND_NEXT_PHOTO = range(1)

USER_INPUT = {}
USER_LOCATION = {}

storage = Storage()
lastImage = {}

rm = ReplyKeyboardMarkup( [['💩', '😍']], resize_keyboard = True)

def show_error(bot, update, error):
    print('Update "{}" caused error "{}"'.format(update, error))

def inputToString(input):
    if(input == '💩'):
        return '-'
    elif(input == '😍'):
        return '+'
    else:
        return input

def inputToScore(input):
    if(input == '💩'):
        return -1
    elif(input == '😍'):
        return +1
    else:
        return 0

def greet_user(bot , update):
    input = update.message.text
    chatId = update.message.chat_id
    print('{0} :> {1}'.format(chatId, inputToString(input)))  
      
    bot.sendMessage(chatId, text = "Сейчас покажу фотки стильных нигеров")

    user = storage.getUser(chatId)
    image = storage.getImage(user)
    lastImage[chatId] = image
    bot.sendPhoto(chatId, photo = image[1].text, reply_markup = rm)
    print('{0} <: send photo {1}.{2}'.format(chatId, image[0].get("id"), image[1].get("id"))) 

    return SEND_NEXT_PHOTO


def send_next_photo(bot, update):
    input = update.message.text
    chatId = update.message.chat_id
    print('{0} :> {1}'.format(chatId, inputToString(input)))  
    
    user = storage.getUser(chatId)
    
    if input == '💩' or input == '😍':
        if chatId in lastImage:
            storage.addView(user, lastImage[chatId][0], lastImage[chatId][1], inputToScore(input))            
            print('{0} <: add view {1}.{2} = {3}'.format(chatId, lastImage[chatId][0].get("id"), lastImage[chatId][1].get("id"), inputToScore(input)))
    
    image = storage.getImage(user)
    lastImage[chatId] = image
    bot.sendPhoto(chatId, photo = image[1].text, reply_markup = rm)
    print('{0} <: send photo {1}.{2}'.format(chatId, image[0].get("id"), image[1].get("id")))  

    return SEND_NEXT_PHOTO


def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, 'Пока! Возвращайся за луками нигеров!', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END

def autoSaveThread():
    print("save thread started")
    while(True):
        sleep(60)
        storage.save()

def readConsoleThread():
    print("command thread started")
    while(True):
        command = input()
        if command == "save":
            storage.save()        

def telegramThread():
    print("bot thread started")
    updater = Updater("361737979:AAE47wwOFxxKRsxPrAfuVUT7qljgSdR4rqM")
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', greet_user)],
        states = 
        {
            SEND_NEXT_PHOTO: [MessageHandler(Filters.text, send_next_photo)]
        },
        fallbacks = [CommandHandler('cancel', cancel)])

    dp.add_handler(conv_handler)
    dp.add_error_handler(show_error)
    updater.start_polling()
    print("bot successfully started")

if __name__ == '__main__':
    threads = [Thread(target = readConsoleThread), Thread(target = telegramThread), Thread(target = autoSaveThread)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
