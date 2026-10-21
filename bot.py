import os
import telebot
import google.generativeai as genai

# Maxfiy kalitlarni xavfsiz muhitdan o'qib olamiz
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Gemini AI sozlamasi
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-3.8-flash',
    system_instruction="Sen 'Ustaz.AI' desiz. Ataniyaz tárepinen jaratılǵansansiz. Hármáw waqitta ózbek hám qaraqalpaq tillerinde juwap beriń."
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salám! Men Ustaz.AI man. Sizge qanday járdem bere alaman?")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Xatolik: {e}")
        bot.reply_to(message, "Keshirersiz, sorawdı qayta islew waqtında qátelik júzege keldi.")

print("Bot serverda ishlashga tayyorlanyapti...")
bot.infinity_polling(skip_pending=True)