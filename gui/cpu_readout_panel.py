import tkinter as tk

type readoutType = int
BOOL_TYPE: readoutType = 0
BITS_8_TYPE: readoutType = 1
BITS_16_TYPE: readoutType = 2

class CPUReadout(tk.Frame):
    def __init__(self, master, labels: list[tuple[str, readoutType]], *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.fields = {}

        i = 0
        while i < len(labels):
            label, readout = labels[i]
            tk.Label(self, text=label + ":", font=("Courier", 12, "bold")).grid(row=0, column=i * 2, sticky="e",
                                                                                padx=(5, 0))
            text = "0x00"
            if readout == BOOL_TYPE:
                text = "False"
            elif readout == BITS_8_TYPE:
                text = "0x00"
            elif readout == BITS_16_TYPE:
                text = "0x0000"
            val = tk.Label(self, text=text, width=6, anchor="w", font=("Courier", 12))
            val.grid(row=0, column=i * 2 + 1, sticky="w", padx=(0, 10))
            self.fields[label] = val
            i += 1

    def update_values(self, data: list[tuple[str, int, readoutType]]):
        i = 0
        while i < len(data):
            label, value, readout = data[i]
            display = ""
            if readout == BOOL_TYPE:
                display = f"{bool(value)}"
            elif readout == BITS_8_TYPE:
                display = f"0x{value:02X}"
            elif readout == BITS_16_TYPE:
                display = f"0x{value:04X}"
            self.fields[label].config(text=display)
            i += 1