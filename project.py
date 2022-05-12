# ---------------------------> modules < ---------------------------
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.chataction import ChatAction
from telegram import ReplyKeyboardMarkup
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
import requests
# ---------------------------> token < ---------------------------
updater = Updater(token="your token",use_context=True)
# ---------------------------> api < ---------------------------
api = "https://min-api.cryptocompare.com/data/price?fsym={currency}&tsyms=USD,GBP,EUR,TRY,IRR,SUR,KWD,JPY,CNY,CAD,AUD"
# ---------------------------> bot messages < ---------------------------
messages = {
    "help_msg" : "Hey guys\nfor getting prices  write /getprice <code of currnecy>",
    "start_msg" : "Hello he/she {} Welcome to the bot\n you can get prices from me;)",
    "menu_msg" : "menu:",
    "src_msg" : "The source code of bot is on my github:)\nMy github : your github",
    "support_btn" : "Support",
    "src_btn" : "Source Code",
    "back_btn" : "Back",
    "contact_us_msg" : "your social medias",
    "list_crypto" : "list of crypto currencies",
    "list_money" : "list of moneys",
    "list_crypto_link" : "https://coinmarketcap.com/all/views/all/",
    "list_money_link" : "https://www.xe.com/iso4217.php"
    }
# ---------------------------> /start < ---------------------------
def start(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    context.bot.send_chat_action(chat_id,ChatAction.TYPING )
    update.message.reply_text(text=messages["start_msg"].format(first_name))
    update.message.reply_text(text=messages["help_msg"])
    menu(update, context)
# ---------------------------> /help < ---------------------------
def Help(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING )
    update.message.reply_text(text=messages["help_msg"])
# ---------------------------> /getprice < ---------------------------
def price(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    currency = update.message.text.split()[1]
    response = requests.get(api.format(currency=currency)).json()
    message = f"Now the {currency} of price is :\n{response['USD']}\U0001F1FA\U0001F1F8\n{response['GBP']}\U0001F1EC\U0001F1E7\n{response['EUR']}\U0001F1EA\U0001F1FA\n{response['TRY']}\U0001F1F9\U0001F1F7\n{response['IRR']}\U0001F1EE\U0001F1F7\n{response['SUR']}\U0001F1F7\U0001F1FA\n{response['KWD']}\U0001F1F0\U0001F1FC\n{response['JPY']}\U0001F1EF\U0001F1F5\n{response['CNY']}\U0001F1E8\U0001F1F3\n{response['CAD']}\U0001F1E8\U0001F1E6\n{response['AUD']}\U0001F1E6\U0001F1FA"
    context.bot.send_chat_action(chat_id,ChatAction.TYPING )
    update.message.reply_text(message)
# ---------------------------> /about < ---------------------------
def about(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    update.message.reply_text(text=messages["contact_us_msg"])
# ---------------------------> /code < ---------------------------
def code(update : Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["src_msg"])
# ---------------------------> /cryptocurrencies < ---------------------------
def cryptocurrencies(update : Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["list_crypto_link"])
# ---------------------------> /moneys < ---------------------------
def moneys(update : Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["list_money_link"])
# ---------------------------> menu < ---------------------------
def menu(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["support_btn"]], [messages["src_btn"]], [messages["list_crypto"]], [messages["list_money"]]
    ]
    context.bot.send_chat_action(chat_id,ChatAction.TYPING )
    update.message.reply_text(
        text=messages["menu_msg"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> support button < ---------------------------
def support(update : Update , context : CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id,ChatAction.TYPING )
    update.message.reply_text(
        text=messages["contact_us_msg"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> source code button < ---------------------------
def source_code(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["src_msg"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# --------------------------- > list of crypto currencies button < ---------------------------
def list_crypto(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    buttons =[
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.FIND_LOCATION)
    update.message.reply_text(
        text=messages["list_crypto_link"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# --------------------------- > list of moneys < ---------------------------
def list_money(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    buttons =[
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.FIND_LOCATION)
    update.message.reply_text(
        text=messages["list_money_link"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> /back < ---------------------------
def back(update : Update, context : CallbackContext):
    menu(update, context)
# ---------------------------> run < ---------------------------
def run():
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("getprice", price))
    updater.dispatcher.add_handler(CommandHandler("help", Help))
    updater.dispatcher.add_handler(CommandHandler("about", about))
    updater.dispatcher.add_handler(CommandHandler("code", code))
    updater.dispatcher.add_handler(CommandHandler("cryptocurrencies", cryptocurrencies))
    updater.dispatcher.add_handler(CommandHandler("moneys", moneys))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["support_btn"]),support))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["src_btn"]),source_code))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_crypto"]),list_crypto))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_money"]),list_money))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["back_btn"]),back))
    updater.start_polling()
    updater.idle()
run()
