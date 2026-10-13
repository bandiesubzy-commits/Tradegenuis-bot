import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Tradegenius AI 🤖\n\nYour smart Forex assistant:\n/trend - Check market trend\n/buy - Buy signal\n/sell - Sell signal\n/start - Menu\n/stop - Stop\n\nTrade smart!")

async def trend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Market Trend: BULLISH")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 BUY Signal: Wait for confirmation")

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔴 SELL Signal: Wait for confirmation")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏹️ Trading stopped")

token = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trend", trend))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(CommandHandler("sell", sell))
app.add_handler(CommandHandler("stop", stop))
app.run_polling()
