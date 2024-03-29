# By MMX24
# ---------------------------> modules < ---------------------------
from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import error
from telegram.chataction import ChatAction
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from datetime import datetime
from pandas_datareader import DataReader
from pandas_datareader._utils import RemoteDataError
import mplfinance as mpfl
import requests
import pytz
import logging
# ---------------------------> database < ---------------------------
logging.basicConfig(filename="data.log", filemode="a", level=logging.INFO, format="%(asctime)s-%(filename)s-%(message)s")
# ---------------------------> token < ---------------------------
updater = Updater(token="your token", use_context=True)
# ---------------------------> api < ---------------------------
api = "https://min-api.cryptocompare.com/data/price?fsym={currency}&tsyms=USD,GBP,EUR,TRY,IRR,RUB,KWD,JPY,CNY,CAD,AUD,AED,CHF,BRL,INR"
# ---------------------------> bot messages < ---------------------------
messages = {
    "start_msg": "Hello Dear {}-({}), welcome to the robot\n\nIf you need help, you can write /help :)",
    "help_msg" : "Dear user {} \U0001F601\nRobot target \U0001F3AF\nThe purpose of building such a robot is to receive the price of different and abundant currencies for dear Telegram users :)\nHow it works\U0001F9BE\nTo get the target currency price you have to start from /getprice and write a space and then your currency iso code (note: you can get the list of iso codes from the buttons.)\nResult : /getprice <currency iso code>\nAnd for chart \U0001F4C8\nif you want get bitcoin or other, you should write /getchart BTC USD\nResult\n/getchart <iso code> <iso code2>\nExample\nSo if you want to get bitcoin (BTC or btc), write /getprice BTC or /getprice btc or write to get US dollars (USD or usd) /getprice USD or /getprice  and for chart of bitcoin you should write /getchart BTC USD or /getprice btc and...\nFor get time of market you should write /gettime\ncrypto currency\nSample of the best crypto currencies and more...\nmoney\nSample of best moneys and more...\ncompany\nSample of the best companies and more...\nMore\nIf you have trouble finding currency identifiers, do not worry: you can find those currencies by pressing another button.\n\nP.N. For feedback write /feedback=)",
    "menu_msg": "Menu:",
    "more_msg": "More:",
    "list_crypto_msg" : "Ten of the best Crypto currencies with ISO code:\n\n1.Bitocin --------------> /getprice BTC\n1.Bitocin ----------> /getchart BTC USD\n\n2.Ethereum -------------> /getprice ETH\n2.Ethereum ----------> /getchart ETH USD\n\n3.Tether ----------------------> /getprice USDT\n3.Tether ------------------> /getchart USDT USD\n\n4.Binance -------------------------> /getprice BNB\n4.Binance ----------------------> /getchart BNB USD\n\n5.Solona -------------------------------> /getprice  SOL\n5.Solona ---------------------------> /getchart SOL USD\n\n6.Doge Coin ---------------------> /getprice  DOGE\n6.Doge Coin -----------------> /getchart DOGE USD\n\n7.Tron -----------------------------> /getprice TRX\n7.Tron -------------------------> /getchart TRX USD\n\n8.Shiba Inu ------------------> /getprice SHIB\n8.Shiba Inu --------------> /getchart SHIB USD\n\n9.Bitcon Cash -----------> /getprice BCH\n9.Bitcon Cash -------> /getchart BCH USD\n\n10.Cardano ----------> /getprice ADA\n10.Cardano ------> /getchart ADA USD\n\nClick on the more button for more Crypto currencies ...",
    "list_money_msg": "Ten of the best Moneys with ISO code:\n\n1.American dollar -> /getprice USD\n\n2.European euro -----> /getprice EUR\n\n3.Sterling pound ------> /getprice GBP\n\n4.Arab dirham -----------> /getprice AED\n\n5.Russian ruble ----------> /getprice RUB\n\n6.Kuweit dinar -----------> /getprice KWD\n\n7.Japanese yen ----------> /getprice JPY\n\n8.Sweden krona -----> /getprice SEK\n\n9.Turkish lira ------> /getprice TRY\n\n10.Iranian rial -> /getprice IRR\n\nClick on the more button for more Moneys ...",
    "list_company_msg" : "Five of the best Companies with ISO code:\n\n1.Apple ----------> /getchart AAPL USD\n\n2.Google ------------------> /getchart GOOGL USD\n\n3.Amazon ---------------------> /getchart AMZN USD\n\n4.Tesla -------------------> /getchart TSLA USD\n\n5.Alibaba --------> /getchart BABA USD\n\nClick on the more button for more...",
    "feedback_msg" : "Thanks for feedback🙏🙏",
    "src_msg": "The source code of the robot is in my github :)\nMy github : https://github.com/wwx42/currency-bot.git",
    "more_btn": "More",
    "support_btn": "Support",
    "src_btn": "Source Code",
    "back_btn": "Back",
    "feedback_btn" : "Feedback",
    "list_crypto": "Crypto Currency",
    "list_money": "Money",
    "list_company" : "Company",
    "list_crypto_link": "https://coinmarketcap.com/all/views/all/",
    "list_money_link": "https://www.xe.com/iso4217.php",
    "list_company_link" : "https://www.nasdaq.com/market-activity/stocks/screener"
}
try :
# ---------------------------> /start < ---------------------------
    def start(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        name = update.message.chat.full_name
        acc_id = update.message.chat.id
        username = update.message.chat.username
        context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        update.message.reply_text(text=(messages["start_msg"].format(name,acc_id)))
        menu(update, context)
        logging.info("[+]({} - {} - @{}) started the bot.".format(name, chat_id,username))
# ---------------------------> /help < ---------------------------
    def h(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        name = update.message.chat.full_name
        context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        update.message.reply_text(text=messages["help_msg"].format(name))
# ---------------------------> /getprice < ---------------------------
    def price(update: Update, context: CallbackContext):
        try:
            chat_id = update.message.chat_id
            currency = update.message.text.split()[1]
            response = requests.get(api.format(currency=currency)).json()
            timezone = pytz.timezone("UTC")
            date_time = datetime.now(timezone)
            time = date_time.strftime("%d/%m/%Y %H:%M:%S")
            message = f"In {time}\n\nThe price of {currency.upper()} is:\n\n{response['USD']:,} \U0001F1FA\U0001F1F8\n\n{response['GBP']:,} \U0001F1EC\U0001F1E7\n\n{response['EUR']:,} \U0001F1EA\U0001F1FA\n\n{response['TRY']:,} \U0001F1F9\U0001F1F7\n\n{response['IRR']:,} \U0001F1EE\U0001F1F7\n\n{response['RUB']:,} \U0001F1F7\U0001F1FA\n\n{response['KWD']:,} \U0001F1F0\U0001F1FC\n\n{response['AED']:,} \U0001F1E6\U0001F1EA\n\n{response['JPY']:,} \U0001F1EF\U0001F1F5\n\n{response['CNY']:,} \U0001F1E8\U0001F1F3\n\n{response['CAD']:,} \U0001F1E8\U0001F1E6\n\n{response['AUD']:,} \U0001F1E6\U0001F1FA\n\n{response['CHF']:,} \U0001F1E8\U0001F1ED\n\n{response['BRL']:,} \U0001F1E7\U0001F1F7\n\n{response['INR']:,} \U0001F1EE\U0001F1F3"
            context.bot.send_chat_action(chat_id, ChatAction.TYPING)
            update.message.reply_text(message)
        except KeyError:
            update.message.reply_text(f"{currency.upper()} is not defined !!!")
        except IndexError:
            update.message.reply_text("/getprice <currency> not only /getprice !!!")
# ---------------------------> /getchart < ---------------------------
    def chart(update: Update, context: CallbackContext):
        try:
            chat_id = update.message.chat_id
            start_time = datetime(2022, 1, 1)
            end_time = datetime.now()
            timezone = pytz.timezone("UTC")
            time = datetime.now(timezone)
            date = time.strftime("%d/%m/%Y %H:%M:%S")
            currency1 = update.message.text.split()[1]
            currency2 = update.message.text.split()[2]
            data = DataReader(f"{currency1}-{currency2}", "yahoo", start_time, end_time)
            mpfl.plot(data, style="yahoo", volume=True,type="candle", savefig="chart.png",title=f"{currency1.upper()}-{currency2.upper()} in 2022")
            with open("./chart.png", "rb") as img:
                context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
                context.bot.sendPhoto(chat_id, img, caption=f"The chart of {currency1.upper()}-{currency2.upper()} in {date}")
        except IndexError:
            update.message.reply_text("/getchart <currency_1> <currency_2>  not only /getchart !!!")
        except RemoteDataError:
            update.message.reply_text(f"{currency1.upper()}-{currency2.upper()} is not defined !!!")
# ---------------------------> /gettime < ---------------------------
    def time(update : Update, context : CallbackContext):
        chat_id = update.message.chat_id
        timezone = pytz.timezone("UTC")
        date_time = datetime.now(timezone)
        time = date_time.strftime("%d/%m/%Y %H:%M:%S")
        context.bot.send_chat_action(chat_id,ChatAction.TYPING)
        update.message.reply_text(text=f"Time of Market : {time}")
# ---------------------------> /about < ---------------------------
    def about(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        update.message.reply_text(text='Telegram : @codeit01\n\nGithub : [wwx42](https://github.com/wwx42)\n\nLinkedin : [Mahdi Mohammadkhani](https://www.linkedin.com/in/mahdi-mohammadkhani-6a4241237/)\n\nInstagram : [mmx24](https://www.instagram.com/mmx24/)\n\nTwitter : [mmx2442](https://twitter.com/mmx2442)\n\n', parse_mode='MarkdownV2',disable_web_page_preview=True)
# ---------------------------> /src < ---------------------------
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
# ---------------------------> /companies < ---------------------------
    def companies(update: Update,context: CallbackContext):
        chat_id = update.message.chat_id
        context.bot.send_chat_action(chat_id,ChatAction.TYPING)
        update.message.reply_text(text=messages["list_company_link"])
# ---------------------------> /feedback < ---------------------------
    def feedback(update : Update, context : CallbackContext):
        chat_id = update.message.chat_id
        context.bot.send_chat_action(chat_id,ChatAction.TYPING)
        update.message.reply_text(messages["feedback_msg"])
        update.message.forward(chat_id=5117722111)
# ---------------------------> menu < ---------------------------
    def menu(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        buttons = [
            [messages["list_crypto"], messages["list_money"]],
            [messages["list_company"], messages["more_btn"]]
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
            text='Telegram : @codeit01\n\nGithub : [wwx42](https://github.com/wwx42)\n\nLinkedin : [Mahdi Mohammadkhani](https://www.linkedin.com/in/mahdi-mohammadkhani-6a4241237/)\n\nInstagram : [mmx24](https://www.instagram.com/mmx24/)\n\nTwitter : [mmx2442](https://twitter.com/mmx2442)\n\n', parse_mode='MarkdownV2',disable_web_page_preview=True,
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
# ---------------------------> feedback button < ---------------------------
    def feedback_btn(update : Update, context : CallbackContext):
        chat_id = update.message.chat_id
        context.bot.send_chat_action(chat_id,ChatAction.TYPING)
        update.message.reply_text(text=messages["feedback_msg"])
        update.message.forward(chat_id=5117722111)
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
# --------------------------- > list of moneys button < ---------------------------
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
# --------------------------- > list of companies button < ---------------------------
    def list_company(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        buttons = [
            [
                InlineKeyboardButton(text="more",url="https://www.nasdaq.com/market-activity/stocks/screener")
            ]
        ]
        context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        update.message.reply_text(
            text=messages["list_company_msg"],
            reply_markup=InlineKeyboardMarkup(buttons)
        )
# ---------------------------> more button < ---------------------------
    def more(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        buttons = [
            [messages["src_btn"]],
            [messages["support_btn"], messages["feedback_btn"]],
            [messages["back_btn"]]
        ]
        context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        update.message.reply_text(
            text=messages["more_msg"],
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        )
# ---------------------------> back1 < ---------------------------
    def back1(update: Update, context: CallbackContext):
        menu(update, context)
# ---------------------------> handler of bot < ---------------------------
except error.RetryAfter:
    chat_id = Update.message.chat_id
    Update.message.reply_text(chat_id,text="There is a lot of traffic, please Try again in minutes...")
    Update.message.reply_text(chat_id,text="Thanks for your patience\U0001F64F")
except error.NetworkError:
    chat_id = Update.message.chat_id
    Update.message.reply_text(chat_id,text="The network has a problem, please Try again in minutes...")
    Update.message.reply_text(chat_id,text="Thanks for your patience\U0001F64F")
# ---------------------------> run < ---------------------------
if __name__ == "__main__":
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("getchart",chart))
    updater.dispatcher.add_handler(CommandHandler("getprice", price))
    updater.dispatcher.add_handler(CommandHandler("gettime",time))
    updater.dispatcher.add_handler(CommandHandler("help", h))
    updater.dispatcher.add_handler(CommandHandler("about", about))
    updater.dispatcher.add_handler(CommandHandler("src", src))
    updater.dispatcher.add_handler(CommandHandler("cryptocurrencies", cryptocurrencies))
    updater.dispatcher.add_handler(CommandHandler("moneys", moneys))
    updater.dispatcher.add_handler(CommandHandler("companies",companies))
    updater.dispatcher.add_handler(CommandHandler("feedback",feedback))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["menu_msg"]), menu))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["more_btn"]), more))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["feedback_btn"]), feedback_btn))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["support_btn"]), support))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["src_btn"]), source_code))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_crypto"]), list_crypto))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_money"]), list_money))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["list_company"]), list_company))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["back_btn"]), back1))
    updater.start_polling()
    updater.idle()

