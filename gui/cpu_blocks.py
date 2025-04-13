import tkinter as tk

class CPUBlockDiagram:
    def __init__(self, canvas):
        self.canvas = canvas
        self.component_labels_initial = {}
        self.component_labels = {}

    def draw_block(self, name, label, x, y, initial_value="", w=200, h=75,
                   colour="blue", font_colour="white", mux=False, x0=0, y0=0, x1=0, y1=0):
        self.canvas.create_rectangle(x, y, x + w, y + h, fill=colour, width=2)

        text = label if initial_value == "" else f"{label}({initial_value})"
        label_id = self.canvas.create_text(x + w / 2, y + h / 2, text=text, font=("Arial", 18), fill=font_colour,
                                           justify=tk.CENTER)

        self.component_labels_initial[name] = label
        self.component_labels[name] = label_id

        if mux:
            self.canvas.create_text(x0, y0, text="0", font=("Arial", 11), justify=tk.CENTER, fill=font_colour)
            self.canvas.create_text(x1, y1, text="1", font=("Arial", 11), justify=tk.CENTER, fill=font_colour)

    def draw_all_blocks(self):
        self.draw_block("ACC", "Accumulator\nACC ", 250, 550, initial_value="0x00")
        self.draw_block("IR", "Instruction Register\nIR ", 90, 50, initial_value="0x0000", w=220,
                        colour="slate blue")
        self.draw_block("PC", "Program Counter\nPC ", 525, 200, initial_value="0x00",
                        colour="maroon")
        self.draw_block("ALU", "Arithmetic Logic Unit\nALU", 240, 400, colour="green", w=220)
        self.draw_block("CONTROL_LOGIC", "Control Logic\n(Lines Below)", 30, 300, w=140, h=70,
                        colour="grey")
        self.draw_block("MEMORY", "Memory\n(Right side)", 750, 150, w=140, h=400, colour="grey")
        self.draw_block("ADDR_MUX", "Address\nMux ", 550, 325, w=90, h=120,
                        colour="medium purple", mux=True, x0=555, y0=340, x1=555, y1=430, initial_value="0")
        self.draw_block("DATA_MUX", "Data\nMux ", 365, 290, w=100, h=70,
                        colour="medium purple", mux=True, x0=390, y0=295, x1=435, y1=295, initial_value="0")
        self.draw_block("ZERO", "Zero flag\n", 490, 550, initial_value="False", w=100, h=50,
                        colour="navy")

        self.draw_block("DATA_OUT_BUS", "Data Out\n", 860, 50, initial_value="0x0000", w=100, h=60,
                        colour="deep sky blue", font_colour="black")
        self.draw_block("DATA_IN_BUS", "Data In\n", 860, 600, initial_value="0x0000", w=100, h=60,
                        colour="dark blue")
        self.draw_block("INTERNAL_BUS", "Internal\n", 200, 200, initial_value="0x0000", w=100, h=60,
                        colour="purple")
        self.draw_block("ADDR_BUS", "Addr Bus\n", 645, 400, initial_value="0x00", w=100, h=60,
                        colour="lawn green", font_colour="black")
        self.draw_block("ALU_ACC", "ALU>ACC\n", 370, 485, initial_value="0x00", w=110, h=60,
                        colour="sky blue", font_colour="black")

    def update_block_value(self, values: list[tuple[str, str]]):
        i = 0
        while i < len(values):
            name, value = values[i]
            self.canvas.itemconfigure(self.component_labels[name],
                                      text=f"{self.component_labels_initial[name]}({value})")
            i += 1