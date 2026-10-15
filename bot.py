import os
import asyncio
import random
from datetime import datetime
from flask import Flask
from threading import Thread
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID") # Your Telegram numeric ID
CHANNEL_ID = os.getenv("CHANNEL_ID") # Optional: -100xxxxxxxxxx

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Keep Render Alive (Web Server) ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Tradegenuis Bot is LIVE!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- TRADING LOGIC (Replace with your real analysis) ---
SYMBOLS = ["EURUSD", "XAUUSD", "GBPUSD", "BTCUSD"]

def get_trading_signal(symbol="EURUSD"):
    """Your real strategy here. This is sample that generates signal"""
    side = random.choice(["BUY", "SELL"])
    entry = round(random.uniform(1.0800, 1.0900), 5) if "USD" in symbol else round(random.uniform(2600, 2700), 2)
    sl = round(entry - 0.0020, 5) if side == "BUY" else round(entry + 0.0020, 5)
    tp = round(entry + 0.0040, 5) if side == "BUY" else round(entry - 0.0040, 5)

    confidence = random.randint(75, 95)

    formatted = f"""
📊 **{symbol} SIGNAL** - {datetime.now().strftime('%H:%M GMT')}

{'🟢' if side=='BUY' else '🔴'} **{side} {symbol}**
Entry: `{entry}`
SL: `{sl}`
TP: `{tp}`

Confidence: {confidence}%
⚠️ Risk: Use 2-3% of capital
🔔 Follow SL strictly

🤖 @TradegenuisBot
"""
    return formatted, side

# --- COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 View Chart", url="https://www.tradingview.com/")],
        [InlineKeyboardButton("💬 Join Channel", url="https://t.me/tradegenuis")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"""
👋 Welcome to **TradeGenius Auto Bot**

✅ Auto Trading: **ENABLED** (Every 15 min)
Bot will send signals automatically.

Commands:
/start - Enable auto trading
/stop - Stop auto trading
/analyze - Manual analysis now
/signal - Get signal now

Your bot is LIVE on Render ✅
"""
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Remove auto jobs
    for job in context.job_queue.jobs():
        if job.name == "auto_scan":
            job.schedule_removal()
    await update.message.reply_text("🛑 Auto trading STOPPED. Use /start to enable again.")

async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = "EURUSD"
    if context.args:
        symbol = context.args[0].upper()

    formatted, side = get_trading_signal(symbol)

    keyboard = [
        [InlineKeyboardButton("📈 View Chart", url=f"https://www.tradingview.com/symbols/{symbol}/")],
        [InlineKeyboardButton("💬 Join Channel", url="https://t.me/tradegenuis")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send to current chat
    await update.message.reply_text(formatted, reply_markup=reply_markup, parse_mode='Markdown')

    # Send to channel if set
    if CHANNEL_ID:
        try:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=formatted, parse_mode='Markdown')
            await update.message.reply_text(f"✅ Posted to channel")
        except Exception as e:
            await update.message.reply_text(f"Posting error: {e}")

# --- AUTO JOB (This makes it fully automatic) ---
async def auto_scan(context: ContextTypes.DEFAULT_TYPE):
    logger.info("Auto scan running...")
    for symbol in SYMBOLS:
        try:
            formatted, side = get_trading_signal(symbol)
            # Send to ADMIN
            if ADMIN_ID:
                await context.bot.send_message(chat_id=ADMIN_ID, text=formatted, parse_mode='Markdown')
            # Send to CHANNEL
            if CHANNEL_ID:
                await context.bot.send_message(chat_id=CHANNEL_ID, text=formatted, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Auto scan error for {symbol}: {e}")
        await asyncio.sleep(2) # small delay between symbols

def main():
    print("Starting Tradegenuis Signal Bot...")
    keep_alive() # Start fake web server for Render

    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN not set in Render Environment!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("signal", signal_command))
    application.add_handler(CommandHandler("analyze", signal_command))
    application.add_handler(CommandHandler("buy", signal_command))
    application.add_handler(CommandHandler("sell", signal_command))

    # AUTO TRADE every 15 minutes = 900 seconds
    # First run after 10 seconds of start
    application.job_queue.run_repeating(auto_scan, interval=900, first=10, name="auto_scan")

    print("Polling... Auto trading ENABLED")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
