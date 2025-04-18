import tkinter as tk

type CPUReadoutType = int
BOOL_TYPE: CPUReadoutType = 0
BIT_1_TYPE: CPUReadoutType = 1
BITS_8_TYPE: CPUReadoutType = 2
BITS_16_TYPE: CPUReadoutType = 3

class CPUReadout(tk.Frame):
    def __init__(self, master, labels: list[tuple[str, CPUReadoutType]], *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.fields = {}

        i = 0
        while i < len(labels):
            label, readout = labels[i]
            tk.Label(self, text=label + ":", font=("Courier", 10, "bold")).grid(row=0, column=i * 2, sticky="e",
                                                                                padx=(5, 0))
            text = "0x00"
            if readout == BOOL_TYPE:
                text = "False"
            elif readout == BIT_1_TYPE:
                text = "0"
            elif readout == BITS_8_TYPE:
                text = "0x00"
            elif readout == BITS_16_TYPE:
                text = "0x0000"
            val = tk.Label(self, text=text, width=6, anchor="w", font=("Courier", 11))
            val.grid(row=0, column=i * 2 + 1, sticky="w", padx=(0, 5))
            self.fields[label] = val
            i += 1

    def update_values(self, data: list[tuple[str, int, CPUReadoutType]]):
        i = 0
        while i < len(data):
            label, value, readout = data[i]
            display = ""
            if readout == BOOL_TYPE:
                display = f"{bool(value)}"
            if readout == BIT_1_TYPE:
                display = f"{value}"
            elif readout == BITS_8_TYPE:
                display = f"0x{value:02X}"
            elif readout == BITS_16_TYPE:
                display = f"0x{value:04X}"
            self.fields[label].config(text=display)
            i += 1

    def update_values_formatted(self, data: list[tuple[str, str]]):
        i = 0
        while i < len(data):
            label, value = data[i]
            self.fields[label].config(text=value)
            i += 1
