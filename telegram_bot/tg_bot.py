import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from bot.orders import place_market_order, place_limit_order

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def buy(update, context):
    symbol = context.args[0]
    quantity = float(context.args[1])
    order = place_market_order(symbol, "BUY", quantity)
    update.message.reply_text(str(order))

def sell(update, context):
    symbol = context.args[0]
    quantity = float(context.args[1])
    order = place_market_order(symbol, "SELL", quantity)
    update.message.reply_text(str(order))

updater = Updater(TELEGRAM_TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("buy", buy))
dp.add_handler(CommandHandler("sell", sell))

updater.start_polling()
updater.idle()