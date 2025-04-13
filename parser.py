import re

def __raw_parser(raw_asm: str) -> list[str]:
    stripped = (raw_asm + '\n').strip()
    stripped = re.sub('\t+', '\n', stripped)
    stripped = re.sub(';.*', '', stripped)
    stripped = re.sub(' {2,}', ' ', stripped)
    stripped = re.sub('\n +', '\n', stripped)
    stripped = re.sub(' +\n', '\n', stripped)
    stripped = re.sub('\n{2,}', '\n', stripped)
    return stripped.upper().strip().split('\n')

def parser(raw_asm: str) -> (list[str], list[int]):
    returning_memory: list[int] = []
    parsed_list = __raw_parser(raw_asm)
    for instruction in parsed_list:
        memory_value: int
        split_instruction = instruction.split(' ')
        if split_instruction[0] == "MOVE":
            if len(split_instruction) != 2:
                raise ValueError("MOVE instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("MOVE instruction must be between 0 and 255")
            memory_value = 0x0000 + value
        elif split_instruction[0] == "ADD":
            if len(split_instruction) != 2:
                raise ValueError("ADD instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("ADD instruction must be between 0 and 255")
            memory_value = 0x1000 + value
        elif split_instruction[0] == "SUB":
            if len(split_instruction) != 2:
                raise ValueError("SUB instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("SUB instruction must be between 0 and 255")
            memory_value = 0x2000 + value
        elif split_instruction[0] == "AND":
            if len(split_instruction) != 2:
                raise ValueError("AND instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("AND instruction must be between 0 and 255")
            memory_value = 0x3000 + value
        elif split_instruction[0] == "LOAD":
            if len(split_instruction) != 2:
                raise ValueError("LOAD instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("LOAD instruction must be between 0 and 255")
            memory_value = 0x4000 + value
        elif split_instruction[0] == "STORE":
            if len(split_instruction) != 2:
                raise ValueError("STORE instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("STORE instruction must be between 0 and 255")
            memory_value = 0x5000 + value
        elif split_instruction[0] == "ADDM":
            if len(split_instruction) != 2:
                raise ValueError("ADMM instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("ADDM instruction must be between 0 and 255")
            memory_value = 0x6000 + value
        elif split_instruction[0] == "SUBM":
            if len(split_instruction) != 2:
                raise ValueError("SUBM instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("SUBM instruction must be between 0 and 255")
            memory_value = 0x7000 + value
        elif split_instruction[0] == "JUMPU":
            if len(split_instruction) != 2:
                raise ValueError("JUMPU instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("JUMPU instruction must be between 0 and 255")
            memory_value = 0x8000 + value
        elif split_instruction[0] == "JUMPZ":
            if len(split_instruction) != 2:
                raise ValueError("JUMPZ instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("JUMPZ instruction must be between 0 and 255")
            memory_value = 0x9000 + value
        elif split_instruction[0] == "JUMPNZ":
            if len(split_instruction) != 2:
                raise ValueError("JUMPNZ instruction must have 2 arguments")
            value = int(split_instruction[1])
            if value < 0 or value > 255:
                raise ValueError("JUMPNZ instruction must be between 0 and 255")
            memory_value = 0xA000 + value
        elif split_instruction[0] == "HALT":
            if len(split_instruction) != 1:
                raise ValueError("HALT instruction must have 1 arguments")
            memory_value = 0xF000
        else:
            raise ValueError(f"Unsupported instruction: {split_instruction}")
        returning_memory.append(memory_value)
    return parsed_list, returning_memory
