import os
from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Welcome to Tradegenius AI 🤖\n\n/trend - Check trend\n/buy - Buy signal\n/sell - Sell signal\n/start - Menu\n/stop - Stop")

def trend(update, context):
    update.message.reply_text("📈 Trend: BULLISH")

def buy(update, context):
    update.message.reply_text("🟢 BUY: Wait for confirmation")

def sell(update, context):
    update.message.reply_text("🔴 SELL: Wait for confirmation")

def stop(update, context):
    update.message.reply_text("⏹️ Stopped")

token = os.getenv("BOT_TOKEN")
updater = Updater(token, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("trend", trend))
dp.add_handler(CommandHandler("buy", buy))
dp.add_handler(CommandHandler("sell", sell))
dp.add_handler(CommandHandler("stop", stop))
updater.start_polling()
updater.idle()
