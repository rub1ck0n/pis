import json, shlex

# Общая токенизация строки
def tokenize(line: str):
    type_part, props = line.split(":", 1)
    type_part = " ".join(type_part.split())  # нормализуем пробелы
    tokens = shlex.split(props)
    return type_part, tokens

# Парсеры под конкретные типы

# Тип 1: Фиксация проезда автомобилей
# Формат свойств: "гггг.мм.дд" "чч:мм" "номер автомобиля" "скорость"
def parse_car_passage(tokens):
    date, time, plate, speed = tokens[0], tokens[1], tokens[2], tokens[3]
    return {"Дата": date, "Время": time, "Номер": plate, "Скорость": speed}

# Тип 2: Регистрация парковки
# Формат свойств: "гггг.мм.дд" "чч:мм" "номер автомобиля" "номер места" "стоимость за час"
def parse_parking(tokens):
    date, time, plate, place, cost = tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]
    return {"Дата": date, "Время": time, "Номер": plate, "Место на парковке": place, "Стоимость": cost}

# Тип 3: Регистрация заправки
# Формат свойств: "гггг.мм.дд" "чч:мм" "номер автомобиля"
#                 "тип топлива" "итоговая цена заправки"
def parse_refuel(tokens):
    date, time, plate, fuel, cost = tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]
    return {"Дата": date, "Время": time, "Номер": plate, "Вид топлива": fuel, "Стоимость": cost}

# Таблица соответствий "тип ---> функция-парсер"
PARSERS = {
    "Фиксация проезда автомобилей": parse_car_passage,
    "Регистрация парковки": parse_parking,
    "Регистрация заправки": parse_refuel,
}

# 1. Разбор строки по типам объектов через таблицу парсеров
def parse_line(line: str) -> dict:
    type_part, tokens = tokenize(line)
    parser = PARSERS.get(type_part)
    if parser:
        data = parser(tokens)
        return {"type": type_part, **data}
    # неизвестный тип — просто вернём "сырые" токены
    return {"type": type_part, "raw": tokens}

# 2. Обработка файла
def process_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield parse_line(line)

# 3. Главная функция программы
def main():
    filename = "input.txt"
    for obj in process_file(filename):
        print(json.dumps(obj, ensure_ascii=False))  # вывод в JSON

if __name__ == "__main__":
    main()
