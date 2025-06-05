from StaticError import *
from Symbol import *
from functools import *


def simulate(list_of_commands):
    """
    Executes a list of commands and processes them sequentially.
    
    Args:
        list_of_commands (list[str]): A list of commands to be executed.
    
    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
    
    initial_state= ([[]],0,[]) #symbol_table, current_level, result

    try:
        final_state = reduce(process_command, list_of_commands, initial_state)
        symbol_table, level, results= final_state
        if level > 0:
            raise UnclosedBlock(level)
        return results
    except StaticError as e:
        _,_, results= initial_state
        return results + [str(e)]

def process_command(state, command):
    symbol_table, level, results = state
    if (
            not command or 
           '\t' in command or
            '\n' in command or
            not all(c.isprintable() for c in command)
        ):
        raise InvalidInstruction("Invalid command")

    if command.lstrip() != command:
        raise InvalidInstruction("Invalid command")
    
    cmd_parts = command.split()
    if not cmd_parts:
        raise InvalidInstruction("Invalid command")
    
    cmd_type= cmd_parts[0]
    valid_keywords = ["INSERT", "ASSIGN", "BEGIN", "END", "LOOKUP", "PRINT", "RPRINT"]

    if cmd_type not in valid_keywords or cmd_type != cmd_type.upper():
        raise InvalidInstruction("Invalid command")
    
    if command != command.rstrip():
        raise InvalidInstruction(command)
    
    if cmd_type == "INSERT":
        return process_insert(symbol_table, level, results, command)
    elif cmd_type == "ASSIGN":
        return process_assign(symbol_table, level, results, command)
    elif cmd_type == "BEGIN":
        return process_begin(symbol_table, level, results, command)
    elif cmd_type == "END":
        return process_end(symbol_table, level, results, command)
    elif cmd_type == "LOOKUP":
        return process_lookup(symbol_table, level, results, command)
    elif cmd_type == "PRINT":
        return process_print(symbol_table, level, results, command)
    elif cmd_type == "RPRINT":
        return process_rprint(symbol_table, level, results, command)

def is_valid_spacing(command, expected_parts):
    parts = command.split(' ')
    filtered = list(filter(lambda x: x != '', parts))
    return len(filtered) == expected_parts and '  ' not in command

def is_valid_name(name):
    return (name and name[0].islower() and 
            all(c.isalpha() or c.isdigit() or c == '_' for c in name))

def is_number(value):
    return value.isdigit()

def is_string(value):
    return (len(value) >= 2 and value[0] == "'" and value[-1] == "'" and 
            all(c.isalpha() or c.isdigit() for c in value[1:-1]))

def get_type(value):
    if is_number(value):
        return "number"
    elif is_string(value):
        return "string"
    return None

def lookup_symbol(name, symbol_table, current_level):
    def search(level):
        return (
            next(((sym, level) for sym in symbol_table[level] if sym.name == name), None)
            if level >= 0 else None
        ) or (search(level - 1) if level > 0 else (None, -1))
    
    return search(current_level)
    
def process_insert(symbol_table, level, results, command):
    if not is_valid_spacing(command, 3):
        raise InvalidInstruction(command)

    cmd_parts = command.split()
    _, name, stype = cmd_parts
    
    if not is_valid_name(name):
        raise InvalidInstruction(command)
    
    if stype not in ["number", "string"]:
        raise InvalidInstruction(command)
    
    if any(sym.name == name for sym in symbol_table[level]):
        raise Redeclared(command)
    
    new_symbol = Symbol(name, stype)
    new_symbol_table = [lst.copy() for lst in symbol_table]
    new_symbol_table[level] = symbol_table[level] + [new_symbol]
    
    return new_symbol_table, level, results + ["success"]

def process_assign(symbol_table, level, results, command):
    if not is_valid_spacing(command, 3):
        raise InvalidInstruction(command)

    cmd_parts = command.split()
    
    _, name, value = cmd_parts
    
    if not is_valid_name(name):
        raise InvalidInstruction(command)
    
    target_sym, _ = lookup_symbol(name, symbol_table, level)
    if not target_sym:
        raise Undeclared(command)
    
    value_type = get_type(value)
    
    if value_type:
        if value_type != target_sym.typ:
            raise TypeMismatch(command)
    else:
        if not is_valid_name(value):
            raise InvalidInstruction(command)
        
        source_sym, _ = lookup_symbol(value, symbol_table, level)
        if not source_sym:
            raise Undeclared(command)
        
        if source_sym.typ != target_sym.typ:
            raise TypeMismatch(command)
    
    return symbol_table, level, results + ["success"]

def process_begin(symbol_table, level, results, command):
    if not is_valid_spacing(command, 1) or command != "BEGIN":
        raise InvalidInstruction(command)
    
    new_symbol_table = [lst.copy() for lst in symbol_table] + [[]]
    
    return new_symbol_table, level + 1, results

def process_end(symbol_table, level, results, command):
    if not is_valid_spacing(command, 1) or command != "END":
        raise InvalidInstruction(command)
    
    if level == 0:
        raise UnknownBlock()
    
    new_symbol_table = symbol_table[:-1]
    
    return new_symbol_table, level - 1, results

def process_lookup(symbol_table, level, results, command):
    if not is_valid_spacing(command, 2):
        raise InvalidInstruction(command)
    
    cmd_parts = command.split()
    _, name = cmd_parts
    
    if not is_valid_name(name):
        raise InvalidInstruction(command)
    
    _, sym_level = lookup_symbol(name, symbol_table, level)
    if sym_level == -1:
        raise Undeclared(command)
    
    return symbol_table, level, results + [str(sym_level)]

def process_print(symbol_table, level, results, command):
    if not is_valid_spacing(command, 1) or command != "PRINT":
        raise InvalidInstruction(command)
    
    levels = range(level + 1)
    
    all_pairs = reduce(
        lambda acc, lvl: acc + list(map(
            lambda sym_and_idx: (sym_and_idx[1].name, lvl, sym_and_idx[0]), 
            enumerate(symbol_table[lvl])
        )), 
        levels, 
        []
    )
    visible_symbols = reduce(
        lambda acc, pair: {**acc, pair[0]: (pair[1], pair[2])},
        all_pairs,
        {}
    )
    
    output = " ".join(map(
        lambda pair: f"{pair[0]}//{pair[1][0]}", 
        sorted(visible_symbols.items(), 
              key=lambda x: (x[1][0], x[1][1]))
    ))
    
    return symbol_table, level, results + [output]

def process_rprint(symbol_table, level, results, command):
    if not is_valid_spacing(command, 1) or command != "RPRINT":
        raise InvalidInstruction(command)

    levels = list(range(level, -1, -1))

    all_pairs = reduce(
        lambda acc, lvl: acc + list(map(lambda sym: (sym.name, lvl), reversed(symbol_table[lvl]))),
        levels,
        []
    )

    visible_symbols = reduce(
        lambda acc, pair: acc if pair[0] in dict(acc) else acc + [pair],
        all_pairs,
        []
    )

    output = " ".join(map(lambda p: f"{p[0]}//{p[1]}", visible_symbols))

    return symbol_table, level, results + [output]
