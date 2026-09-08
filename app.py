from enum import IntEnum
import argparse
import tkinter as tk
from tkinter import ttk

# ERROR CODES
# 0 = No error
# 1 = Size error (too big)
# 2 = Size error (too small)
# 3 = Size error (not divisible by 8)

class ErrorCode(IntEnum):
    SIZE_TOO_BIG = 1
    SIZE_TOO_SMALL = 2
    SIZE_DIVISIBILITY = 3


def matrix_to_bytes(matrix, width, height):
    if len(matrix) != height:
        raise ValueError("Matrix height does not match height")

    if any(len(row) != width for row in matrix):
        raise ValueError("Matrix width does not match width")

    if height % 8 != 0:
        raise ValueError("Height must be divisible by 8")

    result = []

    for block_y in range(0, height, 8):
        for x in range(width):
            byte = 0

            for bit in range(8):
                if matrix[block_y + bit][x]:
                    byte |= 1 << bit

            result.append(byte)

    return result

class PixelGrid(tk.Canvas):
    def __init__(
        self,
        parent,
        width,
        height,
        cell_size=20,
        margin=2,
        high="black",
        low="dark green",
        **kwargs
    ):
        self.grid_width = width
        self.grid_height = height
        self.cell_size = cell_size
        self.margin = margin
        self.high = high
        self.low = low

        self.matrix = [
            [0 for _ in range(width)]
            for _ in range(height)
        ]

        super().__init__(
            parent,
            width=width * cell_size,
            height=height * cell_size,
            highlightthickness=0,
            **kwargs
        )

        self.rectangles = []
        self.draw_grid()

        self.bind("<Button-1>", self.draw_high)
        self.bind("<B1-Motion>", self.draw_high)
        self.bind("<Button-3>", self.draw_low)
        self.bind("<B3-Motion>", self.draw_low)

    def draw_grid(self):
        for y in range(self.grid_height):
            row = []

            for x in range(self.grid_width):
                x1 = x * self.cell_size + self.margin
                y1 = y * self.cell_size + self.margin
                x2 = (x + 1) * self.cell_size - self.margin
                y2 = (y + 1) * self.cell_size - self.margin

                rect = self.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self.low,
                    outline=""
                )

                row.append(rect)

            self.rectangles.append(row)

    def get_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if not (0 <= x < self.grid_width and 0 <= y < self.grid_height):
            return None

        return x, y

    def draw_high(self, event):
        cell = self.get_cell(event)

        if cell is None:
            return

        x, y = cell
        self.matrix[y][x] = 1
        self.update_pixel(x, y)

    def draw_low(self, event):
        cell = self.get_cell(event)

        if cell is None:
            return

        x, y = cell
        self.matrix[y][x] = 0
        self.update_pixel(x, y)

    def update_pixel(self, x, y):
        color = self.high if self.matrix[y][x] else self.low
        self.itemconfig(self.rectangles[y][x], fill=color)

    def get(self):
        result = []

        for block_y in range(0, self.grid_height, 8):
            for x in range(self.grid_width):
                byte = 0

                for bit in range(8):
                    if self.matrix[block_y + bit][x]:
                        byte |= 1 << bit

                result.append(byte)

        return result

    def clear(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.matrix[y][x] = 0
                self.update_pixel(x, y)



class App(tk.Tk):
    def __init__(self, args):
        super().__init__()

        self.args = args

        self.geometry("1300x695")
        self.title("ICON1K")
        self.resizable(False, False)

    def popup_export(self):
        top = tk.Toplevel(self)
        top.geometry("300x280")
        top.title("Export...")
        top.resizable(False, False)

        top.transient(self)
        top.grab_set()

        text_size = ttk.Label(top, text=f"WIDTH: {self.args.width}\nHEIGHT: {self.args.height}")
        text_size.pack(anchor="nw", padx=(5, 0), pady=(5, 0))

    def ui(self):
        grid = PixelGrid(
            self,
            width=self.args.width,
            height=self.args.height,
            cell_size=10,
            margin=0.5,
            high="white" if self.args.invert else "black",
            low="blue" if self.args.invert else "green"
        )
        grid.pack(pady=(10, 0))

        frame_btns = ttk.Frame(self)

        btn_export = ttk.Button(frame_btns, text="Export...", command=self.popup_export)
        btn_export.pack(side="right", anchor="se", padx=(0, 10), pady=(0, 10))

        btn_clear = ttk.Button(frame_btns, text="Clear", command=grid.clear)
        btn_clear.pack(side="right", anchor="sw", padx=(0, 5), pady=(0, 10))

        frame_btns.pack(side="bottom", fill="x")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int, help="width of image")
    parser.add_argument("height", type=int, help="height of image, must be divisible by 8")
    parser.add_argument("--invert", action="store_true", help="enable invert-style lcd matrix")

    args = parser.parse_args()

    if args.width > 128 or args.height > 64:
        print("Error: Image size cannot be larger than 128x64.")
        exit(ErrorCode.SIZE_TOO_BIG)

    if args.width < 8 or args.height < 8:
        print("Error: Image size cannot be smaller than 8x8.")
        exit(ErrorCode.SIZE_TOO_SMALL)

    if args.height % 8 != 0:
        print("Error: Height must be divisible by 8.")
        exit(ErrorCode.SIZE_DIVISIBILITY)

    app = App(args)
    app.ui()
    app.mainloop()