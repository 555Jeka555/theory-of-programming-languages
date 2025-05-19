from typing import List, Set, TextIO
from Rule import Rule, get_rules_with_nonterminal, EMPTY_SYMBOL
from GetDirectionSymbols import define_direction_symbols
from io import TextIOBase


class GrammarError(Exception):
    pass


class UnreachableSymbolError(GrammarError):
    """Исключение для недостижимых символов"""
    pass


class UnproductiveSymbolError(GrammarError):
    """Исключение для непродуктивных символов"""
    pass


class AmbiguousGrammarError(GrammarError):
    """Исключение для неоднозначных грамматик"""
    pass


def is_reachable(grammar: List[Rule], start_symbol: str = None) -> bool:
    """Проверяет, все ли нетерминалы достижимы из начального символа."""
    if not grammar:
        return True

    if start_symbol is None:
        start_symbol = grammar[0].non_terminal

    reachable = {start_symbol}
    changed = True

    while changed:
        changed = False
        for rule in grammar:
            if rule.non_terminal in reachable:
                for symbol in rule.right_part:
                    if symbol.isupper() and symbol not in reachable:
                        reachable.add(symbol)
                        changed = True

    all_non_terminals = {rule.non_terminal for rule in grammar}
    return reachable.issuperset(all_non_terminals)


def is_productive(grammar: List[Rule]) -> bool:
    """Проверяет, все ли нетерминалы могут порождать терминальные строки."""
    if not grammar:
        return True

    productive = set()
    # Сначала находим все правила, которые прямо порождают терминалы
    for rule in grammar:
        if all(not symbol.isupper() for symbol in rule.right_part):  # Все символы - терминалы
            productive.add(rule.non_terminal)

    # Затем итеративно расширяем множество продуктивных нетерминалов
    changed = True
    while changed:
        changed = False
        for rule in grammar:
            if rule.non_terminal not in productive:
                # Проверяем, все ли символы в правой части продуктивны или терминалы
                if all((symbol in productive) or (not symbol.isupper()) for symbol in rule.right_part):
                    productive.add(rule.non_terminal)
                    changed = True

    # Проверяем, все ли нетерминалы продуктивны
    all_non_terminals = {rule.non_terminal for rule in grammar}
    return productive.issuperset(all_non_terminals)


def has_shift_reduce_conflict(grammar: List[Rule]) -> bool:
    """Проверяет наличие конфликтов сдвиг-свёртка."""
    for i, rule1 in enumerate(grammar):
        for j, rule2 in enumerate(grammar):
            if i == j:
                continue
            if (rule1.non_terminal == rule2.non_terminal and
                    len(rule1.right_part) > 0 and
                    len(rule2.right_part) > 0 and
                    rule1.right_part[-1] == rule2.right_part[0]):
                return True
    return False


def is_unambiguous(grammar: List[Rule]) -> bool:
    """Проверяет, является ли грамматика однозначной."""
    return not has_shift_reduce_conflict(grammar)


def read_right_part(right_part_str: str, non_terminal: str, rules: List[Rule]) -> None:
    right_parts = right_part_str.split("|")
    right_parts = [part.strip() for part in right_parts]
    for part in right_parts:
        rule = Rule(
            non_terminal=non_terminal,
            right_part=part.split()
        )
        rules.append(rule)


def get_right_part_without_nonterminal(rule: Rule, non_terminal: str) -> List[str]:
    return [s for s in rule.right_part if s != non_terminal]


def add_alternative_rules_without_empty_rule(
        rules: List[Rule],
        new_rules: List[Rule],
        non_terminal: str,
        has_changes: bool
) -> bool:
    rules_with_empty = get_rules_with_nonterminal(rules, non_terminal)

    for rule in rules_with_empty:
        if len(rule.right_part) == 1:
            has_changes = add_alternative_rules_without_empty_rule(
                rules, new_rules, rule.non_terminal, has_changes
            )
            continue

        new_rule = Rule(
            non_terminal=rule.non_terminal,
            right_part=get_right_part_without_nonterminal(rule, non_terminal)
        )

        if new_rule not in rules and new_rule not in new_rules:
            has_changes = True
            new_rules.append(new_rule)

    return has_changes


def remove_rules_with_empty_symbol(rules: List[Rule]) -> List[Rule]:
    return [rule for rule in rules if not (
            len(rule.right_part) == 1 and rule.right_part[0] == EMPTY_SYMBOL
    )]


def find_alternative_rules_without_empty_symbol(rules: List[Rule]) -> List[Rule]:
    new_rules = []
    has_changes = False

    for rule in rules:
        if len(rule.right_part) == 1 and rule.right_part[0] == EMPTY_SYMBOL:
            new_rules.append(rule)
            has_changes = add_alternative_rules_without_empty_rule(
                rules, new_rules, rule.non_terminal, has_changes
            )
        else:
            new_rules.append(rule)

    if has_changes:
        return find_alternative_rules_without_empty_symbol(new_rules)
    return new_rules


def read_grammar(input_file: TextIO) -> List[Rule]:
    rules = []
    for line in input_file:
        if "->" not in line:
            continue
        non_terminal, right_part = line.split("->", 1)
        non_terminal = non_terminal.strip()
        read_right_part(right_part.strip(), non_terminal, rules)

    rules = find_alternative_rules_without_empty_symbol(rules)
    rules = remove_rules_with_empty_symbol(rules)
    define_direction_symbols(rules)

    # Проверки грамматики
    if not is_reachable(rules):
        raise UnreachableSymbolError("Грамматика содержит недостижимые нетерминалы")

    if not is_productive(rules):
        raise UnproductiveSymbolError("Грамматика содержит непродуктивные нетерминалы")

    if not is_unambiguous(rules):
        raise AmbiguousGrammarError("Грамматика может быть неоднозначной")

    return rules