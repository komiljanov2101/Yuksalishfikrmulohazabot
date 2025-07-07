import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, ADMIN_IDS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class FeedbackStates(StatesGroup):
    waiting_for_contact = State()
    waiting_for_feedback = State()

@dp.message(F.text == "/start")
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Assalomu alaykum!\nFikr bildirishingiz uchun telefon raqamingizni yuboring:",
        reply_markup=kb
    )
    await state.set_state(FeedbackStates.waiting_for_contact)

@dp.message(FeedbackStates.waiting_for_contact)
async def get_contact(message: types.Message, state: FSMContext):
    if not message.contact:
        return await message.answer("Iltimos, pastdagi tugmadan foydalaning 📱")

    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Rahmat! Endi fikringizni yozib yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FeedbackStates.waiting_for_feedback)

@dp.message(FeedbackStates.waiting_for_feedback)
async def get_feedback(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    phone = user_data.get("phone")
    feedback = message.text

    for admin_id in ADMIN_IDS:
        await bot.send_message(
            admin_id,
            f"📥 <b>Yangi fikr</b>:\n\n"
            f"<b>📱 Telefon:</b> {phone}\n"
            f"<b>✍️ Fikr:</b> {feedback}",
            parse_mode="HTML"
        )

    await message.answer("Fikringiz uchun katta rahmat! ✅")
    await state.clear()

@dp.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("⛔ Siz admin emassiz.")
    
    await message.answer("👤 Admin panelga xush kelibsiz!\nSizga kelayotgan barcha fikrlar avtomatik yuboriladi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
