from typing import List, Set
from Table import Table, TableStr, END_SYMBOL_IN_TABLE
from Rule import Rule, is_non_terminal, get_nonterminal_rules, END_SYMBOL
from Symbol import Symbol
from GetDirectionSymbols import define_direction_symbols_after_non_terminal


def add_symbols_from_right_part(rule: Rule, symbols: Set[str]) -> None:
    symbols.update(rule.right_part)


def get_all_symbols(grammar: List[Rule]) -> Set[str]:
    symbols = set()
    for rule in grammar:
        symbols.add(rule.non_terminal)
        add_symbols_from_right_part(rule, symbols)
    return symbols


def add_direction_symbols(table_str: TableStr, direction_symbols: List[Symbol], grammar: List[Rule]) -> None:
    for symbol in direction_symbols:
        if symbol.name in table_str.next_symbols:
            if symbol not in table_str.next_symbols[symbol.name]:
                table_str.next_symbols[symbol.name].append(symbol)
        else:
            table_str.next_symbols[symbol.name] = [symbol]


def add_end_direction_symbols(table_str: TableStr, direction_symbols: List[Symbol], num_of_rule: int) -> None:
    for symbol in direction_symbols:
        end_symbol = Symbol(name=END_SYMBOL_IN_TABLE, num_of_rule=num_of_rule)
        if symbol.name in table_str.next_symbols:
            if end_symbol not in table_str.next_symbols[symbol.name]:
                table_str.next_symbols[symbol.name].append(end_symbol)
        else:
            table_str.next_symbols[symbol.name] = [end_symbol]


def has_state_in_table(table_strs: List[TableStr], symbols_of_state: List[Symbol]) -> bool:
    for table_str in table_strs:
        if table_str.symbols == symbols_of_state:
            return True
    return False


def define_next_symbols(grammar: List[Rule], num_of_rule: int, num_of_right_part: int, table_str: TableStr) -> None:
    symbol_name = grammar[num_of_rule].right_part[num_of_right_part]
    symbol = Symbol(
        name=symbol_name,
        num_of_rule=num_of_rule,
        num_of_right_part=num_of_right_part
    )

    if is_non_terminal(symbol.name, grammar):
        direction_symbols = [symbol]
        rules = get_nonterminal_rules(grammar, symbol_name)
        for rule in rules:
            direction_symbols.extend(rule.direction_symbols)
        add_direction_symbols(table_str, direction_symbols, grammar)

    if symbol.name == END_SYMBOL:
        add_end_direction_symbols(table_str, [symbol], symbol.num_of_rule)
        return

    add_direction_symbols(table_str, [symbol], grammar)


def add_info_in_string(table_str: TableStr, symbols: List[Symbol], grammar: List[Rule]) -> None:
    for s in symbols:
        if s.num_of_rule is None or s.num_of_right_part is None or s.name == END_SYMBOL:
            continue

        table_str.symbols.append(s)
        is_end_of_rule = len(grammar[s.num_of_rule].right_part) - 1 == s.num_of_right_part

        if is_end_of_rule:
            direction_symbols = define_direction_symbols_after_non_terminal(
                set(), grammar[s.num_of_rule].non_terminal, grammar
            )
            add_end_direction_symbols(table_str, direction_symbols, s.num_of_rule)
            continue

        define_next_symbols(grammar, s.num_of_rule, s.num_of_right_part + 1, table_str)


def add_new_strings(table: Table, num_of_str: int, grammar: List[Rule]) -> None:
    table_str = table.strings[num_of_str]
    new_strs = []

    for next_symbol_name, next_symbols in table_str.next_symbols.items():
        if (has_state_in_table(table.strings, next_symbols) or
                has_state_in_table(new_strs, next_symbols)):
            continue

        new_str = TableStr(symbols=[], next_symbols={})
        add_info_in_string(new_str, next_symbols, grammar)

        if new_str.symbols:
            new_strs.append(new_str)

    table.strings.extend(new_strs)

    if num_of_str + 1 < len(table.strings):
        add_new_strings(table, num_of_str + 1, grammar)


def create_table(grammar: List[Rule]) -> Table:
    table = Table(symbols=set(), strings=[])
    table.symbols = get_all_symbols(grammar)

    first_str = TableStr(symbols=[], next_symbols={})
    symbol_of_first_str = Symbol(name=grammar[0].non_terminal)
    first_str.symbols.append(symbol_of_first_str)
    add_direction_symbols(first_str, grammar[0].direction_symbols, grammar)

    ok_symbol = Symbol(name="OK")
    first_str.next_symbols[grammar[0].non_terminal] = [ok_symbol]

    for i in range(1, len(grammar)):
        rule = grammar[i]
        if len(rule.right_part) == 1 and rule.right_part[0] == END_SYMBOL:
            end_symbol = Symbol(name=END_SYMBOL_IN_TABLE, num_of_rule=i)
            first_str.next_symbols[END_SYMBOL] = [end_symbol]
            continue

        if rule.non_terminal == symbol_of_first_str.name:
            add_direction_symbols(first_str, rule.direction_symbols, grammar)

    table.strings.append(first_str)
    add_new_strings(table, 0, grammar)

    return table