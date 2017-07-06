from flask import Flask

import random
from api import Repositorie
from bot_types import Commands
import telebot
import os
from telebot import types
from emoji import emojize

from secrets import TOKEN

bot = telebot.TeleBot(TOKEN)
me = bot.get_me()

commands = Commands()
repos = Repositorie()

# Messages
others_messages = [
    "Ok, here's other stuff to check out",
    "Well, select a new theme",
    "What about you want learning?"
]

app = Flask(__name__)


# "Hi! I’m RafaelFelipebot.
# Rafael create me for help you to know some informations about him.
# Ask me about academic or professional life and I’ll send you"


# Options menu
############################################################################################
def menu_education():
    markup = types.InlineKeyboardMarkup()
    degree = types.InlineKeyboardButton("Degree", callback_data=commands.degree)
    exchange = types.InlineKeyboardButton("Exchange program", callback_data=commands.exchange)
    markup.add(degree, exchange)
    return markup


def menu_languages():
    markup = types.InlineKeyboardMarkup()
    portuguese = types.InlineKeyboardButton("Portuguese", callback_data=commands.pt)
    spanish = types.InlineKeyboardButton("Spanish", callback_data=commands.es)
    english = types.InlineKeyboardButton("English", callback_data=commands.en)
    later = types.InlineKeyboardButton("Later", callback_data=commands.later)
    markup.add(portuguese, spanish, english, later)
    return markup


def menu_yes_no(call_yes, call_no):
    markup = types.InlineKeyboardMarkup();
    yes = types.InlineKeyboardButton("Yes", callback_data=call_yes)
    no = types.InlineKeyboardButton("No", callback_data=call_no)
    markup.add(yes, no)
    return markup


def menu_thesis():
    markup = types.InlineKeyboardMarkup();
    yes = types.InlineKeyboardButton("Get thesis", callback_data='thesis_yes')
    other = types.InlineKeyboardButton("Other topics", callback_data=commands.other_topics)
    markup.add(yes, other)
    return markup


def menu_resume():
    markup = types.InlineKeyboardMarkup();
    yes = types.InlineKeyboardButton("Get resume", callback_data='resume_yes')
    other = types.InlineKeyboardButton("Other topics", callback_data=commands.other_topics)
    markup.add(yes, other)
    return markup


def menu_other_topcs():
    markup = types.InlineKeyboardMarkup();
    other = types.InlineKeyboardButton("Other topics", callback_data=commands.other_topics)
    markup.add(other)
    return markup


def menu_main_topcs():
    markup = types.InlineKeyboardMarkup();
    education = types.InlineKeyboardButton("Education", callback_data=commands.education)
    career = types.InlineKeyboardButton("Career", callback_data=commands.carrer)
    contact = types.InlineKeyboardButton("Contact", callback_data=commands.contact)
    portfolio = types.InlineKeyboardButton("Github", callback_data=commands.github)
    markup.add(education, career, contact, portfolio)
    return markup


############################################################################################

def show_repositories(message):
    list = repos.getRepositories()
    return list


def show_main_topics(message):
    x = random.randint(0, others_messages.__len__() - 1)
    bot.send_message(message.chat.id, others_messages[x], reply_markup=menu_main_topcs())


def show_other_topics(message):
    x = random.randint(0, others_messages.__len__() - 1)
    bot.send_message(message.chat.id, others_messages[x], reply_markup=menu_other_topcs())


def show_github(message):
    bot.send_message(message.chat.id,
                     "Wait a little moment " + message.chat.first_name + "... I will get it from his Github")
    list = show_repositories(message)
    name = ""
    for rep in list:
        name = name + (rep['html_url']) + "\n"
    bot.send_message(message.chat.id, name)
    bot.send_message(message.chat.id, "These are Rafael's repositories")


# Show information about Education
def show_education(message):
    bot.send_message(message.chat.id, "Great!")
    bot.send_message(message.chat.id,
                     "Great! Rafael loves learning new things! He's passionate for tecnology\nI hope that one day his make me talk " + emojize(
                         ":smile:", use_aliases=True), reply_markup=menu_education())


# Show information about Degree
def show_degree(message):
    bot.send_message(message.chat.id, "He got his degree in System Analisys Development at FATEC/SP.")
    bot.send_message(message.chat.id, "Do you want I send you his undergraduate thesis?",
                     reply_markup=menu_thesis())


