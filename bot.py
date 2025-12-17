import os
import telebot
from openai import OpenAI

# Ключи из Render (environment variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Клиент OpenAI для xAI Grok — ТОЛЬКО api_key и base_url, без лишнего!
client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Системный промпт — делает Grok экспертом по Югре
SYSTEM_PROMPT = """
Ты — Grok, ассистент платформы Югра Active. Эксперт по активному туризму в ХМАО-Югре.
Отвечай на русском, дружелюбно, с юмором в стиле Grok.
Давай советы по маршрутам (Приполярный Урал, озеро Нумто, сплавы по Казыму/Оби), безопасности, психологии в походах (стресс, выгорание, сплочение группы).
Рекомендуй маршруты из Югры, ссылки на сайт ugra-active.ru.
Если вопрос не по теме — перенаправь на сайт или скажи "Я специализируюсь на туризме Югры!".
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я — Grok-ассистент Югра Active 🏔️\n"
                          "Спрашивай про маршруты, походы, психологию в тайге или безопасность.\n"
                          "Что тебя интересует? 😊")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="grok-beta",  # Бесплатная модель
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            max_tokens=500,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ой, ошибка: {str(e)}. Попробуй позже! 😅")

print("Бот запущен!")
bot.polling(none_stop=True)
