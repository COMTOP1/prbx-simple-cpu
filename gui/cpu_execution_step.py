from dataclasses import dataclass, field
from typing import Dict, Any, Tuple

from gui.cpu_readout_panel import CPUReadoutType, BOOL_TYPE, BIT_1_TYPE, BITS_8_TYPE, BITS_16_TYPE

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
    micro_instruction_desc: str
    memory_write_snapshot: Dict[int, Tuple[int, int]] = field(default_factory=dict)
    # Format: { address: (new_value, old_value) }
    memory_read_snapshot: int = -1
    control_lines: list[ControlLineName] = field(default_factory=list)
    component_values: Dict[ComponentName, Tuple[str, int]] = field(default_factory=dict)
    bus_values: Dict[BusName, Tuple[str, int]] = field(default_factory=dict)

    def __init__(self, step_number: int, instruction_name: str, micro_instruction_desc: str):
        self.step_number = step_number
        self.instruction_name = instruction_name
        self.micro_instruction_desc = micro_instruction_desc
        self.control_lines = []
        self.component_values = {}
        self.memory_write_snapshot = {}
        self.memory_read_snapshot = -1
        self.bus_values = {}

    def record_bus(self, name: BusName, value: int, readout_type: CPUReadoutType):
        display = ""
        if readout_type == BOOL_TYPE:
            display = f"{bool(value)}"
        if readout_type == BIT_1_TYPE:
            display = f"{value}"
        elif readout_type == BITS_8_TYPE:
            display = f"0x{value:02X}"
        elif readout_type == BITS_16_TYPE:
            display = f"0x{value:04X}"
        self.bus_values[name] = (display, value)

    def record_component(self, name: ComponentName, value: Any, readout_type: CPUReadoutType):
        display = ""
        if readout_type == BOOL_TYPE:
            display = f"{bool(value)}"
        if readout_type == BIT_1_TYPE:
            display = f"{value}"
        elif readout_type == BITS_8_TYPE:
            display = f"0x{value:02X}"
        elif readout_type == BITS_16_TYPE:
            display = f"0x{value:04X}"
        self.component_values[name] = (display, value)

    def record_control_line(self, control_line: ControlLineName):
        self.control_lines.append(control_line)

    def record_memory_read_snapshot(self, memory_read_snapshot: int):
        self.memory_read_snapshot = memory_read_snapshot

    def record_memory_write_snapshot(self, address: int, new_value: int, old_value: int):
        self.memory_write_snapshot[address] = (new_value, old_value)
