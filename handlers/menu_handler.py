"""
Обработчик интерактивных меню и кнопок.
Обрабатывает нажатия на кнопки меню для всех ролей.
"""

import logging
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils.config import Config
from utils.logger import log_action
# from utils.keyboards import get_main_menu_keyboard, get_examples_keyboard, get_quick_actions_keyboard

logger = logging.getLogger(__name__)


async def menu_button_handler(message: Message):
    """Обработчик нажатий на кнопки меню"""
    user_id = message.from_user.id
    config = Config()
    user_role = config.get_user_role(user_id)
    
    if user_role == "unknown":
        return
    
    button_text = message.text
    log_action(user_id, "menu_button", button_text)
    
    try:
        # Обработка общих кнопок
        if button_text == "🏠 Главное меню":
            await show_main_menu(message, user_role)
            
        elif button_text == "📋 Справка":
            from handlers.common import help_handler
            await help_handler(message)
            
        # Обработка кнопок маркетологов
        elif user_role == "marketer":
            if button_text == "💳 Создать заявку на оплату":
                await message.answer(
                    "💳 **Создание заявки на оплату**\n\n"
                    "🆕 **Поддерживается естественный язык!**\n\n"
                    "**Примеры:**\n"
                    "• `Привет, мне нужно оплатить фейсбук на сотку для проекта Альфа через крипту`\n"
                    "• `Нужна оплата гугл адс 50 долларов проект Бета телефон +1234567890`\n"
                    "• `Оплати инстаграм 200$ проект Гамма счет 1234-5678`\n\n"
                    "Просто напишите свой запрос естественным языком!",
                    parse_mode="Markdown"
                )
                
            elif button_text == "📝 Примеры заявок":
                await message.answer(
                    "📝 **Примеры заявок на оплату:**\n\n"
                    "**1. Классический формат:**\n"
                    "`Нужна оплата сервиса [НАЗВАНИЕ] на сумму [СУММА]$ для проекта [ПРОЕКТ], [СПОСОБ]: [ДЕТАЛИ]`\n\n"
                    "**2. Естественный язык:**\n"
                    "• `Привет, мне нужно оплатить фейсбук на сотку для проекта Альфа через крипту`\n"
                    "• `Нужна оплата гугл адс 50 долларов проект Бета телефон +1234567890`\n"
                    "• `Оплати инстаграм 200$ проект Гамма счет 1234-5678`\n\n"
                    "**Способы оплаты:**\n"
                    "• **crypto** - криптовалюта\n"
                    "• **phone** - номер телефона\n"
                    "• **account** - банковский счет\n"
                    "• **file** - файл с реквизитами",
                    parse_mode="Markdown"
                )
        
        # Обработка кнопок финансистов
        elif user_role == "financier":
            if button_text == "💰 Показать баланс":
                from handlers.financier import balance_command_handler
                await balance_command_handler(message)
                
            elif button_text == "✅ Подтвердить оплату":
                await message.answer(
                    "✅ **Подтверждение оплаты**\n\n"
                    "**Формат:**\n"
                    "`Оплачено [ID_ЗАЯВКИ]` + прикрепите подтверждение\n\n"
                    "**Примеры:**\n"
                    "• `Оплачено 123` + скриншот\n"
                    "• `Оплачено 124, хэш: 0xabc123...`\n\n"
                    "Отправьте ID заявки и прикрепите файл подтверждения.",
                    parse_mode="Markdown"
                )
                
            elif button_text == "📊 Мои операции":
                await message.answer(
                    "📊 **Мои операции**\n\n"
                    "Функция в разработке...\n"
                    "Скоро вы сможете посмотреть историю своих операций.",
                    parse_mode="Markdown"
                )
        
        # Обработка кнопок руководителей
        elif user_role == "manager":
            if button_text == "💰 Показать баланс":
                from handlers.manager import statistics_handler
                await statistics_handler(message)
                
            elif button_text == "📊 Статистика":
                from handlers.manager import statistics_handler
                await statistics_handler(message)
                
            elif button_text == "💵 Пополнить баланс":
                await message.answer(
                    "💵 **Пополнение баланса**\n\n"
                    "🆕 **Поддерживается естественный язык!**\n\n"
                    "**Примеры:**\n"
                    "• `Пополнение 1000`\n"
                    "• `Добавить 500 на баланс`\n"
                    "• `Закинь 200 долларов от клиента Альфа`\n"
                    "• `Получили оплату 850$ от заказчика`\n\n"
                    "Просто напишите сумму и описание!",
                    parse_mode="Markdown"
                )
                
            elif button_text == "📈 Отчеты":
                await message.answer(
                    "📈 **Отчеты**\n\n"
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
                
    except Exception as e:
        logger.error(f"Ошибка обработки кнопки меню: {e}")
        await message.answer("❌ Произошла ошибка при обработке команды.")


async def show_main_menu(message: Message, user_role: str):
    """Показывает главное меню для роли"""
    role_names = {
        "marketer": "Маркетолог",
        "financier": "Финансист", 
        "manager": "Руководитель"
    }
    
    role_descriptions = {
        "marketer": "📝 Создавайте заявки на оплату в естественном языке",
        "financier": "💰 Управляйте балансом и подтверждайте оплаты",
        "manager": "📊 Контролируйте финансы и статистику системы"
    }
    
    await message.answer(
        f"🏠 **Главное меню - {role_names[user_role]}**\n\n"
        f"{role_descriptions[user_role]}\n\n"
        f"Используйте команды из меню (/) или напишите сообщение:",
        parse_mode="Markdown"
    )


async def callback_handler(callback: CallbackQuery):
    """Обработчик callback-запросов от inline кнопок"""
    user_id = callback.from_user.id
    config = Config()
    user_role = config.get_user_role(user_id)
    
    if user_role == "unknown":
        await callback.answer("❌ У вас нет доступа к этому боту.")
        return
    
    callback_data = callback.data
    log_action(user_id, "callback", callback_data)
    
    # Примеры для маркетологов
    if callback_data == "example_crypto":
        await callback.message.answer(
            "💳 **Пример заявки с криптовалютой:**\n\n"
            "`Нужна оплата сервиса Facebook Ads на сумму 100$ для проекта Alpha, криптовалюта: 0x1234567890abcdef`\n\n"
            "**Или естественным языком:**\n"
            "`Привет, мне нужно оплатить фейсбук на сотку для проекта Альфа через крипту`",
            parse_mode="Markdown"
        )
    elif callback_data == "example_phone":
        await callback.message.answer(
            "📱 **Пример заявки с телефоном:**\n\n"
            "`Оплата сервиса Google Ads на 50$ для проекта Beta, номер телефона: +1234567890`\n\n"
            "**Или естественным языком:**\n"
            "`Нужна оплата гугл адс 50 долларов проект Бета телефон +1234567890`",
            parse_mode="Markdown"
        )
    elif callback_data == "example_account":
        await callback.message.answer(
            "💰 **Пример заявки со счетом:**\n\n"
            "`Оплата сервиса Instagram на 200$ для проекта Gamma, счет: 1234-5678-9012-3456`\n\n"
            "**Или естественным языком:**\n"
            "`Оплати инстаграм 200$ проект Гамма счет 1234-5678`",
            parse_mode="Markdown"
        )
    elif callback_data == "example_file":
        await callback.message.answer(
            "📄 **Пример заявки с файлом:**\n\n"
            "`Нужна оплата сервиса TikTok на 75$ для проекта Delta, счет:` + прикрепите файл\n\n"
            "**Или естественным языком:**\n"
            "`Требуется оплата тикток 75$ для проекта Дельта, прикрепляю файл`",
            parse_mode="Markdown"
        )
    elif callback_data == "example_natural":
        await callback.message.answer(
            "🤖 **Примеры естественного языка:**\n\n"
            "• `Привет, мне нужно оплатить фейсбук на сотку для проекта Альфа через крипту`\n"
            "• `Нужна оплата гугл адс 50 долларов проект Бета телефон +1234567890`\n"
            "• `Оплати инстаграм 200$ проект Гамма счет 1234-5678`\n"
            "• `Требуется оплата тикток 75$ для проекта Дельта, прикрепляю файл`\n"
            "• `Мне нужно оплатить YouTube рекламу на 300 баксов для проекта Эпсилон через кошелек 0x123abc`",
            parse_mode="Markdown"
        )
    
    # Примеры для финансистов
    elif callback_data == "example_confirmation":
        await callback.message.answer(
            "✅ **Примеры подтверждения оплаты:**\n\n"
            "• `Оплачено 123` + скриншот\n"
            "• `Оплачено 124, хэш: 0xabc123...`\n"
            "• `Оплачено 125` + чек об оплате\n\n"
            "Обязательно прикрепите файл подтверждения!",
            parse_mode="Markdown"
        )
    elif callback_data == "example_balance_commands":
        await callback.message.answer(
            "📋 **Команды баланса для финансистов:**\n\n"
            "• `Покажи баланс` / `Сколько денег?`\n"
            "• `Текущий баланс` / `Баланс счета`\n"
            "• `/balance` (классическая команда)\n\n"
            "Все команды работают с естественным языком!",
            parse_mode="Markdown"
        )
    
    # Примеры для руководителей  
    elif callback_data == "example_balance_classic":
        await callback.message.answer(
            "💵 **Классическое пополнение баланса:**\n\n"
            "• `Added 1000$`\n"
            "• `Added 500$ пополнение от клиента X`\n"
            "• `Added 750$ поступление от проекта Y`",
            parse_mode="Markdown"
        )
    elif callback_data == "example_balance_natural":
        await callback.message.answer(
            "🤖 **Пополнение естественным языком:**\n\n"
            "• `Пополнение 1000`\n"
            "• `Добавить 500 на баланс`\n"
            "• `Закинь 200 долларов от клиента Альфа`\n"
            "• `Получили оплату 850$ от заказчика`\n"
            "• `Нужно добавить 2000 долларов`\n"
            "• `Баланс пополнить на 1500`",
            parse_mode="Markdown"
        )
    elif callback_data == "example_stats_commands":
        await callback.message.answer(
            "📊 **Команды статистики:**\n\n"
            "• `Статистика` / `Покажи отчет`\n"
            "• `Как дела?` / `Общая статистика`\n"
            "• `Покажи баланс` / `Сколько денег?`\n"
            "• `/stats` / `/balance` (классические команды)",
            parse_mode="Markdown"
        )
    
    # Быстрые действия
    elif callback_data == "quick_balance":
        from handlers.financier import balance_command_handler
        await balance_command_handler(callback.message)
    elif callback_data == "quick_stats":
        from handlers.manager import statistics_handler
        await statistics_handler(callback.message)
    elif callback_data.startswith("quick_"):
        await callback.message.answer(
            f"🚀 **Быстрое действие: {callback_data}**\n\n"
            "Функция в разработке...",
            parse_mode="Markdown"
        )
    
    await callback.answer()


def setup_menu_handlers(dp: Dispatcher):
    """Регистрация обработчиков меню"""
    
    def is_authorized(message):
        return Config.is_authorized(message.from_user.id)
    
    def is_authorized_callback(callback):
        return Config.is_authorized(callback.from_user.id)
    
    # Команда меню
    # dp.message.register(
    #     lambda msg: show_main_menu(msg, Config.get_user_role(msg.from_user.id)),
    #     Command("menu"),
    #     is_authorized
    # )  # Убрано
    
    # Обработчик кнопок меню отключен (reply кнопки убраны)
    # dp.message.register(
    #     menu_button_handler,
    #     F.text.regexp(r"^[📋🏠💳📝💰✅📊💵📈🚀]"),
    #     is_authorized
    # )
    
    # Обработчик callback-запросов
    dp.callback_query.register(
        callback_handler,
        is_authorized_callback
    )