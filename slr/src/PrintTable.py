from typing import List, Set, TextIO
from Table import Table, TableStr
from Symbol import Symbol


def print_names_of_columns(table: Table, output: TextIO) -> None:
    output.write("\t")
    for s in table.symbols:
        output.write(f"'{s}'\t")
    output.write("\n")


def print_symbols(symbols: List[Symbol], output: TextIO) -> None:
    for i, symbol in enumerate(symbols):
        output.write(f"'{symbol}'")
        if i + 1 != len(symbols):
            output.write(", ")
    output.write("\t")


def print_next_symbols(table_str: TableStr, symbols: Set[str], output: TextIO) -> None:
    for s in symbols:
        if s not in table_str.next_symbols:
            output.write("\t")
        else:
            print_symbols(table_str.next_symbols[s], output)


def print_table(table: Table, output: TextIO) -> None:
    print_names_of_columns(table, output)
    for table_str in table.strings:
        print_symbols(table_str.symbols, output)
        print_next_symbols(table_str, table.symbols, output)
        output.write("\n")
