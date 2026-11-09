import asyncio
import logging
import re
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# ⚠️ ВСТАВЬТЕ СЮДА ВАШ ТОКЕН ИЗ BOTFATHER (Кавычки не удалять!)
TOKEN = "8957653429:AAFNhZXXoeGd_7g_EVaBRQPoa4g6n5AUmKo"

# ID вашего закрытого приватного канала (куда проверяется доступ)
CHANNEL_ID = -1004288240193

# 🔗 ВСТАВЬТЕ СЮДА ВАШУ ССЫЛКУ НА GOOGLE ДИСК
GOOGLE_DRIVE_URL = "https://google.com"


# Функция для автоматического создания прямой ссылки из обычной ссылки Google Drive
def get_direct_google_drive_link(url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9_-]{33,})", url)
    if match:
        file_id = match.group(1)
        return f"https://google.com{file_id}"
    return url


# Генерируем прямую ссылку для видео-плеера
VIDEO_SOURCE = get_direct_google_drive_link(GOOGLE_DRIVE_URL)

dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    print(f"Получена команда /start от пользователя {message.from_user.id}. Генерирую тестовую ссылку...")
    
    try:
        # Пробуем сгенерировать одноразовую пригласительную ссылку в канал
        invite_link = await bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)
        
        # Если ссылка создалась успешно, выводим её в виде кнопки под видео
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 ТЕСТ: Вступить в канал", url=invite_link.invite_link)]
        ])
        
        welcome_text = (
            "🧪 <b>ТЕСТОВЫЙ ЗАПУСК: Проверка функционала ссылки</b>\n\n"
            "Оплата отключена для проверки. Бот успешно связался с каналом и сгенерировал ссылку!\n\n"
            "Нажмите на большую кнопку <b>«🚀 ТЕСТ: Вступить в канал»</b> ниже, чтобы проверить вход."
        )
        
        # Отправляем промо-видео вместе с кнопкой входа
        await bot.send_video(
            chat_id=message.chat.id,
            video=VIDEO_SOURCE,
            caption=welcome_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        print("✅ Тестовое видео и ссылка успешно отправлены в чат!")
        
    except Exception as e:
        logging.error(f"Ошибка при генерации тестовой ссылки: {e}")
        # Если бот не админ или ID канала неверный, он пришлет текст с точной ошибкой
        error_text = (
            "❌ <b>Ошибка проверки ссылки!</b>\n\n"
            f"Боту не удалось сгенерировать ссылку. Код ошибки:\n<code>{e}</code>\n\n"
            "<b>Что проверить:</b>\n"
            "1. Добавлен ли бот в ваш закрытый канал?\n"
            "2. Выданы ли боту права Администратора на создание пригласительных ссылок?\n"
            f"3. Правильно ли указан ID канала: <code>{CHANNEL_ID}</code>?"
        )
        await message.answer(
            text=error_text,
            parse_mode="HTML"
        )

async def main():
    bot = Bot(token=TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    print("="*50)
    print("🤖 ТЕСТОВЫЙ БОТ ЗАПУЩЕН НА ХОСТИНГЕ!")
    print("Откройте Telegram и напишите боту /start для проверки ссылки.")
    print("="*50)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nБот остановлен.")
    except Exception as fatal_error:
        print("\n❌ КРИТИЧЕСКАЙ ОШИБКА ПРИ ЗАПУСКЕ:")
        import traceback
        traceback.print_exc()
        input("\nНажмите ENTER...")
