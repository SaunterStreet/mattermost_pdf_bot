import asyncio
import logging
from os import getenv
from datetime import datetime, timedelta
from random import randint, uniform
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Регистрация шрифтов
pdfmetrics.registerFont(TTFont('calibri', 'Calibri/calibri.ttf'))
pdfmetrics.registerFont(TTFont('calibri_bold', 'Calibri/calibri_bold.ttf'))

load_dotenv()

dp = Dispatcher()
TOKEN = getenv("BOT_TOKEN")


class PDFEditor:
    def __init__(self, template_path: str):
        """
        Инициализация редактора PDF
        :param template_path: путь к шаблону PDF
        """
        self.template_path = template_path
        self.reader = PdfReader(template_path)
        
    def add_text(self, output_path: str, text_data: list):
        """
        Добавление текста в одностраничный PDF по координатам
        :param output_path: путь для сохранения результата
        :param text_data: список словарей с данными текста
        """
        page = self.reader.pages[0]
        
        packet = BytesIO()
        mediabox = page.mediabox
        page_width = float(mediabox.width)
        page_height = float(mediabox.height)

        page_width += 5
        page_height += 5

        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        for item in text_data:
            text = item['text']
            x = item['x']
            y = item['y']
            font = item.get('font', 'Helvetica')
            size = item.get('size', 12)
            align = item.get('align', 'left')
            
            can.setFont(font, size)
            
            if align == 'right':
                can.drawRightString(x, y, text)
            elif align == 'center':
                can.drawCentredString(x, y, text)
            else:
                can.drawString(x, y, text)
        
        can.save()
        packet.seek(0)
        
        overlay_pdf = PdfReader(packet)
        overlay_page = overlay_pdf.pages[0]
        
        page.merge_page(overlay_page)
        
        writer = PdfWriter()
        writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


