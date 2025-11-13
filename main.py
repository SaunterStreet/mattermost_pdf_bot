import logging
import json
import os
import requests
import websocket
from pdf import *
from templates import *
from dotenv import load_dotenv

load_dotenv()

class WebSocketMattermostApp:
    mm_ws_headers = dict()
    connection = None
    bot_token = os.getenv('BOT_TOKEN')
    mm_url = os.getenv('MM_URL')
    bot_user_id = None
    user_modes = {}

    @staticmethod
    def get_bot_id():
        url = f"{WebSocketMattermostApp.mm_url}/api/v4/users/me"
        headers = {"Authorization": f"Bearer {WebSocketMattermostApp.bot_token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                WebSocketMattermostApp.bot_user_id = user_data['id']
                print(f"🤖 ID бота: {WebSocketMattermostApp.bot_user_id}")
        except Exception as e:
            print(f"❌ Ошибка получения ID: {e}")

    @staticmethod
    def send_message(channel_id, message_text):
        url = f"{WebSocketMattermostApp.mm_url}/api/v4/posts"
        headers = {
            "Authorization": f"Bearer {WebSocketMattermostApp.bot_token}",
            "Content-Type": "application/json"
        }
        data = {"channel_id": channel_id, "message": message_text}
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 201
        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")
            return False

    @staticmethod
    def send_pdf(channel_id, pdf_path):
        try:
            upload_url = f"{WebSocketMattermostApp.mm_url}/api/v4/files"
            headers = {"Authorization": f"Bearer {WebSocketMattermostApp.bot_token}"}
            with open(pdf_path, 'rb') as f:
                files = {'files': (os.path.basename(pdf_path), f)}
                data = {'channel_id': channel_id}
                response = requests.post(upload_url, headers=headers, files=files, data=data)
            if response.status_code != 201:
                print(f"❌ Ошибка загрузки: {response.status_code}")
                return False
            file_id = response.json()['file_infos'][0]['id']
            post_url = f"{WebSocketMattermostApp.mm_url}/api/v4/posts"
            headers["Content-Type"] = "application/json"
            post_data = {
                "channel_id": channel_id,
                "message": "✅ Готово! Вот твой PDF файл.",
                "file_ids": [file_id]
            }
            response = requests.post(post_url, headers=headers, json=post_data)
            return response.status_code == 201
        except Exception as e:
            print(f"❌ Ошибка отправки PDF: {e}")
            return False

    @staticmethod
    def process_pdf_ir(channel_id, user_id, user_message):
        lines = user_message.strip().split('\n')
        if len(lines) < 19:
            WebSocketMattermostApp.send_message(
                channel_id,
                f"❌ Недостаточно данных! Получено {len(lines)} строк, нужно 19."
            )
            return
        print(f"📨 Обработка данных от {user_id}")
        WebSocketMattermostApp.send_message(channel_id, "⏳ Начинаю обработку PDF...")
        try:
            text_data = text_generator.generate_text_data_ir(user_message)
            editor = PDFEditor("template_ir.pdf")
            output_path = f"result_{user_id}.pdf"
            editor.add_text(output_path, text_data)
            success = WebSocketMattermostApp.send_pdf(channel_id, output_path)
            os.remove(output_path)
            print(f"✅ PDF создан и отправлен: {output_path}")
            if not success:
                WebSocketMattermostApp.send_message(channel_id, "❌ Ошибка отправки PDF")
        except Exception as e:
            print(f"❌ Ошибка создания PDF: {e}")
            WebSocketMattermostApp.send_message(channel_id, f"❌ Ошибка: {str(e)}")

    @staticmethod
    def process_pdf_ie(channel_id, user_id, user_message):
        lines = user_message.strip().split('\n')
        if len(lines) < 23:
            WebSocketMattermostApp.send_message(
                channel_id,
                f"❌ Недостаточно данных! Получено {len(lines)} строк, нужно 23."
            )
            return
        print(f"📨 Обработка данных от {user_id}")
        WebSocketMattermostApp.send_message(channel_id, "⏳ Начинаю обработку PDF...")
        try:
            text_data = text_generator.generate_text_data_ie(user_message)
            editor = PDFEditor("template_ie.pdf")
            output_path = f"result_{user_id}.pdf"
            editor.add_text(output_path, text_data)
            success = WebSocketMattermostApp.send_pdf(channel_id, output_path)
            os.remove(output_path)
            print(f"✅ PDF создан и отправлен: {output_path}")
            if not success:
                WebSocketMattermostApp.send_message(channel_id, "❌ Ошибка отправки PDF")
        except Exception as e:
            print(f"❌ Ошибка создания PDF: {e}")
            WebSocketMattermostApp.send_message(channel_id, f"❌ Ошибка: {str(e)}")

    @staticmethod
    def process_pdf_uk(channel_id, user_id, user_message):
        lines = user_message.strip().split('\n')
        if len(lines) < 12:
            WebSocketMattermostApp.send_message(
                channel_id,
                f"❌ Недостаточно данных! Получено {len(lines)} строк, нужно 12."
            )
            return
        print(f"📨 Обработка данных от {user_id}")
        WebSocketMattermostApp.send_message(channel_id, "⏳ Начинаю обработку PDF...")
        try:
            text_data = text_generator.generate_text_data_uk(user_message)
            editor = PDFEditor("template_uk.pdf")
            output_path = f"result_{user_id}.pdf"
            editor.add_text(output_path, text_data)
            success = WebSocketMattermostApp.send_pdf(channel_id, output_path)
            os.remove(output_path)
            print(f"✅ PDF создан и отправлен: {output_path}")
            if not success:
                WebSocketMattermostApp.send_message(channel_id, "❌ Ошибка отправки PDF")
        except Exception as e:
            print(f"❌ Ошибка создания PDF: {e}")
            WebSocketMattermostApp.send_message(channel_id, f"❌ Ошибка: {str(e)}")

    @staticmethod
    def connect():
        WebSocketMattermostApp.get_bot_id()
        WebSocketMattermostApp.mm_ws_headers["Authorization"] = f"Bearer {WebSocketMattermostApp.bot_token}"
        WebSocketMattermostApp.connection = websocket.WebSocketApp(
            "wss://lizardteam.org/api/v4/websocket",
            header=WebSocketMattermostApp.mm_ws_headers,
            on_open=WebSocketMattermostApp.ws_on_open,
            on_message=WebSocketMattermostApp.ws_on_message,
            on_error=WebSocketMattermostApp.ws_on_error,
            on_close=WebSocketMattermostApp.ws_on_close
        )
        WebSocketMattermostApp.connection.run_forever(reconnect=5)

    @staticmethod
    def ws_on_message(ws, message):
        try:
            data = json.loads(message)
            event = data.get('event')
            if event == 'posted':
                post_data = json.loads(data['data']['post'])
                user_id = post_data.get('user_id')
                user_message = post_data.get('message', '').strip()
                channel_id = post_data.get('channel_id')
                if user_id == WebSocketMattermostApp.bot_user_id:
                    return
                if user_message.startswith('/'):
                    command = user_message.split()[0].lower()
                    if command == '/israel':
                        WebSocketMattermostApp.user_modes[user_id] = 'israel'
                        WebSocketMattermostApp.send_message(channel_id, "📝 Режим Israel активирован!\nТеперь отправь данные (19 строк):\nПример:\n" + ir_template)
                        return
                    elif command == '/ireland':
                        WebSocketMattermostApp.user_modes[user_id] = 'ireland'
                        WebSocketMattermostApp.send_message(channel_id, "📝 Режим Ireland активирован!\nТеперь отправь данные (23 строки):\nПример:\n" + ie_template)
                        return
                    elif command == '/uk':
                        WebSocketMattermostApp.user_modes[user_id] = 'uk'
                        WebSocketMattermostApp.send_message(channel_id, "📝 Режим UK активирован!\nТеперь отправь данные (12 строк):\nПример:\n" + gb_template)
                        return
                    elif command == '/info':
                        help_text = """
**Доступные команды:**

`/israel` - создание PDF для Израиля  
`/ireland` - создание PDF для Ирландии  
`/uk` - создание PDF для Великобритании  
`/return` - отменить текущий режим
                        """
                        WebSocketMattermostApp.send_message(channel_id, help_text)
                        return
                    elif command == '/return':
                        if user_id in WebSocketMattermostApp.user_modes:
                            del WebSocketMattermostApp.user_modes[user_id]
                            WebSocketMattermostApp.send_message(channel_id, "❌ Режим отменён")
                        else:
                            WebSocketMattermostApp.send_message(channel_id, "ℹ️ Нет активного режима")
                        return
                mode = WebSocketMattermostApp.user_modes.get(user_id)
                if mode == 'israel':
                    WebSocketMattermostApp.process_pdf_ir(channel_id, user_id, user_message)
                    del WebSocketMattermostApp.user_modes[user_id]
                elif mode == 'ireland':
                    WebSocketMattermostApp.process_pdf_ie(channel_id, user_id, user_message)
                    del WebSocketMattermostApp.user_modes[user_id]
                elif mode == 'uk':
                    WebSocketMattermostApp.process_pdf_uk(channel_id, user_id, user_message)
                    del WebSocketMattermostApp.user_modes[user_id]
                else:
                    WebSocketMattermostApp.send_message(channel_id, "ℹ️ Используй `/israel`, `/ireland` или `/uk` для создания PDF или `/info` для справки")
        except Exception as e:
            print(f"❌ Ошибка обработки: {e}")

    @staticmethod
    def ws_on_error(ws, error):
        logging.error(f"Error: {error}")

    @staticmethod
    def ws_on_close(ws, close_status_code, close_msg):
        logging.info(f"Connection closed {close_status_code} | {close_msg}")

    @staticmethod
    def ws_on_open(ws):
        logging.info("Connection opened")

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("🤖 Запуск PDF бота...")
    try:
        WebSocketMattermostApp.connect()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
