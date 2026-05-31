import pandas as pd
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# === загружаем датасет ===
df = pd.read_csv("incidents.csv")

# убираем пустые строки
df = df.dropna(subset=["text"])


# === кнопки ===
keyboard = [["Прислать инфо"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === старт ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Нажми кнопку, чтобы получить информацию о свалке",
        reply_markup=markup
    )


# === обработка кнопки ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📍 Прислать инфо":

        row = df.sample(1).iloc[0]

        response = (
            f"🚨 Инцидент\n\n"
            f"Станция: {row['station_name']}\n"
            f"Описание: {row['text']}\n"
        )

        if "source_url" in row and pd.notna(row["source_url"]):
            response += f"\n🔗 Источник: {row['source_url']}"

        await update.message.reply_text(response)

    else:
        await update.message.reply_text("Нажми кнопку 👇", reply_markup=markup)


# === запуск ===
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()