from dataclasses import dataclass, field
from typing import Dict, Any

type BusName = str
DATA_OUT_BUS: BusName = "DATA_OUT_BUS"
DATA_IN_BUS: BusName = "DATA_IN_BUS"
INTERNAL_BUS: BusName = "INTERNAL_BUS"
ADDR_BUS: BusName = "ADDR_BUS"
ALU_ACC: BusName = "ALU_ACC"

type ComponentName = str
ACC: ComponentName = "ACC"
IR: ComponentName = "IR"
PC: ComponentName = "PC"
ADDR_MUX: ComponentName = "ADDR_MUX"
DATA_MUX: ComponentName = "DATA_MUX"
ZERO: ComponentName = "ZERO"

type ControlLineName = str
IR_WR: ControlLineName = "IR_WR"
ACC_CTL0: ControlLineName = "ACC_CTL0"
ACC_CTL1: ControlLineName = "ACC_CTL1"
ACC_CTL2: ControlLineName = "ACC_CTL2"
PC_EN: ControlLineName = "PC_EN"
ACC_EN: ControlLineName = "ACC_EN"
DATA_SEL: ControlLineName = "DATA_SEL"
ADDR_SEL: ControlLineName = "ADDR_SEL"
RAM_EN: ControlLineName = "RAM_EN"
RAM_WR: ControlLineName = "RAM_WR"
PC_LD: ControlLineName = "PC_LD"
ZERO_FLAG: ControlLineName = "ZERO_FLAG"
NOT_ZERO_FLAG: ControlLineName = "NOT_ZERO_FLAG"
PC_INC: ControlLineName = "PC_INC"
HALT_FLAG: ControlLineName = "HALT_FLAG"
ACC_WR: ControlLineName = "ACC_WR"

@dataclass
class CPUExecutionStep:
    step_number: int
    instruction_name: str
    micro_instruction_name: str
    memory_change_snapshot: tuple[int, int]
    control_lines: Dict[ControlLineName, bool] = field(default_factory=dict)
    component_values: Dict[ComponentName, Any] = field(default_factory=dict)
    bus_values: Dict[BusName, int] = field(default_factory=dict)
