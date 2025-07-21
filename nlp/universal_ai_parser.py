"""
Универсальный AI-парсер для всех типов команд и сообщений.
Использует OpenAI GPT-4 для максимально точного понимания естественного языка.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from openai import AsyncOpenAI
from utils.config import Config

logger = logging.getLogger(__name__)


class UniversalAIParser:
    """Универсальный AI-парсер для всех типов команд"""
    
    def __init__(self):
        self.config = Config()
        self.client = AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
        
        # Системный промпт для универсального парсинга
        self.system_prompt = """
Ты — эксперт по анализу сообщений в системе управления Telegram-ботом. 
Твоя задача — точно определить тип сообщения и извлечь все необходимые данные.

ТИПЫ ОПЕРАЦИЙ:
1. "balance_add" - пополнение баланса
2. "balance_reset" - обнуление баланса  
3. "payment_request" - заявка на оплату
4. "payment_confirm" - подтверждение оплаты
5. "analytics_query" - аналитический запрос (простые запросы баланса/статистики)
6. "ai_analytics" - сложный аналитический запрос для AI-помощника
7. "system_command" - системная команда
8. "unknown" - неопределенное сообщение

ПРАВИЛА АНАЛИЗА:

ПОПОЛНЕНИЕ БАЛАНСА (balance_add):
- Ключевые слова: пополни, добавь, закинь, внеси, поступило, зачисли, added, transfer, deposit
- Должна содержать числовую сумму
- Может содержать описание (от кого, для чего)

ОБНУЛЕНИЕ БАЛАНСА (balance_reset):
- Ключевые слова: обнули, очисти, сделай нулевой, reset, clear + баланс
- Должно быть явное указание на обнуление/очистку
- НЕ путать с пополнением на определенную сумму

ЗАЯВКА НА ОПЛАТУ (payment_request):
- Ключевые слова: оплати, нужна оплата, требуется оплата, pay, payment
- Содержит сумму и платформу/сервис
- Может содержать проект и способ оплаты

ПОДТВЕРЖДЕНИЕ ОПЛАТЫ (payment_confirm):
- Ключевые слова: оплачено, подтверждаю, выполнено, paid, confirmed
- Обязательно содержит ID заявки (число)
- Может содержать хэш транзакции, номер чека

АНАЛИТИЧЕСКИЙ ЗАПРОС (analytics_query):
- Только прямые команды статистики без подробной аналитики
- НЕ используется для конкретных вопросов с данными

СЛОЖНЫЙ АНАЛИТИЧЕСКИЙ ЗАПРОС (ai_analytics):
- Вопросительные слова: сколько, какой, что, как, где, когда, покажи
- Запросы с глубокой аналитикой: количество людей в команде, платежи за период, история баланса
- Сложные вопросы требующие AI-анализа данных  
- ВСЕ запросы баланса, операций, платежей, команды должны быть ai_analytics
- Ключевые слова: анализ, сколько человек, какие платежи, за неделю, за месяц, тенденции, статистика по проектам, покажи, последние операции, история баланса, ожидающие оплаты, платформы, баланс, операции
- Детальные запросы по данным дашборда

СИСТЕМНАЯ КОМАНДА (system_command):
- Команды помощи: помощь, справка, help, что умеешь, что ты умеешь, возможности, функции
- Команды начала работы: привет, старт, start, начать, меню, menu, здравствуй, доброе утро
- Команды дашборда: дашборд, dashboard, ссылка на дашборд, веб-интерфейс, панель управления
- AI помощник: ИИ помощник, AI помощник, искусственный интеллект, аналитик, AI
- Команда обнуления: сброс баланса, reset balance, обнулить баланс
- Общие системные запросы и приветствия

ФОРМАТ ОТВЕТА - строго JSON:
{
    "operation_type": "тип_операции",
    "amount": число_или_null,
    "description": "описание",
    "platform": "платформа_или_null",
    "project": "проект_или_null",
    "payment_method": "способ_оплаты_или_null",
    "payment_details": "детали_оплаты_или_null",
    "payment_id": число_или_null,
    "confidence": 0.95
}

