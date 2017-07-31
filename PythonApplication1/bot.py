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

photos = ['http://i.imgur.com/QFsaN9J.jpg', 'http://i.imgur.com/aEef2aM.jpg', 'http://i.imgur.com/MbOanXz.jpg', 'http://i.imgur.com/4cuT7TU.jpg', 'http://i.imgur.com/pcYzxGy.jpg', 'http://i.imgur.com/d3f0miG.jpg', 'http://i.imgur.com/0mmyqPg.jpg', 'http://i.imgur.com/jov80tB.png', 'http://i.imgur.com/T2u8LE7.jpg', 'http://i.imgur.com/srUdzb0.jpg', 'http://i.imgur.com/D7OauqK.jpg', 'http://i.imgur.com/HgKKd6u.jpg', 'http://i.imgur.com/JAp2yYE.jpg', 'http://i.imgur.com/jmNNhdR.jpg', 'http://i.imgur.com/GgG0wkd.png', 'http://i.imgur.com/a8XIGwr.jpg', 'http://i.imgur.com/aKOMnjA.png', 'http://i.imgur.com/nKn0q4z.jpg', 'http://i.imgur.com/78jL0UC.jpg', 'http://i.imgur.com/ltGWv5s.jpg', 'http://i.imgur.com/d2iorEU.png', 'http://i.imgur.com/ryU6s9t.jpg', 'http://i.imgur.com/F2X45hD.jpg', 'http://i.imgur.com/NuAx64D.jpg', 'http://i.imgur.com/xri6wDD.jpg', 'http://i.imgur.com/LBoVzZZ.jpg', 'http://i.imgur.com/P50kFBz.jpg', 'http://i.imgur.com/8PRlebK.jpg', 'http://i.imgur.com/BCuqQ7N.jpg', 'http://i.imgur.com/t5egZsI.jpg', 'http://i.imgur.com/LSXcyJi.jpg', 'http://i.imgur.com/OzvwjFk.jpg', 'http://i.imgur.com/Dwq2OJT.png', 'http://i.imgur.com/tPUsBkM.jpg', 'http://i.imgur.com/IB7WmR5.jpg', 'http://i.imgur.com/dwqvphr.jpg', 'http://i.imgur.com/pApOk6C.jpg', 'http://i.imgur.com/AYKcNzn.jpg', 'http://i.imgur.com/WDGbnkE.png', 'http://i.imgur.com/ZEB9m7X.jpg', 'http://i.imgur.com/98pGfiB.png', 'http://i.imgur.com/lrOqo2m.jpg', 'http://i.imgur.com/tL0hFnZ.jpg', 'http://i.imgur.com/SNZP6e4.jpg', 'http://i.imgur.com/COdI5b8.jpg', 'http://i.imgur.com/SMW6TaX.jpg', 'http://i.imgur.com/LLfZhng.png', 'http://i.imgur.com/supdpnj.png', 'http://i.imgur.com/7CPkGGC.jpg', 'http://i.imgur.com/tgSmgrg.jpg', 'http://i.imgur.com/WLMZabC.jpg', 'http://i.imgur.com/S8KRakl.jpg', 'http://i.imgur.com/jQzu9ZB.jpg', 'http://i.imgur.com/8hwjQJI.jpg', 'http://i.imgur.com/vVD8YT8.jpg', 'http://i.imgur.com/bbpxTTN.png', 'http://i.imgur.com/BUL6lCK.jpg', 'http://i.imgur.com/EGs5njD.jpg', 'http://i.imgur.com/EvjmChw.jpg', 'http://i.imgur.com/sMQ9y2S.png', 'http://i.imgur.com/RfYcGPP.jpg', 'http://i.imgur.com/uFbZql9.jpg', 'http://i.imgur.com/URh5QkR.jpg', 'http://i.imgur.com/97EVmSk.jpg', 'http://i.imgur.com/iwpnD5E.jpg', 'http://i.imgur.com/iJBGQY7.jpg', 'http://i.imgur.com/CCBfAjk.jpg', 'http://i.imgur.com/w1B2jrO.jpg', 'http://i.imgur.com/QDRpd1T.jpg', 'http://i.imgur.com/qSgXW1h.jpg', 'http://i.imgur.com/XkotlcW.jpg', 'http://i.imgur.com/Jph519N.jpg', 'http://i.imgur.com/lZJfAfi.jpg', 'http://i.imgur.com/umx2TfZ.jpg', 'http://i.imgur.com/lJ7Yj0r.jpg', 'http://i.imgur.com/zGE4HKC.jpg', 'http://i.imgur.com/urbPZri.jpg', 'http://i.imgur.com/Uu2MKHm.png', 'http://i.imgur.com/Ovz6PzW.jpg', 'http://i.imgur.com/2MbaWOy.jpg', 'http://i.imgur.com/TBj9afN.jpg', 'http://i.imgur.com/fm2InNs.jpg', 'http://i.imgur.com/4KrBtl5.jpg', 'http://i.imgur.com/IwBYXc0.jpg', 'http://i.imgur.com/s1z62gT.jpg', 'http://i.imgur.com/bZ4qOIB.jpg', 'http://i.imgur.com/iQDDZAk.jpg', 'http://i.imgur.com/nde3Jrm.png', 'http://i.imgur.com/C7y71uu.jpg', 'http://i.imgur.com/DHMOdWq.jpg', 'http://i.imgur.com/VopJ71D.jpg', 'http://i.imgur.com/GL17X7u.png', 'http://i.imgur.com/222a4at.jpg', 'http://i.imgur.com/cRY1aM4.jpg', 'http://i.imgur.com/KBcnIzP.jpg', 'http://i.imgur.com/qxohFAo.jpg', 'http://i.imgur.com/S0Ovmp0.jpg', 'http://i.imgur.com/R8EadQ9.jpg', 'http://i.imgur.com/FcbKJXG.jpg', 'http://i.imgur.com/SonIzxm.jpg', 'http://i.imgur.com/EenvDpG.jpg', 'http://i.imgur.com/T08RbxQ.jpg', 'http://i.imgur.com/EC45qQg.jpg', 'http://i.imgur.com/pvAmNrr.jpg', 'http://i.imgur.com/6bR6JES.jpg', 'http://i.imgur.com/2tFh0Hd.jpg', 'http://i.imgur.com/7GGnmyN.jpg', 'http://i.imgur.com/GB6gW6E.jpg', 'http://i.imgur.com/fDPDoR2.jpg', 'http://i.imgur.com/R3RNf4e.jpg', 'http://i.imgur.com/0UTRyNc.jpg', 'http://i.imgur.com/Wz2DS9E.jpg', 'http://i.imgur.com/s5vsOBT.jpg', 'http://i.imgur.com/ndGJdeb.jpg', 'http://i.imgur.com/ddWkbUi.png', 'http://i.imgur.com/6KmuIqX.jpg', 'http://i.imgur.com/xss7DfI.jpg', 'http://i.imgur.com/AbwurSQ.jpg', 'http://i.imgur.com/MWJNOKT.jpg', 'http://i.imgur.com/IHee7wr.jpg', 'http://i.imgur.com/h5w94eS.jpg', 'http://i.imgur.com/Cgkwg0Q.png', 'http://i.imgur.com/awqhp5e.jpg', 'http://i.imgur.com/h7bwDSG.jpg', 'http://i.imgur.com/jEaKz7W.jpg', 'http://i.imgur.com/LclafhW.jpg', 'http://i.imgur.com/1KvJljo.png', 'http://i.imgur.com/AEv7f6M.jpg', 'http://i.imgur.com/TpFJpZq.jpg', 'http://i.imgur.com/uHZj8M6.jpg', 'http://i.imgur.com/AzTYNV5.png', 'http://i.imgur.com/UVqRl3E.jpg', 'http://i.imgur.com/4mPs7EA.jpg', 'http://i.imgur.com/jjgrXYr.jpg', 'http://i.imgur.com/aEi0wVe.jpg', 'http://i.imgur.com/sDknhw7.jpg', 'http://i.imgur.com/7KRcsZN.jpg', 'http://i.imgur.com/9PsSpdI.jpg', 'http://i.imgur.com/QhmgQLy.jpg', 'http://i.imgur.com/P2Oo2IQ.jpg', 'http://i.imgur.com/r5lTbXz.jpg', 'http://i.imgur.com/viy2J2g.jpg', 'http://i.imgur.com/Xfzx26D.jpg', 'http://i.imgur.com/S9iqyVn.jpg', 'http://i.imgur.com/j8W23VF.jpg', 'http://i.imgur.com/211VlqR.jpg', 'http://i.imgur.com/GEJBXoE.jpg', 'http://i.imgur.com/M43HmwW.png', 'http://i.imgur.com/6aIqY53.jpg', 'http://i.imgur.com/VNSnJ8r.jpg', 'http://i.imgur.com/j6eL0hJ.png', 'http://i.imgur.com/GFPSnS0.jpg', 'http://i.imgur.com/Y3avGqN.jpg', 'http://i.imgur.com/8WQSy08.jpg', 'http://i.imgur.com/ZqzcTTF.jpg', 'http://i.imgur.com/07zST85.jpg', 'http://i.imgur.com/y5G141S.jpg', 'http://i.imgur.com/g2IJdTm.jpg', 'http://i.imgur.com/mJn9T4A.jpg', 'http://i.imgur.com/Pw1uwwZ.jpg', 'http://i.imgur.com/LJZ7oGm.jpg', 'http://i.imgur.com/T2Pe0R5.jpg', 'http://i.imgur.com/Wu4fpES.jpg', 'http://i.imgur.com/cYXzHry.jpg', 'http://i.imgur.com/Ckx7rLy.jpg', 'http://i.imgur.com/CcIJzm8.jpg', 'http://i.imgur.com/cPaW3lr.jpg', 'http://i.imgur.com/mcKvz5c.jpg', 'http://i.imgur.com/MEZzuVf.jpg', 'http://i.imgur.com/dHym6zl.jpg', 'http://i.imgur.com/eWOB1pG.jpg', 'http://i.imgur.com/lAcGG2Q.jpg', 'http://i.imgur.com/K7i2yMl.jpg', 'http://i.imgur.com/v5KYssA.jpg', 'http://i.imgur.com/aVIWixb.jpg', 'http://i.imgur.com/59YBIxd.jpg', 'http://i.imgur.com/syFggAg.jpg', 'http://i.imgur.com/lctWX1e.jpg', 'http://i.imgur.com/vGJN0TL.jpg', 'http://i.imgur.com/GcOzCL6.png', 'http://i.imgur.com/Ml5xp4n.jpg', 'http://i.imgur.com/AO20JlL.jpg', 'http://i.imgur.com/WC7nXe3.jpg', 'http://i.imgur.com/Yk1sKxr.jpg', 'http://i.imgur.com/I66geKf.jpg', 'http://i.imgur.com/pPmqMdG.png', 'http://i.imgur.com/DRenhQh.jpg', 'http://i.imgur.com/HmeGF3a.jpg', 'http://i.imgur.com/c2Qvs6y.jpg', 'http://i.imgur.com/QhfFPcS.png', 'http://i.imgur.com/wjS0ctH.jpg', 'http://i.imgur.com/5MhWhXc.jpg', 'http://i.imgur.com/hyeAa6C.jpg', 'http://i.imgur.com/PjsZtIP.jpg', 'http://i.imgur.com/WAsLdH6.jpg', 'http://i.imgur.com/PPDLW0x.jpg', 'http://i.imgur.com/E3E2Fhu.jpg', 'http://i.imgur.com/xuJ55WD.jpg', 'http://i.imgur.com/bC3j39c.jpg', 'http://i.imgur.com/6Fbk3OL.jpg']

