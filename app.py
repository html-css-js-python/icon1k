import tkinter as tk
from tkinter import ttk

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
        **kwargs
    ):
        self.grid_width = width
        self.grid_height = height
        self.cell_size = cell_size
        self.margin = margin

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

        self.bind("<Button-1>", self.draw_black)
        self.bind("<B1-Motion>", self.draw_black)
        self.bind("<Button-3>", self.draw_green)
        self.bind("<B3-Motion>", self.draw_green)

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
                    fill="dark green",
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

    def draw_black(self, event):
        cell = self.get_cell(event)

        if cell is None:
            return

        x, y = cell
        self.matrix[y][x] = 1
        self.update_pixel(x, y)

    def draw_green(self, event):
        cell = self.get_cell(event)

        if cell is None:
            return

        x, y = cell
        self.matrix[y][x] = 0
        self.update_pixel(x, y)

    def update_pixel(self, x, y):
        color = "black" if self.matrix[y][x] else "dark green"
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
    def __init__(self):
        super().__init__()

        self.geometry("880x480")
        self.title("ICON1K")

    def ui(self):
        grid = PixelGrid(
            self,
            width=128,
            height=64,
            cell_size=5,
            margin=0.5
        )

        grid.pack()

if __name__ == "__main__":
    app = App()
    app.ui()
    app.mainloop()