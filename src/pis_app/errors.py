class ParseError(Exception):
    """Базовая ошибка разбора входной строки."""


class UnknownTypeError(ParseError):
    """Неизвестный тип объекта слева от двоеточия."""


class TokenizationError(ParseError):
    """Не удалось корректно токенизировать строку (кавычки/двоеточие/и т.п.)."""


class ValidationError(ParseError):
    """Валидные по синтаксису токены, но семантически некорректные значения."""