storage = Storage()

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
    user_choice = [update.message.text]
    variants = [['💩', '😍'], ['save']]
    rm = ReplyKeyboardMarkup(variants)
    
    user = storage.getUser(update.message.chat_id)
    image = storage.getImage(user)

    print(user_choice[0])

    if user_choice[0] == '👦' or user_choice[0] == '👧':
        bot.sendMessage(update.message.chat_id, text="Ok, got it",
                        reply_markup=rm)
        bot.sendPhoto(update.message.chat_id, photo=image.text, reply_markup=rm)
        #storage.addView(user,i, -1)
    if user_choice[0] == 'save':
        bot.sendMessage(update.message.chat_id, text="Saved", reply_markup=rm)
        storage.save()
    if user_choice[0] == '💩':
        bot.sendPhoto(update.message.chat_id, photo=image.text, reply_markup=rm)
        #storage.add_view(user,i, -1)
        return SEND_NEXT_PHOTO
    if user_choice[0] == '😍':
        bot.sendPhoto(update.message.chat_id, photo=image.text, reply_markup=rm)
        #storage.add_view(user,i, 1)
        return SEND_NEXT_PHOTO


def cancel(bot, update):
    bot.sendMessage(update.message.chat_id,'Пока! Надеюсь, я помог тебе!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    updater = Updater("361737979:AAE47wwOFxxKRsxPrAfuVUT7qljgSdR4rqM")
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', greet_user)],
        states={
            SEND_NEXT_PHOTO: [MessageHandler([Filters.text], send_next_photo)]
        },

       fallbacks=[CommandHandler('cancel', cancel)])

    dp.add_handler(conv_handler)
    dp.add_error_handler(show_error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
