from __future__ import annotations
import re
from datetime import datetime
from .errors import ValidationError

# Разрешённые буквы госномеров РФ по ГОСТу
RUS_LETTERS = "АВЕКМНОРСТУХ"
PLATE_RE = re.compile(rf"^[{RUS_LETTERS}]\d{{3}}[{RUS_LETTERS}]{{2}}\d{{2,3}}$")

def validate_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y.%m.%d")
    except ValueError as e:
        raise ValidationError(f"Дата должна быть в формате гггг.мм.дд: {value}") from e
    return value

def validate_time(value: str) -> str:
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError as e:
        raise ValidationError(f"Время должно быть в формате чч:мм: {value}") from e
    return value

def validate_plate(value: str) -> str:
    if not PLATE_RE.fullmatch(value):
        raise ValidationError(f"Неверный формат номера РФ: {value}")
    return value

def validate_int(value: str, name: str) -> str:
    try:
        int(value)
    except ValueError as e:
        raise ValidationError(f"{name} должно быть целым числом: {value}") from e
    return value

def validate_float(value: str, name: str) -> str:
    try:
        float(value.replace(",", "."))
    except ValueError as e:
        raise ValidationError(f"{name} должно быть числом: {value}") from e
    return value

FUEL_ALLOWED = {"АИ-92", "АИ-95", "АИ-98", "ДТ"}

def validate_fuel(value: str) -> str:
    if value.upper() not in FUEL_ALLOWED:
        raise ValidationError(f"Тип топлива не поддерживается: {value}")
    return value.upper()

def validate_nonempty(value: str, name: str) -> str:
    if not value:
        raise ValidationError(f"{name} не должно быть пустым.")
    return value
