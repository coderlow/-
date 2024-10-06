import nest_asyncio
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta

# Применение nest_asyncio для поддержки многократного использования цикла событий
nest_asyncio.apply()

# Функция для запуска бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Математика", callback_data='math')],
        [InlineKeyboardButton("Конвертация", callback_data='conversion')],
        [InlineKeyboardButton("Индекс массы тела (ИМТ)", callback_data='bmi')],
        [InlineKeyboardButton("Расчет возраста", callback_data='age')],
        [InlineKeyboardButton("Вычисление процентов", callback_data='percent')],
        [InlineKeyboardButton("Календарные расчеты", callback_data='calendar')],
        [InlineKeyboardButton("НОК и НОД", callback_data='gcd_lcm')],
        [InlineKeyboardButton("Площадь и объем", callback_data='area_volume')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я калькулятор-бот. Выберите опцию:', reply_markup=reply_markup)

# Обработчик кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'math':
        await query.edit_message_text(text="Введите два числа через пробел:")
        context.user_data['mode'] = 'math'
    elif query.data == 'conversion':
        await query.edit_message_text(text="Введите величину и единицы измерения:")
        context.user_data['mode'] = 'conversion'
    elif query.data == 'bmi':
        await query.edit_message_text(text="Введите ваш вес (кг) и рост (м) через пробел:")
        context.user_data['mode'] = 'bmi'
    elif query.data == 'age':
        await query.edit_message_text(text="Введите вашу дату рождения (дд.мм.гггг):")
        context.user_data['mode'] = 'age'
    elif query.data == 'percent':
        await query.edit_message_text(text="Введите сумму и процент через пробел:")
        context.user_data['mode'] = 'percent'
    elif query.data == 'calendar':
        await query.edit_message_text(text="Введите дату и количество дней:")
        context.user_data['mode'] = 'calendar'
    elif query.data == 'gcd_lcm':
        await query.edit_message_text(text="Введите два числа для НОД и НОК через пробел:")
        context.user_data['mode'] = 'gcd_lcm'
    elif query.data == 'area_volume':
        await query.edit_message_text(text="Выберите:\n1. Площадь квадрата\n2. Объем куба\nВведите 1 или 2:")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mode = context.user_data.get('mode')

    if mode == 'math':
        numbers = list(map(float, update.message.text.split()))
        if len(numbers) == 2:
            result = numbers[0] + numbers[1]  # Здесь можно добавить другие операции
            await update.message.reply_text(f"Результат: {result}")
        else:
            await update.message.reply_text("Пожалуйста, введите два числа через пробел.")
    
    elif mode == 'conversion':
        # Логика конвертации (пример)
        await update.message.reply_text("Конвертация пока не реализована.")
    
    elif mode == 'bmi':
        weight, height = map(float, update.message.text.split())
        bmi = calculate_bmi(weight, height)
        await update.message.reply_text(f"Ваш ИМТ: {bmi:.2f}")
    
    elif mode == 'age':
        birth_date = update.message.text
        age = calculate_age(birth_date)
        await update.message.reply_text(f"Ваш возраст: {age} лет.")
    
    elif mode == 'percent':
        amount, percentage = map(float, update.message.text.split())
        result = calculate_percent(amount, percentage)
        await update.message.reply_text(f"{percentage}% от {amount} = {result:.2f}")
    
    elif mode == 'calendar':
        date_str, days = update.message.text.split()
        new_date = calculate_new_date(date_str, int(days))
        await update.message.reply_text(f"Новая дата: {new_date.strftime('%d.%m.%Y')}")
    
    elif mode == 'gcd_lcm':
        numbers = list(map(int, update.message.text.split()))
        if len(numbers) == 2:
            gcd = calculate_gcd(numbers[0], numbers[1])
            lcm = calculate_lcm(numbers[0], numbers[1])
            await update.message.reply_text(f"НОД: {gcd}, НОК: {lcm}")
        else:
            await update.message.reply_text("Пожалуйста, введите два целых числа через пробел.")
    
    elif mode == 'area_volume':
        choice = update.message.text
        if choice == '1':
            await update.message.reply_text("Введите длину стороны квадрата:")
            context.user_data['mode'] = 'area_square'
        elif choice == '2':
            await update.message.reply_text("Введите длину стороны куба:")
            context.user_data['mode'] = 'volume_cube'
    
    elif mode == 'area_square':
        side_length = float(update.message.text)
        area = side_length ** 2
        await update.message.reply_text(f"Площадь квадрата: {area:.2f}")
        context.user_data['mode'] = None
    
    elif mode == 'volume_cube':
        side_length = float(update.message.text)
        volume = side_length ** 3
        await update.message.reply_text(f"Объем куба: {volume:.2f}")
        context.user_data['mode'] = None

# Функции для вычислений
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def calculate_age(birth_date):
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, '%d.%m.%Y')
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def calculate_percent(amount, percentage):
    return amount * (percentage / 100)

def calculate_new_date(date_str, days):
    date = datetime.strptime(date_str, '%d.%m.%Y')
    return date + timedelta(days=days)

def calculate_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def calculate_lcm(a, b):
    return abs(a * b) // calculate_gcd(a, b)

# Основная функция
async def main():
    application = ApplicationBuilder().token("6969657638:AAED-wfkIIFjc3rA4svOGI-0k7Rs9LE4Dgk").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

