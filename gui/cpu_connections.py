import tkinter as tk


class CPUConnections:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_connections(self):
        def line(points, colour="black", width=10):
            self.canvas.create_line(
                *points,
                fill=colour,
                width=width,
                arrow=tk.LAST,
                arrowshape=(16, 20, 6),  # (length, width, wing)
                capstyle=tk.ROUND)

        line([
            810, 150,
            810, 25,
            200, 25,
            200, 50,
            ], "deep sky blue") # Memory -> IR

        line([
            810, 150,
            810, 25,
            435, 25,
            435, 325,
        ], "deep sky blue") # Memory -> Data Mux

        line([
            625, 275,
            625, 290,
            510, 290,
            510, 340,
            550, 340
        ], "orange") # PC -> Addr Mux

        line([
            630, 385,
            750, 385,
        ], "lawn green") # Addr Mux -> Memory

        line([
            415, 375,
            415, 400,
        ], "dim grey") # Data Mux -> ALU

        line([
            200, 125,
            200, 175,
            100, 175,
            100, 300,
        ], "purple") # IR -> Control Logic

        line([
            200, 125,
            200, 175,
            390, 175,
            390, 325,
        ], "purple") # IR -> Data Mux

        line([
            200, 125,
            200, 175,
            490, 175,
            490, 430,
            550, 430
        ], "purple") # IR -> Addr Mux

        line([
            200, 125,
            200, 175,
            625, 175,
            625, 200,
        ], "purple") # IR -> PC

        line([
            350, 475,
            350, 550,
        ], "sky blue") # ALU -> ACC

        line([
            350, 625,
            350, 650,
            210, 650,
            210, 375,
            290, 375,
            290, 400,
        ], "dark blue") # ACC -> ALU

        line([
            350, 625,
            350, 650,
            600, 650,
            600, 500,
            540, 500,
            540, 550,
        ], "dark blue")  # ACC -> Zero

        line([
            350, 625,
            350, 650,
            810, 650,
            810, 550,
        ], "dark blue")  # ACC -> Memory
