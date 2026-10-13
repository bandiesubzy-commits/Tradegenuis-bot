import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Tradegenius AI 🤖\n\n"
        "Your smart Forex assistant:\n"
        "/trend - Check market trend\n"
        "/buy - Buy signal analysis\n"
        "/sell - Sell signal analysis\n"
        "/start - Show this menu\n"
        "/stop - Stop trading\n\n"
        "Trade smart!"
    )

async def trend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Market Trend: BULLISH on EUR/USD")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 BUY Signal: EUR/USD Entry 1.0850 SL 1.0820 TP 1.0900")

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔴 SELL Signal: GBP/USD Entry 1.2650 SL 1.2680 TP 1.2600")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏹️ Trading stopped.")

token = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trend", trend))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(CommandHandler("sell", sell))
app.add_handler(CommandHandler("stop", stop))
app.run_polling()
