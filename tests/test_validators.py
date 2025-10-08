import pytest
from src.pis_app.validators import validate_date, validate_time, validate_plate, validate_fuel, ValidationError

def test_date_ok():
    assert validate_date("2025.10.07") == "2025.10.07"

def test_date_bad():
    with pytest.raises(ValidationError):
        validate_date("2025-10-07")

def test_time_ok():
    assert validate_time("09:30") == "09:30"

def test_time_bad():
    with pytest.raises(ValidationError):
        validate_time("9-30")

def test_plate_ok():
    assert validate_plate("А123ВС77") == "А123ВС77"

def test_plate_bad():
    with pytest.raises(ValidationError):
        validate_plate("A123BC77")  # латиница не допускается

def test_fuel_ok():
    assert validate_fuel("АИ-95") == "АИ-95"

def test_fuel_bad():
    with pytest.raises(ValidationError):
        validate_fuel("AI-95")
