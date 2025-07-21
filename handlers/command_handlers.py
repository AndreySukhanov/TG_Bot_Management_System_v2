"""
Обработчики специальных команд для каждой роли.
Обрабатывает команды из меню бота (/).
"""

import logging
from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.config import Config
from utils.logger import log_action
# from utils.keyboards import get_examples_keyboard
from utils.bot_commands import BotCommandManager

logger = logging.getLogger(__name__)


# Обработчики для маркетологов
async def examples_command(message: Message):
    """Команда /examples - примеры заявок"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "marketer":
        await message.answer("❌ Эта команда доступна только маркетологам.")
        return
    
    log_action(user_id, "examples_command", "")
    
    await message.answer(
        "📝 **Примеры заявок на оплату:**\n\n"
        "**1. Классический формат:**\n"
        "`Нужна оплата сервиса [НАЗВАНИЕ] на сумму [СУММА]$ для проекта [ПРОЕКТ], [СПОСОБ]: [ДЕТАЛИ]`\n\n"
        "**2. Естественный язык:**\n"
        "• `Привет, мне нужно оплатить фейсбук на сотку для проекта Альфа через крипту`\n"
        "• `Нужна оплата гугл адс 50 долларов проект Бета телефон +1234567890`\n"
        "• `Оплати инстаграм 200$ проект Гамма счет 1234-5678`\n\n"
        "**Способы оплаты:**\n"
        "• **crypto** - криптовалюта (адрес кошелька)\n"
        "• **phone** - номер телефона\n"
        "• **account** - банковский счет\n"
        "• **file** - файл с реквизитами",
        parse_mode="Markdown"
    )


async def formats_command(message: Message):
    """Команда /formats - форматы сообщений"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "marketer":
        await message.answer("❌ Эта команда доступна только маркетологам.")
        return
    
    log_action(user_id, "formats_command", "")
    
    await message.answer(
        "📄 **Поддерживаемые форматы сообщений:**\n\n"
        "**1. Классический структурированный формат:**\n"
        "`Нужна оплата сервиса [НАЗВАНИЕ] на сумму [СУММА]$ для проекта [ПРОЕКТ], [СПОСОБ]: [ДЕТАЛИ]`\n\n"
        "**2. 🆕 Естественный язык (ИИ):**\n"
        "• `Привет, мне нужно оплатить фейсбук на сотку для проекта Альфа через крипту`\n"
        "• `Нужна оплата гугл адс 50 долларов проект Бета телефон +1234567890`\n\n"
        "**Способы оплаты:**\n"
        "• **crypto** - криптовалюта (адрес кошелька)\n"
        "• **phone** - номер телефона\n"
        "• **account** - банковский счет/реквизиты\n"
        "• **file** - прикрепленный файл с реквизитами",
        parse_mode="Markdown"
    )


async def natural_command(message: Message):
    """Команда /natural - примеры естественного языка"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "marketer":
        await message.answer("❌ Эта команда доступна только маркетологам.")
        return
    
    log_action(user_id, "natural_command", "")
    
    await message.answer(
        "🤖 **Примеры естественного языка:**\n\n"
        "**Facebook реклама:**\n"
        "• `Привет, мне нужно оплатить фейсбук на сотку для проекта Альфа через крипту`\n"
        "• `Оплати фейсбук 100$ проект Alpha криптой`\n\n"
        "**Google Ads:**\n"
        "• `Нужна оплата гугл адс 50 долларов проект Бета телефон +1234567890`\n"
        "• `Гугл реклама 50$ проект Beta через телефон`\n\n"
        "**Instagram:**\n"
        "• `Оплати инстаграм 200$ проект Гамма счет 1234-5678`\n"
        "• `Инста реклама 200 долларов проект Gamma банковский счет`\n\n"
        "**TikTok:**\n"
        "• `Требуется оплата тикток 75$ для проекта Дельта, прикрепляю файл`\n"
        "• `ТикТок реклама 75$ проект Delta файлом`\n\n"
        "🎯 **Главное:** Укажите сервис, сумму, проект и способ оплаты в любом порядке!",
        parse_mode="Markdown"
    )


# Обработчики для финансистов
async def confirm_command(message: Message):
    """Команда /confirm - подтверждение оплаты"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "financier":
        await message.answer("❌ Эта команда доступна только финансистам.")
        return
    
    log_action(user_id, "confirm_command", "")
    
    await message.answer(
        "✅ **Подтверждение оплаты:**\n\n"
        "**Формат сообщения:**\n"
        "`Оплачено [ID_ЗАЯВКИ]` + прикрепите подтверждение\n\n"
        "**Примеры:**\n"
        "• `Оплачено 123` + скриншот транзакции\n"
        "• `Оплачено 124, хэш: 0xabc123...` + файл\n"
        "• `Оплачено 125` + чек об оплате\n\n"
        "**Важно:**\n"
        "• Обязательно укажите ID заявки\n"
        "• Прикрепите файл подтверждения (скриншот, хэш, чек)\n"
        "• После подтверждения маркетолог получит уведомление",
        parse_mode="Markdown"
    )


