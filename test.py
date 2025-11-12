from pdf import *

user_message = """ILIA KOKOTOV
51 Einstein
Tel Aviv
6946032
2978 469810
086 53218197по
09 OCT 25
09 NOV 25
6434148
1291287
1872380
368.80
281.00
170.02
152.49
14.26
3.27
98.00
07-9682185
09847 00009026798 0488078 692042"""

text_data = text_generator.generate_text_data_ir(user_message)
print("Начинаю обработку PDF")
editor = PDFEditor("template_ir.pdf")
output_path = f"result_123.pdf"
editor.add_text(output_path, text_data)
print("PDF создан")