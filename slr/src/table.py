from dataclasses import dataclass

END_SYMBOL_IN_TABLE = "R"

# @dataclass
# class Symbol:
#     name: str
    # num_of_rule: int | None = None
    # num_of_right_part: int | None = None


@dataclass
class Line:
    symbols: list[str]
    next_symbols: dict[str, list[str]]


@dataclass
class Table:
    symbols: list[str]
    lines: list[Line]
