# Telegram PDF Bot

Бот для автоматической генерации PDF документов на основе пользовательского ввода.

## 📋 Требования

- Python 3.11+
- Docker и Docker Compose (для запуска в контейнере)
- Telegram Bot Token

## 🚀 Установка и запуск

### Вариант 1: Локальный запуск

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/SaunterStreet/telegram_pdf_bot.git
cd telegram_pdf_bot
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения:**
```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте токен вашего бота:
```env
BOT_TOKEN=your_actual_bot_token_here
```

5. **Запустите бота:**
```bash
python bot.py
```

---

### Вариант 2: Запуск через Docker 🐳

#### Способ А: Docker Compose (Рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/SaunterStreet/telegram_pdf_bot.git
cd telegram_pdf_bot
```

2. **Создайте файл `.env`:**
```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте токен:
```env
BOT_TOKEN=your_actual_bot_token_here
```

3. **Запустите контейнер:**
```bash
docker compose up -d
```

4. **Проверьте статус:**
```bash
docker compose ps
```

5. **Просмотр логов:**
```bash
docker compose logs -f
```

6. **Остановка бота:**
```bash
docker compose down
```

#### Способ Б: Чистый Docker

1. **Соберите образ:**
```bash
docker build -t telegram-pdf-bot .
```

2. **Запустите контейнер:**
```bash
docker run -d \
  --name telegram_pdf_bot \
  --restart unless-stopped \
  -e BOT_TOKEN=your_actual_bot_token_here \
  -v $(pwd)/template.pdf:/app/template.pdf \
  -v $(pwd)/Calibri:/app/Calibri \
  telegram-pdf-bot
```

3. **Просмотр логов:**
```bash
docker logs -f telegram_pdf_bot
```

4. **Остановка и удаление:**
```bash
docker stop telegram_pdf_bot
docker rm telegram_pdf_bot
```

---

## 📝 Использование

Отправьте боту текст в формате (4 строки):

```
JOHN WICK
Maddison St
Hod Hasharon
5 Eln Hal
```

Бот автоматически:
- Сгенерирует PDF с вашими данными
- Добавит случайные номера счетов, даты и значения
- Отправит готовый документ обратно

---

## 🛠 Полезные Docker команды

### Перезапуск бота
```bash
docker-compose restart
```

### Обновление после изменений в коде
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Просмотр использования ресурсов
```bash
docker stats telegram_pdf_bot
```

### Зайти внутрь контейнера
```bash
docker exec -it telegram_pdf_bot /bin/bash
```

---

## 📂 Структура проекта

```
telegram_pdf_bot/
│
├── bot.py                 # Основной файл бота
├── template.pdf           # Шаблон PDF документа
├── Calibri/               # Папка со шрифтами
│   ├── calibri.ttf
│   └── calibri_bold.ttf
├── .env                   # Переменные окружения (не в Git!)
├── .env.example           # Пример .env
├── requirements.txt       # Python зависимости
├── Dockerfile             # Docker конфигурация
├── docker-compose.yml     # Docker Compose конфигурация
├── .gitignore             # Игнорируемые файлы
└── README.md              # Этот файл
```

---

## ⚙️ Переменные окружения

| Переменная | Описание | Обязательная |
|-----------|----------|--------------|
| `BOT_TOKEN` | Токен Telegram бота от @BotFather | ✅ Да |

---

## 🐛 Решение проблем

### Ошибка: "Cannot find template.pdf"
Убедитесь, что файл `template.pdf` находится в корне проекта.

### Ошибка: "Cannot find font Calibri"
Убедитесь, что папка `Calibri/` содержит файлы `calibri.ttf` и `calibri_bold.ttf`.

### Docker: Бот не запускается
Проверьте логи:
```bash
docker-compose logs
```

### Docker: Изменения в коде не применяются
Пересоберите образ:
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📄 Лицензия

MIT License

---

## 👤 Автор

[@SaunterStreet](https://github.com/SaunterStreet)

---

## 🤝 Contribution

Pull requests приветствуются! Для больших изменений сначала откройте issue для обсуждения.
