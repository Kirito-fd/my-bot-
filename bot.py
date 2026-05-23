import asyncio
import os
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai
from aiohttp import web

# Твои данные (просто вставь их в кавычки)
TELEGRAM_TOKEN = '8475528128:AAFGr3AHZvXVRBdcr3LK6hihwlZ7XfvVGnc'
GOOGLE_API_KEY = 'AIzaSyA_Cpjxz6AiVi4fSc05vwDbQ3DhG-cwSs'

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def health_check(request):
    return web.Response(text="Bot is running")

async def main():
    # Создаем веб-сервер для Render
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Порт для Render
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())