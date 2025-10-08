from __future__ import annotations
from typing import Iterable, Iterator
from .tokenizer import split_type_and_props, tokenize_props
from .parsers import ParserRegistry, default_registry
from .errors import ParseError

def process_lines(lines: Iterable[str], registry: ParserRegistry | None = None) -> Iterator[dict]:
    """Построчная обработка: всегда выдаём результат (успех/ошибка) в виде dict"""
    reg = registry or default_registry()
    for i, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue
        try:
            type_part, props = split_type_and_props(line)
            tokens = tokenize_props(props)
            yield reg.parse(type_part, tokens)
        except ParseError as e:
            # Единый формат ошибок в потоке результатов
            yield {"type": "ERROR", "line": i, "message": str(e), "raw": line}
