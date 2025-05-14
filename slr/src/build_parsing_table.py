from src.grammar_utils import Grammar, Production, Rule
from src.table import Table, Line


def build_parsing_table(grammar: Grammar) -> Table:
    table = Table([], [])
    table.symbols = get_all_symbols(grammar)

    firstLine = Line([], {})
    first_pair = next(iter(grammar.rules.items()), None)
    first_key: str
    first_rule: Rule
    first_key, first_rule = first_pair
    # firstSymbol = Symbol(first_rule.nonterminal)
    add_direction_symbols(firstLine, first_rule.productions)

    return


def get_all_symbols(grammar: Grammar) -> list[str]:
    symbols = set()

    for nonterminal, rule in grammar.rules:
        symbols.add(nonterminal)
        symbols = add_symbols_from_first_set(symbols, rule)

    return list(symbols)


def add_symbols_from_first_set(symbols: set[str], rule: Rule) -> set[str]:
    for production in rule.productions:
        for symbol in production.first_set:
            symbols.add(symbol)

    return symbols


def add_direction_symbols(line: Line, first_set: list[Production]):
    for symbol in first_set:
        symbol_name = symbol.name
        if symbol_name in line.next_symbols:
            if symbol not in line.next_symbols[symbol_name]:
                line.next_symbols[symbol_name].append(symbol)
        else:
            line.next_symbols[symbol_name] = [symbol]
