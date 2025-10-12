# 🤖 Mattermost PDF Bot

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Умный бот для работы с PDF файлами в Mattermost*

[Возможности](#-возможности) • [Быстрый старт](#-быстрый-старт) • [Установка](#️-установка) • [Конфигурация](#️-конфигурация) • [Использование](#-использование)

</div>

---

## ✨ Возможности

- 📄 **Обработка PDF файлов** - автоматическая работа с документами
- 🔄 **Интеграция с Mattermost** - полная интеграция с вашим рабочим пространством
- 🐳 **Docker поддержка** - простое развертывание в один клик
- ⚡ **Быстрая настройка** - запуск за 5 минут
- 🔒 **Безопасность** - все данные остаются на вашем сервере

## 🚀 Быстрый старт

```bash
# Клонируем репозиторий
git clone https://github.com/your-username/mattermost_pdf_bot.git
cd mattermost_pdf_bot

# Настраиваем переменные окружения
cp .env.example .env
nano .env

# Запускаем через Docker
docker-compose up -d
```

**Готово!** 🎉 Бот уже работает.

## 🛠️ Установка

### Через Docker (рекомендуется)

#### Требования
- Docker 20.10+
- Docker Compose 2.0+

#### Шаги установки

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/your-username/mattermost_pdf_bot.git
   cd mattermost_pdf_bot
   ```

2. **Создайте файл конфигурации**
   ```bash
   cp .env.example .env
   ```

3. **Отредактируйте `.env` файл**
   ```bash
   nano .env
   ```
   
   Заполните необходимые переменные:
   ```env
   MATTERMOST_URL=https://your-mattermost.com
   MATTERMOST_TOKEN=your_bot_token_here
   BOT_USERNAME=pdf-bot
   ```

4. **Запустите бота**
   ```bash
   docker-compose up -d
   ```

5. **Проверьте статус**
   ```bash
   docker-compose logs -f
   ```

### Локальная установка

#### Требования
- Python 3.11+
- pip

#### Шаги установки

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/your-username/mattermost_pdf_bot.git
   cd mattermost_pdf_bot
   ```

2. **Создайте виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate  # Windows
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения**
   ```bash
   cp .env.example .env
   nano .env
   ```

5. **Запустите бота**
   ```bash
   python bot.py
   ```

## ⚙️ Конфигурация

### Обязательные переменные

| Переменная | Описание | Пример |
|-----------|----------|--------|
| `MATTERMOST_URL` | URL вашего Mattermost сервера | `https://chat.company.com` |
| `MATTERMOST_TOKEN` | Токен бота | `abc123xyz...` |
| `BOT_USERNAME` | Имя пользователя бота | `pdf-bot` |

### Опциональные переменные

| Переменная | Описание | По умолчанию |
|-----------|----------|--------------|
| `LOG_LEVEL` | Уровень логирования | `INFO` |
| `DATA_DIR` | Директория для данных | `./data` |

### Получение токена Mattermost

1. Войдите в Mattermost как администратор
2. Перейдите в **System Console** → **Integrations** → **Bot Accounts**
3. Нажмите **Add Bot Account**
4. Заполните информацию о боте
5. Скопируйте токен доступа

## 📖 Использование

### Команды Docker

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f

# Пересборка и запуск
docker-compose up -d --build

# Просмотр статуса
docker-compose ps
```

### Работа с ботом в Mattermost

1. Добавьте бота в нужный канал
2. Отправьте PDF файл в канал
3. Бот автоматически обработает файл
4. Получите результат

## 📁 Структура проекта

```
mattermost_pdf_bot/
├── bot.py                 # Основной файл бота
├── config.py              # Конфигурация
├── requirements.txt       # Python зависимости
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker Compose конфигурация
├── .env.example          # Пример переменных окружения
├── .gitignore           # Git ignore файл
├── README.md            # Документация
└── data/                # Директория для данных (не в git)
```

## 🔧 Разработка

### Локальная разработка

```bash
# Установка зависимостей для разработки
pip install -r requirements.txt

# Запуск в режиме разработки
python bot.py
```

### Запуск тестов

```bash
# Проверка переменных окружения
python check_env.py
```

## 🐛 Решение проблем

### Бот не подключается к Mattermost

- ✅ Проверьте правильность `MATTERMOST_URL`
- ✅ Убедитесь, что токен действителен
- ✅ Проверьте сетевое подключение

### Ошибки с переменными окружения

```bash
# Проверьте, что .env файл существует
ls -la .env

# Запустите проверку конфигурации
python check_env.py
```

### Docker контейнер не запускается

```bash
# Проверьте логи
docker-compose logs

# Пересоберите образ
docker-compose build --no-cache
docker-compose up -d
```

## 📝 Логи

Логи доступны через Docker:

```bash
# Все логи
docker-compose logs

# Последние 100 строк
docker-compose logs --tail=100

# Следить за логами в реальном времени
docker-compose logs -f
```

## 🤝 Участие в разработке

Приветствуются Pull Request'ы! Для крупных изменений сначала откройте Issue для обсуждения.

1. Форкните проект
2. Создайте ветку (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 💬 Поддержка

Если у вас возникли вопросы или проблемы:

- 🐛 [Создайте Issue](https://github.com/your-username/mattermost_pdf_bot/issues)
- 💡 [Обсуждения](https://github.com/your-username/mattermost_pdf_bot/discussions)

## ⭐ Благодарности

Сделано с ❤️ для сообщества Mattermost

---

<div align="center">

**[⬆ Вернуться к началу](#-mattermost-pdf-bot)**

</div>