def generate_text_data(user_input: str) -> list:
    """
    Генерирует text_data на основе пользовательского ввода
    """
    lines = user_input.strip().split('\n')
    
    # Парсинг пользовательского ввода
    name = lines[0].strip() if len(lines) > 0 else "JOHN CITIZEN"
    address_line1 = lines[1].strip() if len(lines) > 1 else "2708122 Israel"
    address_line2 = lines[2].strip() if len(lines) > 2 else "Kiryat-Bialik"
    address_line3 = lines[3].strip() if len(lines) > 3 else "Giera Street 12/35 ISRAEL"
    
    # Генерация дат
    today = datetime.now()
    statement_date = today.strftime("%b %d %Y")  # Oct 3 2025
    date_format1 = today.strftime("%b %d, %Y")  # Sep 22, 2025
    month_ago = today - timedelta(days=30)
    date_format2 = month_ago.strftime("%b %d, %Y")  # Aug 22, 2025
    
    # Дата через месяц от первого значения комментария 3
    next_month = today + timedelta(days=30)
    next_month_format = next_month.strftime("%b %d")  # Oct 22
    
    # Период 30 дней
    period_start = today.strftime("%b %d")
    period_end = next_month.strftime("%b %d")
    period_text = f"{period_start}-{period_end} (30 days)"
    
    # Текущий год
    current_year = today.strftime("%Y")
    
    # Текущий месяц этот год и прошлый год
    current_month_this_year = today.strftime("%b %Y")
    current_month_last_year = today.replace(year=today.year - 1).strftime("%b %Y")
    
    # Рандомные данные
    account_number = ''.join([str(randint(0, 9)) for _ in range(11)])
    
    # Даты для комментария 5
    random_month = randint(1, 12)
    random_day1 = randint(1, 28)
    random_day2 = random_day1 + 1
    date_5_1 = datetime(2024, random_month, random_day1).strftime("%b %d")
    date_5_2 = datetime(2024, random_month, random_day2).strftime("%b %d")
    
    # Рандомные числа
    value_6 = round(uniform(180, 185), 2)
    value_7 = round(uniform(130, 135), 2)
    value_8 = round(uniform(78, 82), 2)
    value_9 = round(uniform(115, 125), 2)
    value_13 = randint(88500, 89000)
    value_14 = randint(87000, 87300)
    value_15 = value_13 - value_14
    value_16 = round(uniform(187, 190), 2)
    random_val1 = randint(20, 40)
    random_val2 = randint(20, 40)
    
    text_data = [
        # 1. Имя пользователя
        {
            'text': name,
            'x': 560,
            'y': 730,
            'font': 'calibri_bold',
            'size': 14,
            'align': 'right'
        },
        # 2. Адрес (3 строки)
        {
            'text': address_line1,
            'x': 560,
            'y': 717,
            'font': 'calibri',
            'size': 11,
            'align': 'right'
        },
        {
            'text': address_line2,
            'x': 560,
            'y': 704,
            'font': 'calibri',
            'size': 11,
            'align': 'right'
        },
        {
            'text': address_line3,
            'x': 560,
            'y': 691,
            'font': 'calibri',
            'size': 11,
            'align': 'right'
        },
        # 3. Statement date
        {
            'text': f'Statement date {statement_date}',
            'x': 560,
            'y': 678,
            'font': 'calibri',
            'size': 11,
            'align': 'right'
        },
        # 3. (1 строка) - сегодняшняя дата
        {
            'text': date_format1,
            'x': 382,
            'y': 293.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 3. (2 строка) - месяц назад
        {
            'text': date_format2,
            'x': 382,
            'y': 279.8,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 4. Account number
        {
            'text': f'Account number: {account_number}',
            'x': 560,
            'y': 665,
            'font': 'calibri',
            'size': 11,
            'align': 'right'
        },
        # 5. Рандомные даты (2 строки)
        {
            'text': date_5_1,
            'x': 393.5,
            'y': 612.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        {
            'text': date_5_2,
            'x': 343.5,
            'y': 585.9,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 6. Одинаковые значения (2 строки)
        {
            'text': str(value_6),
            'x': 593,
            'y': 612.5,
            'font': 'calibri',
            'size': 11,
            'align': 'right'
        },
        {
            'text': str(value_6),
            'x': 599,
            'y': 585.5,
            'font': 'calibri',
            'size': 11,
            'align': 'right'
        },
        # 7. Рандомное значение
        {
            'text': str(value_7),
            'x': 562.3,
            'y': 516.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 8. Рандомное значение
        {
            'text': str(value_8),
            'x': 563.1,
            'y': 502.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 9. Одинаковые значения (2 строки)
        {
            'text': str(value_9),
            'x': 562,
            'y': 488.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        {
            'text': str(value_9),
            'x': 562,
            'y': 466.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 10. Дата через месяц
        {
            'text': next_month_format,
            'x': 514,
            'y': 453.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 10. Текущий год
        {
            'text': current_year,
            'x': 300.3,
            'y': 440.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # Повтор адреса (комментарий 2)
        {
            'text': address_line1,
            'x': 300.3,
            'y': 400.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        {
            'text': address_line2,
            'x': 300.3,
            'y': 387.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        {
            'text': address_line3,
            'x': 300.3,
            'y': 374.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 12. Период 30 дней
        {
            'text': period_text,
            'x': 380,
            'y': 320.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 13. Рандомное целое
        {
            'text': str(value_13),
            'x': 556,
            'y': 292.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 14. Рандомное целое
        {
            'text': str(value_14),
            'x': 558,
            'y': 279.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 15. Разность
        {
            'text': str(value_15),
            'x': 562,
            'y': 257.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # 16. Одинаковые значения (2 строки)
        {
            'text': str(value_16),
            'x': 562.5,
            'y': 216.5,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        {
            'text': str(value_16),
            'x': 562.5,
            'y': 193,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # Нынешний месяц этот год
        {
            'text': current_month_this_year,
            'x': 100,
            'y': 381,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # Нынешний месяц прошлый год
        {
            'text': current_month_last_year,
            'x': 100,
            'y': 367.3,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        # Рандомные значения
        {
            'text': str(random_val1),
            'x': 212,
            'y': 381,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
        {
            'text': str(random_val2),
            'x': 212,
            'y': 367.3,
            'font': 'calibri',
            'size': 11,
            'align': 'left'
        },
    ]
    
    return text_data


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    await message.answer(
        "Отправь данные в формате:\n\n"
        "JOHN WICK\n"
        "Maddison St\n"
        "Hod Hasharon\n"
        "5 Eln Hal"
    )


@dp.message(F.text)
async def process_text(message: Message):
    text = message.text
    lines = text.strip().split('\n')

    if len(lines) < 4:
        await message.answer("Недостаточно данных! Нужно минимум 4 строки.")
        return

    name = lines[0].strip()
    address1 = lines[1].strip()
    address2 = lines[2].strip()
    address3 = lines[3].strip()
    
    result_message = (
        "Данные получены!\n\n"
        f"Имя: {name}\n"
        f"Адрес 1: {address1}\n"
        f"Адрес 2: {address2}\n"
        f"Адрес 3: {address3}\n"
    )
    
    await message.answer(result_message)
    logging.info(f"Processing data for: {name}")
    
    await message.answer("Начинаю обработку PDF...")
    
    try:
        # Генерация text_data
        text_data = generate_text_data(text)
        
        # Создание PDF
        editor = PDFEditor("template.pdf")
        output_path = f"result_{message.from_user.id}.pdf"
        editor.add_text(output_path, text_data)
        
        # Отправка PDF
        pdf_file = FSInputFile(output_path)
        await message.answer_document(
            pdf_file,
            caption="Готово! Вот твой PDF файл."
        )

        import os
        os.remove(output_path)  # Удаляем файл после отправки
        logging.info(f"PDF successfully created: {output_path}")
        logging.info(f"PDF file deleted: {output_path}")
        
        
    except Exception as e:
        logging.error(f"Error creating PDF: {e}")
        await message.answer(f"❌ Ошибка при создании PDF: {str(e)}")


async def main() -> None:
    bot = Bot(token=TOKEN)
    logging.info("🤖 Bot started polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())