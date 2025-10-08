from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Dict, List
from .validators import (
    validate_date, validate_time, validate_plate,
    validate_int, validate_fuel, validate_nonempty
)
from .errors import ValidationError, UnknownTypeError

# Протокол для стратегий парсинга (SRP + Strategy)
class Parser(Protocol):
    def parse(self, tokens: List[str]) -> dict: ...

@dataclass(frozen=True)
class CarPassageParser:
    """Тип 1: Фиксация проезда автомобилей
       Формат: гггг.мм.дд чч:мм "номер" скорость
    """
    def parse (self, tokens: List[str]) -> dict:
        if len(tokens) < 4:
            raise ValidationError("Ожидалось 4 свойства: дата, время, номер, скорость.")
        date = validate_date(tokens[0])
        time = validate_time(tokens[1])
        plate = validate_plate(tokens[2])
        speed = validate_int(tokens[3], "Скорость")
        return {"Date": date, "Time": time, "Plate": plate, "Speed": speed}

@dataclass(frozen=True)
class ParkingParser:
    """Тип 2: Регистрация парковки
       Формат: гггг.мм.дд чч:мм "номер" место стоимость_за_час
    """
    def parse(self, tokens: List[str]) -> dict:
        if len(tokens) < 5:
            raise ValidationError("Ожидалось 5 свойств: дата, время, номер, место, стоимость.")
        date = validate_date(tokens[0])
        time = validate_time(tokens[1])
        plate = validate_plate(tokens[2])
        place = validate_nonempty(tokens[3], "Номер места")
        cost = validate_int(tokens[4], "Стоимость за час")
        return {"Date": date, "Time": time, "Plate": plate, "Place": place, "Cost": cost}

@dataclass(frozen=True)
class RefuelParser:
    """Тип 3: Регистрация заправки
       Формат: гггг.мм.дд чч:мм "номер" тип_топлива сумма
    """
    def parse(self, tokens: List[str]) -> dict:
        if len(tokens) < 5:
            raise ValidationError("Ожидалось 5 свойств: дата, время, номер, топливо, цена.")
        date = validate_date(tokens[0])
        time = validate_time(tokens[1])
        plate = validate_plate(tokens[2])
        fuel = validate_fuel(tokens[3])
        cost = validate_int(tokens[4], "Стоимость")
        return {"Date": date, "Time": time, "Plate": plate, "Fuel": fuel, "Cost": cost}

# Реестр стратегий
class ParserRegistry:
    def __init__(self):
        self._parsers: Dict[str, Parser] = {}

    def register(self, type_name: str, parser: Parser) -> None:
        self._parsers[type_name] = parser

    def parse(self, type_name: str, tokens: list[str]) -> dict:
        if type_name not in self._parsers:
            raise UnknownTypeError(f"Неизвестный тип: {type_name}")
        data = self._parsers[type_name].parse(tokens)
        return {"type": type_name, **data}

def default_registry() -> ParserRegistry:
    reg = ParserRegistry()
    reg.register("Фиксация проезда автомобилей", CarPassageParser())
    reg.register("Регистрация парковки",       ParkingParser())
    reg.register("Регистрация заправки",       RefuelParser())
    return reg
