from io import BytesIO
from random import randint

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PyPDF2 import PdfReader, PdfWriter

pdfmetrics.registerFont(TTFont('calibri', 'fonts/Calibri/calibri.ttf'))
pdfmetrics.registerFont(TTFont('calibri_bold', 'fonts/Calibri/calibri_bold.ttf'))
pdfmetrics.registerFont(TTFont('open', 'fonts/opensans/OpenSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('open_bold', 'fonts/opensans/OpenSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('open_semi', 'fonts/opensans/OpenSans-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('utsaahb', 'fonts/utsaah/utsaahb.ttf'))
pdfmetrics.registerFont(TTFont('utsaah', 'fonts/utsaah/utsaah.ttf'))
pdfmetrics.registerFont(TTFont('tahoma', 'fonts/Tahoma/tahoma.ttf'))
pdfmetrics.registerFont(TTFont('arial', 'fonts/Arial/ARIAL.TTF'))
pdfmetrics.registerFont(TTFont('arialb', 'fonts/Arial/ARIALBD.TTF'))
pdfmetrics.registerFont(TTFont('verdana', 'fonts/Verdana/Verdana.ttf'))

class PDFEditor:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.reader = PdfReader(template_path)
        
    def add_text(self, output_path: str, text_data: list):
        page = self.reader.pages[0]
        packet = BytesIO()
        mediabox = page.mediabox
        page_width = float(mediabox.width) + 5
        page_height = float(mediabox.height) + 5

        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        for item in text_data:
            text = item['text']
            x = item['x']
            y = item['y']
            font = item.get('font', 'Helvetica')
            size = item.get('size', 12)
            align = item.get('align', 'left')
            color = item.get('color', '#000000')
            
            can.setFont(font, size)

            if color.startswith('#'):
            # Убираем # и конвертируем в RGB (0-1)
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16) / 255
                g = int(hex_color[2:4], 16) / 255
                b = int(hex_color[4:6], 16) / 255
                can.setFillColorRGB(r, g, b)
            else:
                # Поддержка именованных цветов
                if color == 'red':
                    can.setFillColorRGB(1, 0, 0)
                elif color == 'blue':
                    can.setFillColorRGB(0, 0, 1)
                elif color == 'green':
                    can.setFillColorRGB(0, 1, 0)
                else:
                    can.setFillColorRGB(0, 0, 0)
            
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

        for i in range(len(self.reader.pages)):
            if i == 0:
                writer.add_page(page)  # Первая страница с текстом
            else:
                writer.add_page(self.reader.pages[i])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


class text_generator:
    def __init__(self, user_input: str):
        self.user_input = user_input

    def generate_text_data_ir(user_input) -> list:
        lines = user_input.strip().split('\n')
        
        name = lines[0].strip()
        address_line1 = lines[1].strip()
        address_line2 = lines[2].strip()
        address_line3 = lines[3].strip()
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
        current_month_this_year = lines[19].strip()
        current_month_last_year = lines[20].strip()
        random_val1 = lines[21].strip()
        random_val2 = lines[22].strip()
        meter = ''.join([str(randint(0, 9)) for _ in range(9)])
        random_val3 = lines[23].strip()
        value_16 = float(random_val3) * 0.103000
        formatted_value_16 = f'{value_16:.2f}'
        
        text_data = [
            {'text': name, 'x': 560, 'y': 730, 'font': 'calibri_bold', 'size': 14, 'align': 'right'},
            {'text': address_line1, 'x': 560, 'y': 717, 'font': 'calibri', 'size': 11, 'align': 'right'},
            {'text': address_line2, 'x': 560, 'y': 704, 'font': 'calibri', 'size': 11, 'align': 'right'},
            {'text': address_line3, 'x': 560, 'y': 691, 'font': 'calibri', 'size': 11, 'align': 'right'},
            {'text': f'Statement date {statement_date}', 'x': 560, 'y': 678, 'font': 'calibri', 'size': 11, 'align': 'right'},
            {'text': date_format1, 'x': 382, 'y': 293.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': date_format2, 'x': 382, 'y': 279.8, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': f'Account number: {account_number}', 'x': 560, 'y': 665, 'font': 'calibri', 'size': 11, 'align': 'right'},
            {'text': date_5_1, 'x': 393.5, 'y': 612.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': date_5_2, 'x': 343.5, 'y': 585.9, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(value_6), 'x': 593, 'y': 612.5, 'font': 'calibri', 'size': 11, 'align': 'right'},
            {'text': str(value_6), 'x': 593, 'y': 585.5, 'font': 'calibri', 'size': 11, 'align': 'right'},
            {'text': str(value_7), 'x': 562.3, 'y': 516.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(value_8), 'x': 563.1, 'y': 502.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(value_9), 'x': 562, 'y': 488.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(value_9), 'x': 562, 'y': 466.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': next_month_format, 'x': 514, 'y': 453.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': current_year, 'x': 300.3, 'y': 440.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': address_line1, 'x': 300.3, 'y': 400.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': address_line2, 'x': 300.3, 'y': 387.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': address_line3, 'x': 300.3, 'y': 374.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': period_text, 'x': 380, 'y': 320.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(value_13), 'x': 556, 'y': 292.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(value_14), 'x': 558, 'y': 279.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(value_15), 'x': 562, 'y': 257.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(formatted_value_16), 'x': 562.5, 'y': 216.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(formatted_value_16), 'x': 562.5, 'y': 193, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': current_month_this_year, 'x': 100, 'y': 381, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': current_month_last_year, 'x': 100, 'y': 367.3, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(random_val1), 'x': 212, 'y': 381, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': str(random_val2), 'x': 212, 'y': 367.3, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': meter, 'x': 440.6, 'y': 334.3, 'font': 'calibri', 'size': 11, 'align': 'left'},
            {'text': random_val3, 'x': 414, 'y': 216.5, 'font': 'calibri', 'size': 11, 'align': 'left'},
        ]
        
        return text_data

    def generate_text_data_uk(user_input: str) -> list:
        lines = user_input.strip().split('\n')
        
        name = lines[0].strip()
        address_line1 = lines[1].strip()
        address_line2 = lines[2].strip()
        address_line3 = lines[3].strip()
        statement_date = lines[4].strip() 
        statement_period = lines[5].strip()
        cust_number = lines[6].strip()
        balance = lines[7].strip()
        value1 = lines[8].strip()
        value_2 = lines[9].strip()
        value_3 = lines[10].strip()
        value_4 = lines[11].strip()
        start_str, end_str = [s.strip() for s in statement_period.split('-')]
        
        text_data = [
            {'text': name, 'x': 219, 'y': 3008, 'font': 'open_bold', 'size': 41, 'align': 'left'},
            {'text': address_line1, 'x': 219, 'y': 2962, 'font': 'open', 'size': 41, 'align': 'left'},
            {'text': address_line2, 'x': 219, 'y': 2915, 'font': 'open', 'size': 41, 'align': 'left'},
            {'text': address_line3, 'x': 219, 'y': 2865, 'font': 'open', 'size': 41, 'align': 'left'},
            {'text': statement_date, 'x': 226, 'y': 2093, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': statement_period, 'x': 664, 'y': 2093, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': cust_number, 'x': 1282, 'y': 2351, 'font': 'open_semi', 'size': 50, 'align': 'left'},
            {'text': balance, 'x': 734, 'y': 1708, 'font': 'utsaahb', 'size': 140, 'align': 'left'},
            {'text': f"The amount of £{value1} will be taken from your", 'x': 1382, 'y': 1785, 'font': 'utsaah', 'size': 60, 'align': 'left'},
            {'text': "bank account on or within 3 days of", 'x': 1382, 'y': 1738, 'font': 'utsaah', 'size': 60, 'align': 'left'},
            {'text': statement_date, 'x': 2064, 'y': 1738, 'font': 'utsaahb', 'size': 60, 'align': 'left'},
            {'text': "Your 12 month Personal Projection for your current", 'x': 1382, 'y': 1308, 'font': 'utsaah', 'size': 55, 'align': 'left'},
            {'text': "tariff is", 'x': 1382, 'y': 1256, 'font': 'utsaah', 'size': 55, 'align': 'left'},
            {'text': value_2, 'x': 1511, 'y': 1256, 'font': 'utsaahb', 'size': 55, 'align': 'left'},
            {'text': "Your balance was in debit by", 'x': 212, 'y': 1262, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': "Total charges", 'x': 212, 'y': 1204, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': "(including VAT)", 'x': 482, 'y': 1206, 'font': 'open_semi', 'size': 30, 'align': 'left'},
            {'text': "What you've paid", 'x': 212, 'y': 1149, 'font': 'open_semi', 'size': 41, 'align': 'left'},
            {'text': f"Direct Debit {start_str}", 'x': 212, 'y': 1098, 'font': 'open', 'size': 37, 'align': 'left'},
            {'text': f"Direct Debit {end_str}", 'x': 212, 'y': 1048, 'font': 'open', 'size': 37, 'align': 'left'},
            {'text': balance, 'x': 1192, 'y': 1263, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
            {'text': f"£{value1}", 'x': 1192, 'y': 1206, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
            {'text': value_3, 'x': 1192, 'y': 1151, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
            {'text': "-£10.00", 'x': 1192, 'y': 1098, 'font': 'utsaah', 'size': 55, 'align': 'right'},
            {'text': "-£10.00", 'x': 1192, 'y': 1048, 'font': 'utsaah', 'size': 55, 'align': 'right'},
            {'text': value_4, 'x': 1192, 'y': 957, 'font': 'utsaahb', 'size': 55, 'align': 'right'},
        ]
        
        return text_data
    
    def generate_text_data_ie(user_input: str) -> list:
        lines = user_input.strip().split('\n')
        
        name = lines[0].strip()
        address_line1 = lines[1].strip()
        address_line2 = lines[2].strip()
        address_line3 = lines[3].strip()
        address_line4 = lines[4].strip() 
        date_under_address = lines[5].strip() 
        gas = lines[6].strip()
        supply_address = lines[7].strip()
        blue_kw = lines[8].strip()
        lblue_kw = lines[9].strip()
        aqua_kw = lines[10].strip()
        acc_num = lines[11].strip()
        end_date = lines[12].strip()
        total = lines[13].strip()
        due_on = lines[14].strip()
        gas_1 = lines[15].strip()
        gas_2 = lines[16].strip()
        value1 = lines[17].strip()
        value2 = lines[18].strip()
        value3 = lines[19].strip()
        value4 = lines[20].strip()
        value5 = lines[21].strip()
        value6 = lines[22].strip()
        
        text_data = [
            {'text': name, 'x': 36, 'y': 690, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line1, 'x': 36, 'y': 680, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line2, 'x': 36, 'y': 670, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line3, 'x': 36, 'y': 660, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': address_line4, 'x': 36, 'y': 650, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': date_under_address, 'x': 36, 'y': 630, 'font': 'arialb', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': gas, 'x': 36, 'y': 577, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': gas, 'x': 36, 'y': 408, 'font': 'tahoma', 'size': 9, 'align': 'left', 'color': '#1b2950'},
            {'text': supply_address, 'x': 102, 'y': 547.5, 'font': 'arialb', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': blue_kw, 'x': 269, 'y': 510, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': lblue_kw, 'x': 269, 'y': 487, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': aqua_kw, 'x': 269, 'y': 464, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': acc_num, 'x': 463, 'y': 705.5, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': end_date, 'x': 454.5, 'y': 682, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 376, 'y': 572, 'font': 'verdana', 'size': 13.5, 'align': 'left', 'color': '#ffffff'},
            {'text': total, 'x': 384.5, 'y': 571.5, 'font': 'arialb', 'size': 18, 'align': 'left', 'color': '#ffffff'},
            {'text': due_on, 'x': 370, 'y': 542, 'font': 'arialb', 'size': 11.1, 'align': 'left', 'color': '#ffffff'},
            {'text': gas_1, 'x': 128, 'y': 303, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': gas_2, 'x': 50, 'y': 293.4, 'font': 'tahoma', 'size': 8.1, 'align': 'left', 'color': '#1b2950'},
            {'text': value1, 'x': 267.8, 'y': 346, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value2, 'x': 267.8, 'y': 329, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value3, 'x': 267.8, 'y': 315.5, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value4, 'x': 267.8, 'y': 299, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value4, 'x': 267.8, 'y': 280.3, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value5, 'x': 267.8, 'y': 264.8, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': total, 'x': 267.8, 'y': 251, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value6, 'x': 267.8, 'y': 236, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': value6, 'x': 267.8, 'y': 220, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': total, 'x': 267.8, 'y': 202.5, 'font': 'arialb', 'size': 9, 'align': 'right', 'color': '#1b2950'},
            {'text': '€', 'x': 243.5, 'y': 346, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 243.5, 'y': 329, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 315.5, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 299, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 280.3, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 248, 'y': 264.8, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 243.5, 'y': 251, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 239.5, 'y': 236, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 239.5, 'y': 220, 'font': 'verdana', 'size': 6, 'align': 'left', 'color': '#1b2950'},
            {'text': '€', 'x': 241, 'y': 202.8, 'font': 'verdana', 'size': 6.9, 'align': 'left', 'color': '#1b2950'},
            {'text': '-', 'x': 246.7, 'y': 299, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': '-', 'x': 246.7, 'y': 280.3, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
            {'text': '-', 'x': 238.7, 'y': 220, 'font': 'tahoma', 'size': 8.1, 'align': 'right', 'color': '#1b2950'},
        ]
        
        return text_data