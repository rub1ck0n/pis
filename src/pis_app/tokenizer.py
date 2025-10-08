from __future__ import annotations
import shlex
from .errors import TokenizationError

def split_type_and_props(line: str) -> tuple[str, str]:
    """Делит строку по первому двоеточию на (type_part, props)."""
    if ":" not in line:
        raise TokenizationError("Отсутствует двоеточие, отделяющее тип и свойства.")
    left, right = line.split(":", 1)
    type_part = " ".join(left.split())  # нормализация пробелов
    props = right.strip()
    if not type_part:
        raise TokenizationError("Тип объекта пустой.")
    if not props:
        raise TokenizationError("Список свойств пуст.")
    return type_part, props

def tokenize_props(props: str) -> list[str]:
    """Разбивает свойства с учётом кавычек."""
    try:
        tokens = shlex.split(props)
    except ValueError as exc:
        raise TokenizationError(f"Ошибка токенизации: {exc}") from exc
    if not tokens:
        raise TokenizationError("Не получены токены свойств.")
    return tokens
