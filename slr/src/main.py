import sys
from typing import Optional, NamedTuple
from ReadGrammar import read_grammar
from CreateTable import create_table
from PrintTable import print_table


class Args(NamedTuple):
    input_file_name: str
    output_file_name: str


def parse_args() -> Optional[Args]:
    if len(sys.argv) != 3:
        print("Invalid quantity of arguments")
        print("Usage: python main.py <input_file> <output_file>")
        return None

    return Args(input_file_name=sys.argv[1], output_file_name=sys.argv[2])


def main() -> int:
    args = parse_args()
    if args is None:
        return 1

    try:
        with open(args.input_file_name, 'r') as input_file:
            grammar = read_grammar(input_file)
    except IOError:
        print(f"Input file is not found: {args.input_file_name}")
        return 1

    # Вывод информации о грамматике
    for rule in grammar:
        print(f"{rule.non_terminal} -> ", end="")
        print(" ".join(rule.right_part), end="")
        print(" / ", end="")
        for s in rule.direction_symbols:
            print(s.name, end="")
            if s.num_of_rule is not None:
                print(s.num_of_rule + 1, end="")
            if s.num_of_right_part is not None:
                print(s.num_of_right_part + 1, end="")
            print(" | ", end="")
        print()

    try:
        with open(args.output_file_name, 'w') as output_file:
            table = create_table(grammar)
            print_table(table, output_file)
    except IOError:
        print(f"Output file is not found: {args.output_file_name}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())