async def operations_command(message: Message):
    """Команда /operations - операции финансиста"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "financier":
        await message.answer("❌ Эта команда доступна только финансистам.")
        return
    
    log_action(user_id, "operations_command", "")
    
    await message.answer(
        "📊 **Мои операции:**\n\n"
        "Функция в разработке...\n\n"
        "Скоро здесь будет:\n"
        "• История подтвержденных оплат\n"
        "• Статистика по дням/неделям\n"
        "• Фильтрация по проектам\n"
        "• Экспорт отчетов",
        parse_mode="Markdown"
    )


# Обработчики для руководителей
async def addbalance_command(message: Message):
    """Команда /addbalance - пополнение баланса"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "manager":
        await message.answer("❌ Эта команда доступна только руководителям.")
        return
    
    log_action(user_id, "addbalance_command", "")
    
    await message.answer(
        "💵 **Пополнение баланса:**\n\n"
        "**🆕 Поддерживается естественный язык:**\n\n"
        "**Классический формат:**\n"
        "• `Added 1000$`\n"
        "• `Added 500$ пополнение от клиента X`\n\n"
        "**Естественный язык (ИИ):**\n"
        "• `Пополнение 1000`\n"
        "• `Добавить 500 на баланс`\n"
        "• `Закинь 200 долларов от клиента Альфа`\n"
        "• `Получили оплату 850$ от заказчика`\n"
        "• `Нужно добавить 2000 долларов`\n"
        "• `Баланс пополнить на 1500`\n\n"
        "🎯 **Просто напишите сумму и описание в любом формате!**",
        parse_mode="Markdown"
    )


async def reports_command(message: Message):
    """Команда /reports - отчеты"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "manager":
        await message.answer("❌ Эта команда доступна только руководителям.")
        return
    
    log_action(user_id, "reports_command", "")
    
    await message.answer(
        "📈 **Отчеты системы:**\n\n"
        "Функция в разработке...\n\n"
        "Планируемые отчеты:\n"
        "• 📊 Статистика по проектам\n"
        "• 💰 Движение средств\n"
        "• 📈 Динамика расходов\n"
        "• 👥 Активность пользователей\n"
        "• 📅 Отчеты по периодам\n"
        "• 📤 Экспорт данных",
        parse_mode="Markdown"
    )


async def summary_command(message: Message):
    """Команда /summary - сводка дня"""
    user_id = message.from_user.id
    config = Config()
    
    if config.get_user_role(user_id) != "manager":
        await message.answer("❌ Эта команда доступна только руководителям.")
        return
    
    log_action(user_id, "summary_command", "")
    
    # Получаем статистику (используем существующий обработчик)
    from handlers.manager import statistics_handler
    await statistics_handler(message)


# Общая команда меню
async def menu_command(message: Message):
    """Команда /menu - показать меню"""
    user_id = message.from_user.id
    config = Config()
    role = config.get_user_role(user_id)
    
    if role == "unknown":
        await message.answer("❌ У вас нет доступа к этому боту.")
        return
    
    log_action(user_id, "menu_command", "")
    
    from handlers.menu_handler import show_main_menu
    await show_main_menu(message, role)


def setup_command_handlers(dp: Dispatcher):
    """Регистрация обработчиков команд"""
    
    def is_authorized(message: Message) -> bool:
        return Config.is_authorized(message.from_user.id)
    
    def is_marketer(message: Message) -> bool:
        return Config.get_user_role(message.from_user.id) == "marketer"
    
    def is_financier(message: Message) -> bool:
        return Config.get_user_role(message.from_user.id) == "financier"
    
    def is_manager(message: Message) -> bool:
        return Config.get_user_role(message.from_user.id) == "manager"
    
    # Общие команды
    # dp.message.register(menu_command, Command("menu"), is_authorized)  # Убрано
    
    # Команды для маркетологов
    dp.message.register(examples_command, Command("examples"), is_marketer)
    dp.message.register(formats_command, Command("formats"), is_marketer)
    dp.message.register(natural_command, Command("natural"), is_marketer)
    
    # Команды для финансистов
    dp.message.register(confirm_command, Command("confirm"), is_financier)
    dp.message.register(operations_command, Command("operations"), is_financier)
    
    # Команды для руководителей
    dp.message.register(addbalance_command, Command("addbalance"), is_manager)
    dp.message.register(reports_command, Command("reports"), is_manager)
    dp.message.register(summary_command, Command("summary"), is_manager)