from typing import List, Set, TextIO
from Rule import Rule, get_rules_with_nonterminal, EMPTY_SYMBOL
from GetDirectionSymbols import define_direction_symbols
from io import TextIOBase


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

    return rules