ПРИМЕРЫ:

"пополни баланс на 500 баксов для Инсты для сайта из криптокошелька 12345678990"
→ {
    "operation_type": "balance_add",
    "amount": 500,
    "description": "для Инсты для сайта из криптокошелька 12345678990",
    "platform": "Инста",
    "project": "сайт",
    "payment_method": "криптокошелек",
    "payment_details": "12345678990",
    "confidence": 0.98
}

"обнули баланс"
→ {
    "operation_type": "balance_reset",
    "amount": null,
    "description": "обнуление баланса",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "confidence": 0.99
}

"нужна оплата фейсбук на 100 долларов проект Альфа через карту"
→ {
    "operation_type": "payment_request",
    "amount": 100,
    "description": "оплата фейсбук проект Альфа через карту",
    "platform": "фейсбук",
    "project": "Альфа", 
    "payment_method": "карта",
    "payment_details": null,
    "confidence": 0.97
}

"какой сейчас баланс?"
→ {
    "operation_type": "analytics_query",
    "amount": null,
    "description": "запрос текущего баланса",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "confidence": 0.95
}

"покажи последнюю операцию"
→ {
    "operation_type": "analytics_query",
    "amount": null,
    "description": "запрос последней операции",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.98
}

"оплачено 123"
→ {
    "operation_type": "payment_confirm",
    "amount": null,
    "description": "подтверждение оплаты заявки 123",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": 123,
    "confidence": 0.99
}

"нужна ссылка на дашборд"
→ {
    "operation_type": "system_command",
    "amount": null,
    "description": "запрос ссылки на дашборд",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.95
}

"запусти ИИ помощник"
→ {
    "operation_type": "system_command",
    "amount": null,
    "description": "запрос AI помощника",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.98
}

"привет! что ты умеешь?"
→ {
    "operation_type": "system_command",
    "amount": null,
    "description": "запрос возможностей системы",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.96
}

"сколько человек в команде?"
→ {
    "operation_type": "ai_analytics",
    "amount": null,
    "description": "запрос количества людей в команде",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.95
}

"какие платежи были на этой неделе?"
→ {
    "operation_type": "ai_analytics",
    "amount": null,
    "description": "запрос платежей за неделю",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.92
}

"покажи ожидающие оплаты"
→ {
    "operation_type": "ai_analytics",
    "amount": null,
    "description": "запрос ожидающих оплат",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.94
}

"какой сейчас баланс?"
→ {
    "operation_type": "ai_analytics",
    "amount": null,
    "description": "запрос текущего баланса",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.96
}

"последние операции"
→ {
    "operation_type": "ai_analytics",
    "amount": null,
    "description": "запрос последних операций",
    "platform": null,
    "project": null,
    "payment_method": null,
    "payment_details": null,
    "payment_id": null,
    "confidence": 0.94
}