# Show information about Spain exchange
def show_exchange(message):
    bot.send_message(message.chat.id,
                     "Rafael got a scholarship to study in Spain. The brazilian exchange program's name is 'Ciência sem Fronteiras'")
    bot.send_message(message.chat.id, "He studied for one year 2013-2014, at 'Universidad Autónoma de Madrid'")
    bot.send_message(message.chat.id, "In Spain he can improves his spanish.")
    show_languages(message)


def show_contact(message):
    bot.send_message(message.chat.id,
                     "Hey, it's hin email, rafael.felipe1989@gmail.com")
    bot.send_message(message.chat.id, "If you want, add Rafael on Skype, rafaelfelipe.info",
                     disable_web_page_preview=True)
    bot.send_message(message.chat.id, "In Linkedin has more information and detail https://goo.gl/bEagSw")
    bot.send_message(message.chat.id, "It's a personal page. rafaelcrz.github.io")


# Show the languages
def show_languages(message):
    bot.send_message(message.chat.id, "Listen he talks", reply_markup=menu_languages())


############################################################################################
# Telebot Handlers

# User send 'start' command
@bot.message_handler(commands=[commands.start])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi " + message.chat.first_name + emojize(":smile:", use_aliases=True))
    bot.send_message(message.chat.id, "What do you want know about?", disable_notification=True,
                     reply_markup=menu_main_topcs())


# User send any test message (not a command)
@bot.message_handler()
def send_sorry(message):
    bot.send_message(message.chat.id,
                     "I'm sorry, I cant talk using sentences, but I promess in my next version, I will do it.\n")
    bot.send_message(message.chat.id, "But this is some topics for you")
    show_main_topics(message)


# User select a option in the menu
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    if call.message:
        if call.data == commands.education:
            show_education(call.message)
        elif call.data == commands.carrer:
            bot.send_message(call.message.chat.id,
                             "He was trainee in LexTrend a IT company in Madrid.\nAt now he's searching for an oportunity as Android developer jr\nHe's studing Python and Chatbots")
            bot.send_message(call.message.chat.id, "Do you want I send you his resume?",
                             reply_markup=menu_resume())
        elif call.data == commands.degree:
            show_degree(call.message)
        elif call.data == commands.exchange:
            show_exchange(call.message)
        elif call.data == "thesis_yes":
            send_cv(call.message, "thesis")
            bot.send_message(call.message.chat.id, "Rafael have to studied in Spain. Can I tell you a about?",
                             reply_markup=menu_yes_no("exchange_yes", "exchange_no"))
        elif call.data == "resume_yes":
            send_cv(call.message, "resume")
            show_other_topics(call.message)
        elif call.data == "exchange_yes":
            show_exchange(call.message)
        elif call.data == "exchange_no":
            show_other_topics(call.message)
        elif call.data == commands.pt:
            bot.send_message(call.message.chat.id,
                             "Wait a moment, I will send you the audio")
            send_audio(call.message, commands.pt)
            bot.send_message(call.message.chat.id, "It's his native language =D \nSelect other language")
            show_languages(call.message)
        elif call.data == commands.es:
            bot.send_message(call.message.chat.id,
                             "Wait a moment, I will send you the audio")
            send_audio(call.message, commands.es)
            bot.send_message(call.message.chat.id,
                             "A Rafael le gusta mucho el español! A ver cuando le toca volver a España")
            show_languages(call.message)
        elif call.data == commands.en:
            bot.send_message(call.message.chat.id,
                             "Wait a moment, I will send you the audio")
            send_audio(call.message, commands.en)
            bot.send_message(call.message.chat.id,
                             "I know his English is some basic, but he has studied very hard for improve it")
            show_languages(call.message)
        elif call.data == commands.later:
            show_main_topics(call.message)
        elif call.data == commands.other_topics:
            show_main_topics(call.message)
        elif call.data == commands.contact:
            show_contact(call.message)
            show_main_topics(call.message)

        elif call.data == commands.github:
            show_github(call.message)
            show_other_topics(call.message)


# Send a message voice
def send_audio(message, language):
    voice = open('files/voice_' + language + ".ogg", 'rb')
    bot.send_voice(message.chat.id, voice)


# Send a pdf CV
def send_cv(message, document):
    doc = open('files/' + document + '.pdf', 'rb')
    bot.send_document(message.chat.id, doc)
    bot.send_message(message.chat.id, "Thank's for you interess")


# bot.polling()


############################################################################################
# Flask implementation

@app.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://rafaelfelipebot.herokuapp.com/bot")  # rafaelfelipebot
    bot.polling()  # none_stop=False
    return "!", 200  # 'It works!'


app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
app = Flask(__name__)

# if __name__ == "__main__":
#    app.run()
