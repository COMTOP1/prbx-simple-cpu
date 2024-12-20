import re

def raw_parser(raw_asm: str):
    stripped = (raw_asm + '\n').strip()
    trimmed1 = re.sub('\t+', '\n', stripped)
    trimmed2 = re.sub(' {2,}', ' ', trimmed1)
    trimmed3 = re.sub('\n ', '\n', trimmed2)
    trimmed4 = re.sub('\s{2,}', ' ', trimmed3)
    return trimmed4.upper().strip().split('\n')