ВАЖНО: Всегда возвращай валидный JSON. Если не уверен в типе - используй "unknown" с низким confidence.
"""
    
    async def parse_message(self, text: str, user_role: str = "manager") -> Optional[Dict[str, Any]]:
        """
        Универсальный парсинг сообщения
        
        Args:
            text: Текст сообщения
            user_role: Роль пользователя (manager, financier, marketer)
            
        Returns:
            Словарь с данными операции или None
        """
        if not text or not text.strip():
            return None
            
        text = text.strip()
        logger.info(f"AI парсинг сообщения ({user_role}): {text}")
        
        try:
            # Добавляем контекст роли в промпт
            role_context = f"\nКонтекст: Пользователь имеет роль '{user_role}'. "
            if user_role == "manager":
                role_context += "Может пополнять баланс, делать аналитические запросы, обнулять баланс, запрашивать дашборд, получать системные команды."
            elif user_role == "financier":
                role_context += "Может подтверждать/отклонять оплаты, делать аналитические запросы."
            elif user_role == "marketer":
                role_context += "Может создавать заявки на оплату, делать аналитические запросы."
            
            # Отправка запроса к OpenAI
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt + role_context},
                    {"role": "user", "content": text}
                ],
                max_tokens=300,
                temperature=0.1
            )
            
            # Получение ответа
            content = response.choices[0].message.content.strip()
            logger.info(f"OpenAI ответ: {content}")
            
            # Парсинг JSON ответа
            try:
                parsed_data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON: {e}")
                return None
            
            # Валидация данных
            if not self._validate_parsed_data(parsed_data):
                logger.warning("Данные не прошли валидацию")
                return None
            
            # Нормализация данных
            normalized_data = self._normalize_parsed_data(parsed_data)
            
            logger.info(f"Успешно распарсено AI: {normalized_data}")
            return normalized_data
            
        except Exception as e:
            logger.error(f"Ошибка AI парсинга: {e}")
            return None
    
    def _validate_parsed_data(self, data: Dict[str, Any]) -> bool:
        """Валидация данных от GPT"""
        if not isinstance(data, dict):
            return False
        
        # Проверка обязательных полей
        required_fields = ["operation_type", "confidence"]
        for field in required_fields:
            if field not in data:
                logger.warning(f"Отсутствует обязательное поле: {field}")
                return False
        
        # Проверка типа операции
        valid_operations = [
            "balance_add", "balance_reset", "payment_request", "payment_confirm",
            "analytics_query", "ai_analytics", "system_command", "unknown"
        ]
        if data["operation_type"] not in valid_operations:
            logger.warning(f"Неверный тип операции: {data['operation_type']}")
            return False
        
        # Проверка confidence
        confidence = data.get("confidence", 0)
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            logger.warning(f"Неверное значение confidence: {confidence}")
            return False
        
        # Проверка суммы для операций с балансом и оплатой
        if data["operation_type"] in ["balance_add", "payment_request"]:
            amount = data.get("amount")
            if amount is not None and (not isinstance(amount, (int, float)) or amount <= 0):
                logger.warning(f"Неверная сумма: {amount}")
                return False
        
        # Проверка payment_id для подтверждения оплаты
        if data["operation_type"] == "payment_confirm":
            payment_id = data.get("payment_id")
            if payment_id is None or not isinstance(payment_id, int) or payment_id <= 0:
                logger.warning(f"Неверный ID платежа: {payment_id}")
                return False
        
        return True
    
    def _normalize_parsed_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Нормализация данных"""
        normalized = {
            "operation_type": data["operation_type"],
            "amount": float(data["amount"]) if data.get("amount") is not None else None,
            "description": str(data.get("description", "")).strip(),
            "platform": str(data.get("platform", "")).strip() if data.get("platform") else None,
            "project": str(data.get("project", "")).strip() if data.get("project") else None,
            "payment_method": str(data.get("payment_method", "")).strip() if data.get("payment_method") else None,
            "payment_details": str(data.get("payment_details", "")).strip() if data.get("payment_details") else None,
            "payment_id": int(data["payment_id"]) if data.get("payment_id") is not None else None,
            "confidence": float(data.get("confidence", 0))
        }
        
        return normalized
    
    async def test_connection(self) -> bool:
        """Тест подключения к OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения к OpenAI: {e}")
            return False
    
    def get_examples(self) -> List[Dict[str, str]]:
        """Возвращает примеры правильного формата сообщений"""
        return [
            {
                "input": "пополни баланс на 500 баксов для Инсты для сайта из криптокошелька 12345678990",
                "expected": "balance_add: 500$ для Инсты для сайта из криптокошелька 12345678990"
            },
            {
                "input": "обнули баланс",
                "expected": "balance_reset: обнуление баланса"
            },
            {
                "input": "нужна оплата фейсбук на 100 долларов проект Альфа через карту",
                "expected": "payment_request: 100$ фейсбук проект Альфа через карту"
            },
            {
                "input": "какой сейчас баланс?",
                "expected": "analytics_query: запрос текущего баланса"
            },
            {
                "input": "добавь 1000 рублей от партнера",
                "expected": "balance_add: 1000$ от партнера"
            },
            {
                "input": "закинь 250 долларов на рекламу",
                "expected": "balance_add: 250$ на рекламу"
            }
        ]