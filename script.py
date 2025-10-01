import json, shlex      # shlex разделяет строку на части, учитывая кавычки

filename = "input.txt"
with open(filename, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        type_part, props = line.split(":", 1)
        tokens = shlex.split(props)         # корректное разбиение props
        date, plate, mark, speed = tokens[0], tokens[1], tokens[2], tokens[3]
        obj = {"type": type_part, "date": date, "plate": plate, "mark": mark, "speed": speed}
        print(json.dumps(obj, ensure_ascii=False))          #преобразуем словарь в json-строку


