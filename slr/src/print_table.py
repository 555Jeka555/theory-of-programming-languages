from src.table import Table, Symbol, Line


def print_table(table: Table):
    print_names_of_columns(table)

    for line in table.lines:
        print_symbols(line.symbols)
        print_next_symbol(line, table.symbols)


def print_names_of_columns(table: Table):
    for symbol in table.symbols:
        print(symbol + "\t")
    print()


def print_symbols(symbols: list[Symbol]):
    for symbol in symbols:
        print(symbol.name + "\t")
    print()


def print_next_symbol(line: Line, symbols: list):
    for symbol in symbols:
        if symbol not in line.next_symbols:
            print("\t")
        else:
            print_symbols(line.next_symbols[symbol])
