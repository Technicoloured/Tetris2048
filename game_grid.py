from operator import truediv
import pygame
import lib.stddraw as stddraw
from lib.color import Color
from point import Point
import numpy as np
import copy as cp

class GameGrid:
    def __init__(self, grid_h, grid_w):
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.tile_matrix = np.full((grid_h, grid_w), None)
        self.current_tetromino = None
        self.next_tetromino = None
        self.game_over = False
        self.has_won = False
        self.empty_cell_color = Color(255, 240, 245)
        self.line_color = Color(255, 220, 230)
        self.boundary_color = Color(220, 120, 150)
        self.line_thickness = 0.002
        self.box_thickness = 0.008
        self.grid_pattern = True
        self.pattern_color = Color(255, 230, 238)
        self.sidebar_width = 6
        self.score = 0

    def display(self):
        stddraw.clear(self.empty_cell_color)
        self.draw_grid()
        if self.current_tetromino:
            self.current_tetromino.draw()
        self.draw_next_tetromino()

        # Score text
        stddraw.setPenColor(Color(231, 84, 128))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(16)
        stddraw.text(self.grid_width + self.sidebar_width / 2, self.grid_height - 7, "Score")
        stddraw.setFontSize(24)
        stddraw.text(self.grid_width + self.sidebar_width / 2, self.grid_height - 8.5, str(self.score))

        # Add instructions
        stddraw.setFontSize(12)
        stddraw.setPenColor(Color(150, 150, 150))
        stddraw.text(self.grid_width + self.sidebar_width / 2, 2, "P: Pause")
        stddraw.text(self.grid_width + self.sidebar_width / 2, 1, "R: Restart")

        self.draw_boundaries()

        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        stddraw.line(self.grid_width - 0.5, -0.5, self.grid_width - 0.5, self.grid_height - 0.5)
        stddraw.setPenRadius()
        stddraw.show(400)

    def draw_next_tetromino(self):
        if self.next_tetromino is not None:
            stddraw.setPenColor(Color(231, 84, 128))
            stddraw.setFontFamily("Arial")
            stddraw.setFontSize(16)
            stddraw.text(self.grid_width + self.sidebar_width / 2, self.grid_height - 2, "Next Piece")

            original_pos = cp.copy(self.next_tetromino.bottom_left_cell)

            preview_size = len(self.next_tetromino.tile_matrix)
            self.next_tetromino.bottom_left_cell.x = self.grid_width + (self.sidebar_width - preview_size) / 2
            self.next_tetromino.bottom_left_cell.y = self.grid_height - 5

            for row in range(preview_size):
                for col in range(preview_size):
                    if self.next_tetromino.tile_matrix[row][col] is not None:
                        pos = self.next_tetromino.get_cell_position(row, col)
                        self.next_tetromino.tile_matrix[row][col].draw(pos, 0.8)

            self.next_tetromino.bottom_left_cell = original_pos

    def draw_grid(self):
        if self.grid_pattern:
            stddraw.setPenColor(self.pattern_color)
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    if (x + y) % 2 == 0:
                        stddraw.filledSquare(x, y, 0.5)

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))

        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        for x in range(1, self.grid_width):
            stddraw.line(x - 0.5, -0.5, x - 0.5, self.grid_height - 0.5)
        for y in range(1, self.grid_height):
            stddraw.line(-0.5, y - 0.5, self.grid_width - 0.5, y - 0.5)
        stddraw.setPenRadius()

    def draw_boundaries(self):
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        stddraw.rectangle(-0.5, -0.5, self.grid_width, self.grid_height)
        stddraw.setPenRadius()

    def is_occupied(self, row, col):
        return self.is_inside(row, col) and self.tile_matrix[row][col] is not None

    def is_inside(self, row, col):
        return 0 <= row < self.grid_height and 0 <= col < self.grid_width

    def is_full(self, row):
        return all(self.tile_matrix[row][col] is not None for col in range(self.grid_width))

    def remove_full_rows(self):
        row = self.grid_height - 1
        cleared_rows = []
        while row >= 0:
            if self.is_full(row):
                row_score = sum(tile.number for tile in self.tile_matrix[row] if tile is not None)
                self.score += row_score
                cleared_rows.append(row)

                for r in range(row, self.grid_height - 1):
                    self.tile_matrix[r] = self.tile_matrix[r + 1].copy()
                self.tile_matrix[self.grid_height - 1] = np.full(self.grid_width, None)
            else:
                row -= 1

        if cleared_rows:
            try:
                sound_effect = pygame.mixer.Sound('bubblepop.mp3')
                sound_effect.set_volume(0.2)
                sound_effect.play()
            except:
                pass  # Fail silently if sound can't play
            self.animate_row_clear(cleared_rows)
        return len(cleared_rows)

    def animate_row_clear(self, rows):
        frames = 6
        for frame in range(frames):
            for row in rows:
                for col in range(self.grid_width):
                    tile = self.tile_matrix[row][col]
                    if tile:
                        if frame % 2 == 0:
                            if frame == 0:
                                tile.original_bg = tile.background_color
                                tile.original_fg = tile.foreground_color
                                tile.original_box = tile.box_color
                            tile.background_color = Color(255, 255, 255)
                            tile.foreground_color = Color(255, 255, 255)
                            tile.box_color = Color(255, 255, 255)
                        else:
                            tile.background_color = tile.original_bg
                            tile.foreground_color = tile.original_fg
                            tile.box_color = tile.original_box
            self.display()
            stddraw.show(50)

    def update_grid(self, tiles_to_lock, blc_position):
        self.current_tetromino = None
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])

        for row in range(n_rows):
            for col in range(n_cols):
                tile = tiles_to_lock[row][col]
                if tile:
                    x = blc_position.x + col
                    y = blc_position.y + (n_rows - 1 - row)
                    if self.is_inside(y, x):
                        self.tile_matrix[y][x] = tile
                    else:
                        self.game_over = True

        self.merge_vertical_tiles()
        self.handle_free_tiles()
        self.remove_full_rows()
        return self.game_over

    def merge_vertical_tiles(self):
        merged = True
        while merged:
            merged = False
            for col in range(self.grid_width):
                row = 0
                while row < self.grid_height - 1:
                    current = self.tile_matrix[row][col]
                    above = self.tile_matrix[row + 1][col]

                    if current is not None and above is not None:
                        if current.number == above.number:
                            # Merge logic
                            current.number *= 2
                            current.set_color_by_number()  #  update color
                            self.score += current.number
                            self.tile_matrix[row + 1][col] = None
                            merged = True

                            # Check for win
                            if current.number == 2048:
                                self.game_over = True
                                self.has_won = True
                                print("YOU WIN!")

                            # Skip next row to avoid double merge in same pass
                            row += 2
                            continue
                    row += 1
            if merged:
                self.apply_gravity()


    def apply_gravity(self):
        for col in range(self.grid_width):
            stack = [tile for tile in self.tile_matrix[:, col] if tile is not None]
            stack += [None] * (self.grid_height - len(stack))
            for row in range(self.grid_height):
                self.tile_matrix[row][col] = stack[row]

    def handle_free_tiles(self):
        visited = set()

        def dfs(row, col):
            if (row, col) in visited:
                return
            visited.add((row, col))
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = row + dr, col + dc
                if self.is_inside(nr, nc) and self.tile_matrix[nr][nc]:
                    dfs(nr, nc)

        for col in range(self.grid_width):
            if self.tile_matrix[0][col]:
                dfs(0, col)

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] and (row, col) not in visited:
                    self.score += self.tile_matrix[row][col].number
                    self.tile_matrix[row][col] = None
