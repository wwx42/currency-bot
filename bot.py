# ---------------------------> modules < ---------------------------
from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from telegram.chataction import ChatAction
from datetime import datetime
import requests
import pytz
# ---------------------------> token < ---------------------------
updater = Updater(token="Your token", use_context=True)
# ---------------------------> api < ---------------------------
api = "https://min-api.cryptocompare.com/documentation"
# ---------------------------> bot messages < ---------------------------
messages = {
    "start_msg": "Hello Dear {}, welcome to the robot\n\nIf you need help, you can write /help :)",
    "help_msg" : "Dear user {} \U0001F601\nRobot target \U0001F3AF\nThe purpose of building such a robot is to receive the price of different and abundant currencies for dear Telegram users :)\nHow it works\U0001F9BE\nTo get the target currency price you have to start from /getprice and write a space and then your currency iso code (note: you can get the list of iso codes from the buttons.)\nResult : /getprice <currency iso code>\nExample\nSo if you want to get bitcoin (BTC or btc), write /getprice BTC or /getprice btc or write to get US dollars (USD or USD) /getprice USD or /getprice usd\nLlist of crypot currencies\nSample of the best crypto currencies and more...\nList of moneys\nSample of best moneys and more...\nMore\nIf you have trouble finding currency identifiers, do not worry: you can find those currencies by pressing another button.",
    "menu_msg": "Menu:",
    "more_msg": "More:",
    "list_crypto_msg": "Ten of the best Crypto currencies with ISO code:\n\n1. Bitocin --------------> /getprice BTC\n\n2. Ethereum -------------> /getprice ETH\n\n3. Tether ----------------------> /getprice USD\n\n4. Binance -------------------------> /getprice BNB\n\n5. Solona -------------------------------> /getprice  SOL\n\n6. Doge Coin -------------------------> /getprice  DOGE\n\n7. Tron -----------------------------> /getprice TRX\n\n8. Shiba Inu ------------------> /getprice SHIB\n\n9. Bitcon Cash -----------> /getprice BCH\n\n10. Kardano ----------> /getprice ADA\n\nClick on the more button for more Crypto currencies ...",
    "list_money_msg": "Ten of the best Moneys with ISO code:\n\n1. American dollar -> /getprice USD\n\n2. European euro -----> /getprice EUR\n\n3. Sterling pound ------> /getprice GBP\n\n4. Arab dirham -----------> /getprice AED\n\n5. Russian ruble ----------> /getprice RUB\n\n6. Kuweit dinar -----------> /getprice KWD\n\n7. Japanese yen ----------> /getprice JPY\n\n8. Sweden krona -----> /getprice SEK\n\n9. Turkish lira ------> /getprice TRY\n\n10. Iranian rial -> /getprice IRR\n\nClick on the more button for more Moneys ...",
    "src_msg": "The source code of the robot is in my github :)\nMy github : Your github",
    "more_btn": "More",
    "support_btn": "Support",
    "src_btn": "Source Code",
    "back_btn": "Back",
    "list_crypto": "List of Crypto Currencies",
    "list_money": "List of Moneys",
    "list_crypto_link": "https://coinmarketcap.com/all/views/all/",
    "list_money_link": "https://www.xe.com/iso4217.php"
}
# ---------------------------> /start < ---------------------------
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=(messages["start_msg"].format(first_name)))
    menu(update, context)
