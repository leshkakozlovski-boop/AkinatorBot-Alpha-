import telebot
from rag import play
from IDs import get_session, clear_user_history
import time
bot = telebot.TeleBot("key")

@bot.message_handler(commands=["start"])
def start(message):
    text1 ='''A majestic hello, my dear friend. I'm Akinator (only Alpha Version)! I'll guess your character! Let's start
---------------------------
Commands for you:
---------------------------
/start - registration or restart the bot.
---------------------------
/answers - how need to answer questions.
---------------------------
/statistics - your wins and Akinator wins.
---------------------------
/play - it's definitely play.
---------------------------
/help - how to play this game?
---------------------------
/creators - people who made Akinator.
---------------------------
/updates - information about previous and current versions of Akinator.
---------------------------
/extra - extra information about the game.
'''
    bot.reply_to(message, text1)

@bot.message_handler(commands=["help"])
def helping(message):
    text2="Need you help!? Think about a character, and I will try to guess who is it."
    bot.reply_to(message,text2)

@bot.message_handler(commands=["answers"])
def answering(message):
    text6='''
Positive answers:

"ye", "yeah", "yep", "yes", "да", "da", "y", "д", "yes"
---------------------------
Negative answers:

"no, nope", "nah", "ne", "na", "not", "нет", "net", "ni", "neh", "n", "н"
---------------------------
75% positive answers:

"prob", "probabl", "prbl", "probab", "вероятно", "veroyatno", "p", "в"
---------------------------
75% negative answers:

"not sr", "ntsr", "not sur", "не уверен", "ne uveren", "hoty glaza vikoli", "ns", "i don't know", "idk", "i dont know", "ну"
'''
    bot.reply_to(message, text6)

@bot.message_handler(commands=["creators"])
def creators_name(message):
    text7="Akinator has created by ???"
    bot.reply_to(message,text7)

@bot.message_handler(commands=["updates"])
def update_information_ver(message):
    text8=";] Don't have information yet"
    bot.reply_to(message,text8)

@bot.message_handler(commands=["statistics"])
def statistic(message):
    chat_id = message.chat.id
    session = get_session(chat_id)
    text4=f" Akinator's wins - {session['akinator_wins']}; user's wins - {session['user_wins']}"
    bot.reply_to(message,text4)

@bot.message_handler(commands=["extra"])
def extra(message):
    text9="Sometimes you can see empty question, it's server problem"
    bot.reply_to(message,text9)

@bot.message_handler(commands=["play"])
def playing(message):
    chat_id = message.chat.id
    clear_user_history(chat_id)
    text3_1="Game has begun"
    text3 = play(chat_id)
    bot.reply_to(message, text3_1)
    time.sleep(3)
    bot.reply_to(message, text3)

@bot.message_handler(content_types=["text"])
def akinator_text(message):
    text5 = message.text
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, "typing")
    bot.reply_to(message,play(chat_id, text5))
bot.infinity_polling()