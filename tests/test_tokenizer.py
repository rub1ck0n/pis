import pytest
from src.pis_app.tokenizer import split_type_and_props, tokenize_props
from src.pis_app.errors import TokenizationError

def test_split_ok():
    t, p = split_type_and_props('Фиксация проезда автомобилей: 2025.10.01 08:00 "А123ВС77" 60')
    assert t == "Фиксация проезда автомобилей"
    assert p.startswith("2025.10.01")

def test_split_fail_no_colon():
    with pytest.raises(TokenizationError):
        split_type_and_props('Нет двоеточия 2025.10.01 "А123ВС77"')

def test_tokens_quotes():
    tokens = tokenize_props('2025.10.01 08:00 "А123ВС77" 60')
    assert tokens == ["2025.10.01", "08:00", "А123ВС77", "60"]
