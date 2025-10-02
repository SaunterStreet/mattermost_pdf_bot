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
    statement_date = lines[4].strip() 
    account_number = ''.join([str(randint(0, 9)) for _ in range(11)])
    date_5_1 = lines[5].strip()
    date_5_2 = lines[6].strip()
    date_format1 = lines[7].strip()
    date_format2 = lines[8].strip()
    value_6 = lines[9].strip()
    value_7 = lines[10].strip()
    value_8 = lines[11].strip()
    value_9 = lines[12].strip()
    next_month_format = lines[13].strip()
    current_year = lines[14].strip()
    period_text = lines[15].strip()
    value_13 = lines[16].strip()
    value_14 = lines[17].strip()
    value_15 = lines[18].strip()
    value_16 = lines[19].strip()
    current_month_this_year = lines[20].strip()
    current_month_last_year = lines[21].strip()
    random_val1 = lines[22].strip()
    random_val2 = lines[23].strip()
    meter = ''.join([str(randint(0, 9)) for _ in range(9)])
    
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
        {
            'text': meter,
            'x': 440.6,
            'y': 334.3,
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
        "*Имя*, например: KHAED WADGE\n"
        "*Адрес, 1 строка*, например: 2708123 Israel\n"
        "*Адрес, 2 строка*, например: Hod Hasharon\n"
        "*Адрес, 3 строка*, например: 5 Eln Hal\n"
        "*Statement date*, например: Sep 22 2025\n"
        "*Previouse balance date*, например: Aug 4\n"
        "*Payment*, например: Aug 5\n"
        "*Actual reading, 1 строка*, например: Sep 22, 2025\n"
        "*Actual reading, 2 строка*, например: Aug 22, 2025\n"
        "*1 блок данных с числами справа.*. Например: 182.55\n"
        "*2 блок данных. Supplier.*, например: 131.76\n"
        "*2 блок данных. Delivery.*, например: 79.63\n"
        "*2 и 3 блок данных. Total.*, например: 125.39 или 116.39\n"
        "*3 блок. The total ... by*, например Oct 22\n"
        "*3 блок. Год на след строке, например 2025\n"
        "*3 блок. Billing period*. Например: Aug 22- Sep 22 (30 days)\n"
        "*3 блок снизу справа. 1 значение*, например: 23412\n"
        "*3 блок снизу справа. 2 значение*, например: 12341\n"
        "*4 блок сверху справа. Actual usage*, например: 1321\n"
        "*5 блок. Total*, например: 189.76\n"
        "*Блок слева. 1 строка*, например: Aug 2025 (37F)\n"
        "*Блок слева. 2 строка*, например: Aug 2024 (37F)\n"
        "*Киловаты. 1 строка*, например: 33\n"
        "*Киловаты. 2 строка*, например: 33"
    )


@dp.message(F.text)
async def process_text(message: Message):
    text = message.text
    lines = text.strip().split('\n')

    if len(lines) < 20:
        await message.answer("Недостаточно данных! Нужно минимум 20 строки.")
        return

    logging.info(f"Processing data.")
    
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