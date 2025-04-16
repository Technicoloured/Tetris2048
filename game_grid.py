from operator import truediv

import pygame # for soundplay

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
        self.next_tetromino = None  # Add next tetromino storage
        self.game_over = False
        self.empty_cell_color = Color(255, 240, 245)
        self.line_color = Color(255, 220, 230)
        self.boundary_color = Color(220, 120, 150)
        self.line_thickness = 0.002
        self.box_thickness = 0.008
        self.grid_pattern = True
        self.pattern_color = Color(255, 230, 238)
        self.sidebar_width = 6  # Width of the sidebar area

    def display(self):
        # Clear with empty cell color for both grid and sidebar
        stddraw.clear(self.empty_cell_color)
        self.draw_grid()
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        self.draw_next_tetromino()
        self.draw_boundaries()

        # Draw sidebar boundary
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        stddraw.line(self.grid_width - 0.5, -0.5,
                     self.grid_width - 0.5, self.grid_height - 0.5)
        stddraw.setPenRadius()

        stddraw.show(250)

    def draw_next_tetromino(self):
        if self.next_tetromino is not None:
            # Draw "Next:" label
            stddraw.setPenColor(Color(231, 84, 128))
            stddraw.setFontFamily("Arial")
            stddraw.setFontSize(16)
            stddraw.text(self.grid_width + self.sidebar_width / 2,
                         self.grid_height - 2, "Next Piece")

            # Save original position
            original_pos = cp.copy(self.next_tetromino.bottom_left_cell)

            # Calculate preview position (centered in sidebar)
            preview_size = len(self.next_tetromino.tile_matrix)
            self.next_tetromino.bottom_left_cell.x = self.grid_width + (self.sidebar_width - preview_size) / 2
            self.next_tetromino.bottom_left_cell.y = self.grid_height - 5

            # Draw the next tetromino
            for row in range(preview_size):
                for col in range(preview_size):
                    if self.next_tetromino.tile_matrix[row][col] is not None:
                        position = self.next_tetromino.get_cell_position(row, col)
                        self.next_tetromino.tile_matrix[row][col].draw(position, 0.8)  # Smaller size

            # Restore original position
            self.next_tetromino.bottom_left_cell = original_pos


    def draw_grid(self):
        if self.grid_pattern:
            stddraw.setPenColor(self.pattern_color)
            cell_size = 1.0
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    if (x + y) % 2 == 0:
                        stddraw.filledSquare(x, y, cell_size / 2)

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))

        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()

    def draw_boundaries(self):
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        stddraw.rectangle(-0.5, -0.5, self.grid_width, self.grid_height)
        stddraw.setPenRadius()

    def is_occupied(self, row, col):
        if not self.is_inside(row, col):
            return False
        return self.tile_matrix[row][col] is not None

    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    def is_full(self, row):
        for col in range(self.grid_width):
            if self.tile_matrix[row][col] is None:
                return False
        return True

    def remove_full_rows(self):
        row = self.grid_height - 1
        rows_cleared = [] #for the animation
        while row >= 0:
            if self.is_full(row):
                rows_cleared.append(row)
                for r in range(row, self.grid_height - 1):
                    self.tile_matrix[r] = self.tile_matrix[r + 1].copy()
                self.tile_matrix[self.grid_height - 1] = np.full(self.grid_width, None)
            else:
                row -= 1

        #if any rows were cleared, show the animation
        if rows_cleared:
            sound_effect = pygame.mixer.Sound('bubblepop.mp3')
            sound_effect.set_volume(0.2)
            sound_effect.play()
            self.animate_row_clear(rows_cleared)
        return len(rows_cleared)

    def animate_row_clear(self, rows):
        # Number of animation frames
        frames = 6

        for frame in range(frames):
            # Flash effect - alternate between white and original colors
            for row in rows:
                for col in range(self.grid_width):
                    if self.tile_matrix[row][col] is not None:
                        # Alternate between white and original color
                        if frame % 2 == 0:
                            # Save original colors if first frame
                            if frame == 0:
                                self.tile_matrix[row][col].original_bg = self.tile_matrix[row][col].background_color
                                self.tile_matrix[row][col].original_fg = self.tile_matrix[row][col].foreground_color
                                self.tile_matrix[row][col].original_box = self.tile_matrix[row][col].box_color

                            # Set to white
                            self.tile_matrix[row][col].background_color = Color(255, 255, 255)
                            self.tile_matrix[row][col].foreground_color = Color(255, 255, 255)
                            self.tile_matrix[row][col].box_color = Color(255, 255, 255)
                        else:
                            # Restore original colors
                            self.tile_matrix[row][col].background_color = self.tile_matrix[row][col].original_bg
                            self.tile_matrix[row][col].foreground_color = self.tile_matrix[row][col].original_fg
                            self.tile_matrix[row][col].box_color = self.tile_matrix[row][col].original_box

            # Display the animation frame
            self.display()
            stddraw.show(50)  # Show each frame for 50ms

    def update_grid(self, tiles_to_lock, blc_position):
        self.current_tetromino = None
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])

        for col in range(n_cols):
            for row in range(n_rows):
                if tiles_to_lock[row][col] is not None:
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    else:
                        self.game_over = True

        self.remove_full_rows()
        return self.game_over
