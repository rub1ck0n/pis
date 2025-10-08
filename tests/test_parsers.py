import pytest
from src.pis_app.parsers import default_registry
from src.pis_app.errors import UnknownTypeError, ValidationError

def reg():
    return default_registry()

def test_car_passage_ok():
    data = reg().parse("Фиксация проезда автомобилей", ["2025.10.01","08:00","А123ВС77","60"])
    assert data["Plate"] == "А123ВС77"
    assert data["Speed"] == "60"

def test_parking_ok():
    data = reg().parse("Регистрация парковки", ["2025.10.01","08:00","А123ВС77","P1","200"])
    assert data["Place"] == "P1"

def test_refuel_ok():
    data = reg().parse("Регистрация заправки", ["2025.10.01","08:00","А123ВС77","АИ-95","2800"])
    assert data["Fuel"] == "АИ-95"

def test_unknown_type():
    with pytest.raises(UnknownTypeError):
        reg().parse("Непонятный тип", ["x"])

def test_bad_speed():
    with pytest.raises(ValidationError):
        reg().parse("Фиксация проезда автомобилей", ["2025.10.01","08:00","А123ВС77","xx"])
