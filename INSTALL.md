# Быстрая установка Telegram-бота

## ⚡ Краткая инструкция

1. **Активировать виртуальное окружение:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Установить зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настроить токен бота:**
   - Отредактируйте файл `.env`
   - Замените `YOUR_BOT_TOKEN_HERE` на ваш реальный токен
   - Укажите ID пользователей в соответствующих ролях

4. **Проверить систему:**
   ```bash
   python check_system.py
   ```

5. **Запустить бота:**
   ```bash
   python bot.py
   ```

---

## 📋 Подробная инструкция
