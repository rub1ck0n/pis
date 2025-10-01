import json, shlex

# 1. Разбор строки
def parse_line(line: str) -> dict:
    type_part, props = line.split(":", 1)
    tokens = shlex.split(props)
    date, plate, mark, speed = tokens[0], tokens[1], tokens[2], tokens[3]
    return {
        "type": type_part.strip(),
        "date": date,
        "plate": plate,
        "mark": mark,
        "speed": speed
    }

filename = "input.txt"
with open(filename, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        obj = parse_line(line)  # вызываем функцию
        print(json.dumps(obj, ensure_ascii=False))
