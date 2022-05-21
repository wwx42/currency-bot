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
updater = Updater(token="Your token",use_context=True)
# ---------------------------> api < ---------------------------
api = "https://min-api.cryptocompare.com/data/price?fsym={currency}&tsyms=USD,GBP,EUR,TRY,IRR,SUR,KWD,JPY,CNY,CAD,AUD"
# ---------------------------> bot messages < ---------------------------
messages = {
    "start_msg" : "Hello dear {}, Welcome to the bot\n you can get prices from me;)",
    "help_msg" : "Dear {}\nThe purpose of the robot:\nThe purpose of making such a bot is to get different and abundant currency prices for dear Telegram users :)\n-----------------------------------------\nHow it works\nfor get prices of considered currency you should start by /getprice and a space then write your currency iso code(note : you can get list of iso code from buttons.)\nresult : /getprice <currency iso code>\n-----------------------------------------\nExample\nSo if you want get bitcoin(BTC or btc) write /getprice BTC or /getprice btcOr for get american dollar(USD or usd) write /getprice USD or /getprice usd\n-----------------------------------------\nSupport:\nif bot has any error you can click support button then message to me from social medias;)\n-----------------------------------------\nSource code:\nDear Dev, you can get source code from my github just click source code button:)))\n-----------------------------------------\nMore:\nIf you have trouble finding the currency identifiers, do not worry: you can find those currencies by pressing another button.",
    "menu_msg" : "Menu:",
    "more_msg" : "More:",
    "src_msg" : "The source code of bot is on my github:)\nMy github : your github",
    "more_btn" : "More",
    "support_btn" : "Support",
    "src_btn" : "Source Code",
    "back_btn" : "Back",
    "contact_us_msg" : "Telegram : @your telegram\nInstagram : your instagram\nTwitter : your twitter\nGithub : your github\nLinkedin : your linkedin\nFacebook : your facebook\nDiscord : your discord",
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
    update.message.reply_text(text="If you need help write /help:)")
    menu(update, context)
# ---------------------------> /help < ---------------------------
def Help(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    context.bot.send_chat_action(chat_id,ChatAction.TYPING )
    update.message.reply_text(text=messages["help_msg"].format(first_name))
# ---------------------------> /getprice < ---------------------------
def price(update : Update, context : CallbackContext):
    try:
        chat_id = update.message.chat_id
        currency = update.message.text.split()[1]
        response = requests.get(api.format(currency=currency)).json()
        message = f"Now the {currency.upper()} of price is :\n{response['USD']}\U0001F1FA\U0001F1F8\n{response['GBP']}\U0001F1EC\U0001F1E7\n{response['EUR']}\U0001F1EA\U0001F1FA\n{response['TRY']}\U0001F1F9\U0001F1F7\n{response['IRR']}\U0001F1EE\U0001F1F7\n{response['SUR']}\U0001F1F7\U0001F1FA\n{response['KWD']}\U0001F1F0\U0001F1FC\n{response['JPY']}\U0001F1EF\U0001F1F5\n{response['CNY']}\U0001F1E8\U0001F1F3\n{response['CAD']}\U0001F1E8\U0001F1E6\n{response['AUD']}\U0001F1E6\U0001F1FA"
        context.bot.send_chat_action(chat_id,ChatAction.TYPING )
        update.message.reply_text(message)
    except KeyError:
        update.message.reply_text(f"{currency.upper()} is not defind!")
# ---------------------------> /about < ---------------------------
def about(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    update.message.reply_text(text=messages["contact_us_msg"])
# ---------------------------> /code < ---------------------------
def src(update : Update, context: CallbackContext):
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
        [messages["support_btn"]], [messages["src_btn"]], [messages['more_btn']]
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
# ---------------------------> More button < ---------------------------
def more(update : Update, context : CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["list_crypto"]], [messages["list_money"]], [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    update.message.reply_text(
        text=messages["more_msg"],
        reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True)
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
    updater.dispatcher.add_handler(CommandHandler("src", src))
    updater.dispatcher.add_handler(CommandHandler("cryptocurrencies", cryptocurrencies))
    updater.dispatcher.add_handler(CommandHandler("moneys", moneys))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["menu_msg"]),menu))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["more_btn"]),more))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["support_btn"]),support))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["src_btn"]),source_code))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_crypto"]),list_crypto))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_money"]),list_money))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["back_btn"]),back))
    updater.start_polling()
    updater.idle()
run()