# ---------------------------> /help < ---------------------------
def h(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["help_msg"].format(first_name))
# ---------------------------> /getprice < ---------------------------
def price(update: Update, context: CallbackContext):
    try:
        chat_id = update.message.chat_id
        currency = update.message.text.split()[1]
        response = requests.get(api.format(currency=currency)).json()
        timezone = pytz.timezone("UTC")
        date_time = datetime.now(timezone)
        time = date_time.strftime("%d/%m/%Y %H:%M")
        message = f"In {time}\n\nThe price of {currency.upper()} is:\n\n{response['USD']:,} \U0001F1FA\U0001F1F8\n\n{response['GBP']:,} \U0001F1EC\U0001F1E7\n\n{response['EUR']:,} \U0001F1EA\U0001F1FA\n\n{response['TRY']:,} \U0001F1F9\U0001F1F7\n\n{response['IRR']:,} \U0001F1EE\U0001F1F7\n\n{response['SUR']:,} \U0001F1F7\U0001F1FA\n\n{response['KWD']:,} \U0001F1F0\U0001F1FC\n\n{response['AED']:,} \U0001F1E6\U0001F1EA\n\n{response['JPY']:,} \U0001F1EF\U0001F1F5\n\n{response['CNY']:,} \U0001F1E8\U0001F1F3\n\n{response['CAD']:,} \U0001F1E8\U0001F1E6\n\n{response['AUD']:,} \U0001F1E6\U0001F1FA"
        context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        update.message.reply_text(message)
    except KeyError:
        update.message.reply_text(f"{currency.upper()} is not defined!")
# ---------------------------> /about < ---------------------------
def about(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text='Telegram : @Telegram id\n\nGithub : [Your github id](Your github link)\n\nLinkedin : [Your linkedin id](Your linkedin link)\n\nInstagram : [Your instagram id ](Your instagram link)\n\nTwitter : [Your twitter id ](Your twitter link)\n\n', parse_mode='MarkdownV2',disable_web_page_preview=True)
# ---------------------------> /code < ---------------------------
def src(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["src_msg"])
# ---------------------------> /cryptocurrencies < ---------------------------
def cryptocurrencies(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["list_crypto_link"])
# ---------------------------> /moneys < ---------------------------
def moneys(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["list_money_link"])
# ---------------------------> menu < ---------------------------
def menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["list_crypto"], messages["list_money"]],
        [messages['more_btn']]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["menu_msg"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> support button < ---------------------------
def support(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text='Telegram : @Telegram id\n\nGithub : [Your github id](Your github link)\n\nLinkedin : [Your linkedin id](Your linkedin link)\n\nInstagram : [Your instagram id ](Your instagram link)\n\nTwitter : [Your twitter id ](Your twitter link)\n\n', parse_mode='MarkdownV2',disable_web_page_preview=True,
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> source code button < ---------------------------
def source_code(update: Update, context: CallbackContext):
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
def list_crypto(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [
            InlineKeyboardButton(text="more",url="https://coinmarketcap.com/all/views/all/")
        ]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["list_crypto_msg"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )
# --------------------------- > list of moneys < ---------------------------
def list_money(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [
            InlineKeyboardButton(text="more",url="https://www.xe.com/iso4217.php")
        ]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["list_money_msg"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )
# ---------------------------> more button < ---------------------------
def more(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["support_btn"], messages["src_btn"]],
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["more_msg"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> more button 2 < ---------------------------
def more2(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["list_crypto_link"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> more button 3 < ---------------------------
def more3(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    buttons = [
        [messages["back_btn"]]
    ]
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["list_money_link"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )
# ---------------------------> /back < ---------------------------
def back(update: Update, context: CallbackContext):
    menu(update, context)
# ---------------------------> run < ---------------------------
def run():
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("getprice", price))
    updater.dispatcher.add_handler(CommandHandler("help", h))
    updater.dispatcher.add_handler(CommandHandler("about", about))
    updater.dispatcher.add_handler(CommandHandler("src", src))
    updater.dispatcher.add_handler(CommandHandler("cryptocurrencies", cryptocurrencies))
    updater.dispatcher.add_handler(CommandHandler("moneys", moneys))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["menu_msg"]), menu))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["more_btn"]), more))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["support_btn"]), support))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["src_btn"]), source_code))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_crypto"]), list_crypto))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_money"]), list_money))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["back_btn"]), back))
    updater.start_polling()
    updater.idle()
run()
