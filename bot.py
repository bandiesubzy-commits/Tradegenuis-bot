import os
from threading import Thread
from flask import Flask

# --- Keep Alive Web Server for Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "Tradegenuis Signal Bot is LIVE!"
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
Thread(target=run_web, daemon=True).start()

# --- Telegram Signal Bot ---
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID") # Your Telegram ID
CHANNEL_ID = os.environ.get("CHANNEL_ID") # e.g. @tradegenuis_signals

if not BOT_TOKEN:
    print("BOT_TOKEN missing! Set in Render > Environment")
    import time
    while True: time.sleep(60)

logging.basicConfig(level=logging.INFO)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """🚀 **Welcome to Tradegenuis Signals!**

📈 Premium Crypto & Forex Signals

Commands:
/signal - Create new signal (Admin only)
/help - How to create signals
/price - Check price (coming soon)

Join our channel for signals!"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """📝 **How to Post a Signal:**

As Admin, type:

`/signal BTC/USDT LONG
Entry: 67000 - 67200
SL: 66500
TP1: 68000
TP2: 69000
TP3: 70500
Leverage: 10x`

Bot will auto-format it and post to channel!

Set ADMIN_ID in Render env to your Telegram ID.
Get your ID: @userinfobot on Telegram
"""
    await update.message.reply_text(text, parse_mode='Markdown')

# /signal handler
async def create_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # Check admin
    if ADMIN_ID and user_id!= ADMIN_ID:
        await update.message.reply_text("⛔ Only Admin can post signals.")
        return

    raw = update.message.text.replace("/signal", "").strip()
    if not raw:
        await update.message.reply_text("Send signal details after /signal command.\nUse /help for format.")
        return

    # Format signal beautifully
    lines = raw.split('\n')
    pair = lines[0].upper() if lines else "SIGNAL"

    formatted = f"""
🚀 **TRADEGENUIS SIGNAL** 🚀
━━━━━━━━━━━━━━━━━━
📊 **{pair}**

{raw}

━━━━━━━━━━━━━━━━━━
⚠️ Risk: Use 2-3% of capital
🔔 Follow SL strictly

🤖 @TradegenuisBot
"""

    keyboard = [
        [InlineKeyboardButton("📈 View Chart", url=f"https://www.tradingview.com/chart/?symbol=BINANCE:{pair.split('/')[0]}USDT")],
        [InlineKeyboardButton("💬 Join Channel", url="https://t.me/tradegenuis")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send to current chat
    await update.message.reply_text(formatted, parse_mode='Markdown', reply_markup=reply_markup)

    # Send to channel if set
    if CHANNEL_ID:
        try:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=formatted, parse_mode='Markdown', reply_markup=reply_markup)
            await update.message.reply_text(f"✅ Signal posted to {CHANNEL_ID}!")
        except Exception as e:
            await update.message.reply_text(f"Posted here, but failed to post to channel: {e}\nMake bot admin in channel!")

def main():
    print("Starting Tradegenuis Signal Bot...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("signal", create_signal))
    print("Polling...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
