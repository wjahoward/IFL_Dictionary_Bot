"""
    <summary>
        This solution file creates a simple and usable telegram bot for FYP
    </summary>

    <author>
        @wgl_vin from SP DBKF
        @wja_howard from SP DIT
        @itstknotok from SP DIT
    </author>

    The code is strictly for view only, it is copyright infringement to remove this line. Anyone who conducts a copyright will be liable to be sued, unless there has been approval from either one of the 3 names mentioned above.
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackQueryHandler, Updater, CallbackContext, MessageHandler, CommandHandler, Filters, commandhandler

import pandas as pd
import telepot

BOT = telepot.Bot("<insert_bot_father_secret_token>")
UPDATER = Updater("<insert_bot_father_secret_token>", use_context=True)
DP = UPDATER.dispatcher
FIRST_COLUMN_OF_EXCEL_FILE = 0
SECOND_COLUMN_OF_EXCEL_FILE = 1
THIRD_COLUMN_OF_EXCEL_FILE = 2
FOURTH_COLUMN_OF_EXCEL_FILE = 3
FILE_NAME= 'finlit.xlsx'
HELP_URL = 'https://ifl.org.sg/'
SORRY_MSG = "Sorry, I do not understand you. Please check if you have spelled the word correctly. If it is correct, please press the link /feedback to update us on the new term you want us to include in our update"
AVAILABLE_BUTTONS = ["yes_no", "understood_chat"]
YES_NO_BUTTONS = ["ABUDEN", "I BLUR SOTONG"]
UNDERSTOOD_CHAT_BUTTONS = ["HOSEH LIAO", "CATCH NO BALL"]
FIRST_BUTTON_INDEX = 0
SECOND_BUTTON_INDEX = 1

def get_inline_keyboard(type_of_question):

    button_one = ""
    button_two = ""

    if type_of_question == AVAILABLE_BUTTONS[FIRST_BUTTON_INDEX]:
        button_one = YES_NO_BUTTONS[FIRST_BUTTON_INDEX]
        button_two = YES_NO_BUTTONS[SECOND_BUTTON_INDEX] 
    elif type_of_question == AVAILABLE_BUTTONS[SECOND_BUTTON_INDEX]:
        button_one = UNDERSTOOD_CHAT_BUTTONS[FIRST_BUTTON_INDEX]
        button_two = UNDERSTOOD_CHAT_BUTTONS[SECOND_BUTTON_INDEX] 

    keyboard = [
        [
            InlineKeyboardButton(button_one, callback_data=button_one),
            InlineKeyboardButton(button_two, callback_data=button_two),
        ]
    ]

    return keyboard

def get_keyboard(button_type, update):
        keyboard = get_inline_keyboard(button_type)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Do you understand what " + term + " means?", reply_markup=reply_markup)

def get_excel_data():

    cols = 'A:D' # This is based on the column you want to use: A is 0, B is 1, C is 2, D is 3 
    terms = pd.read_excel(FILE_NAME, sheet_name=0,usecols=cols,header=0)
    termsArr = terms.to_numpy()

    return termsArr

def echo(update: Update, context: CallbackContext):
    global youtube_url, term, type_of_button
    command = update.message.text.lower()

    termsArr = get_excel_data()

    for word in termsArr:
        if command in word[FIRST_COLUMN_OF_EXCEL_FILE].lower():
            youtube_url = word[FOURTH_COLUMN_OF_EXCEL_FILE]
            update.message.reply_text(word[SECOND_COLUMN_OF_EXCEL_FILE])
            update.message.reply_text(word[THIRD_COLUMN_OF_EXCEL_FILE])
            term = word[FIRST_COLUMN_OF_EXCEL_FILE]

            type_of_button = AVAILABLE_BUTTONS[FIRST_BUTTON_INDEX]
            get_keyboard(button_type = type_of_button, update = update)

            return
    
    update.message.reply_text(SORRY_MSG)

def button(update: Update, context: CallbackContext):
    global type_of_button  
    query = update.callback_query

    query.answer()

    message = query.data

    if type_of_button == AVAILABLE_BUTTONS[FIRST_BUTTON_INDEX]:
        if message == YES_NO_BUTTONS[FIRST_BUTTON_INDEX]:
            query.message.reply_text("Thanks for dropping by today!")
            return
        elif message == YES_NO_BUTTONS[SECOND_BUTTON_INDEX]:
            query.message.reply_text("Hi, here is your link for " + term + " : " + youtube_url)
            type_of_button = AVAILABLE_BUTTONS[SECOND_BUTTON_INDEX]
            get_keyboard(button_type = type_of_button, update = query)
    elif type_of_button == AVAILABLE_BUTTONS[SECOND_BUTTON_INDEX]:
        if message == UNDERSTOOD_CHAT_BUTTONS[SECOND_BUTTON_INDEX]:
            query.message.reply_text("Hi, it seems that you need help! We will be redirecting you to this url so that you can speak with one of our trainers : " + HELP_URL)       
            query.message.reply_text("If you are unable to access the link, it could be because that the server is down or our trainers are currently busy. Do let our trainers know what you want to enquire about")
            return
        elif message == UNDERSTOOD_CHAT_BUTTONS[FIRST_BUTTON_INDEX]:
            query.message.reply_text("Hope the video was useful!")
            return

def start(update, context):
    update.message.reply_text("Welcome to ATLAS Dictionary! Enter any terms that you are unfamiliar with! Enter /help to ...")

def help(update, context):
    update.message.reply_text("What do you need help with?")

def about(update, context):
    update.message.reply_text("This bot helps youths to gain some financial knowledge of terms that are commonly used so as to make sound financial decisions and hence distinguish prejudiced opinions of financial products.")

def main():
    # main code to run the function
    DP.add_handler(CommandHandler("start", start))
    DP.add_handler(CommandHandler("help", help))
    DP.add_handler(CommandHandler("about", about))

    DP.add_handler(MessageHandler(Filters.text, echo))
    DP.add_handler(CallbackQueryHandler(button))

    UPDATER.start_polling()
    UPDATER.idle()

main()