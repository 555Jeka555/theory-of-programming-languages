import sys
from lab6.main import task
from grammar_utils import parse_grammar, parse_grammar_with_first_set, write_grammar, Grammar
from src.grammar import factorize_grammar, remove_direct_recursion, remove_indirect_recursion, remove_unreachable_rules, \
    calculate_directing_sets


def task1() -> None:
    with open("../new-grammar.txt", "r", encoding="utf-8") as f:
        grammar = parse_grammar_with_first_set(f.readlines())

    print(grammar)


def task3() -> tuple[Grammar, str]:
    with open("../grammar.txt", "r", encoding="utf-8") as f:
        grammar, axiom_nonterminal = parse_grammar(f.readlines())

    grammar = factorize_grammar(grammar)

    grammar = remove_indirect_recursion(grammar)

    grammar = remove_direct_recursion(grammar)

    grammar = remove_unreachable_rules(grammar, axiom_nonterminal)

    axiom = grammar.rules[axiom_nonterminal]

    needs_new_axiom = False
    if len(axiom.productions) > 1:
        needs_new_axiom = True
    elif axiom.productions and (axiom.nonterminal in axiom.productions[0].symbols or (
            axiom.productions[0].symbols and axiom.productions[0].symbols[-1].startswith('<') and
            axiom.productions[0].symbols[-1].endswith('>'))):
        needs_new_axiom = True

    if needs_new_axiom:
        grammar.add_production("<axiom>", [axiom_nonterminal, "END"], [])
        axiom_nonterminal = "<axiom>"

    grammar = calculate_directing_sets(grammar, axiom_nonterminal)

    write_grammar(grammar, axiom_nonterminal)

    return grammar, axiom_nonterminal


def task4() -> None:
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <input-file>')
        return

    input_file = sys.argv[1]

    tokens = task(input_file)
    line = " ".join(token.type for token in tokens)

    task3()
    task1()


if __name__ == "__main__":
    task4()
