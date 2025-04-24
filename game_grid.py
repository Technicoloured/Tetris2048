################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
import pygame # for soundplay
import time

# The main function where this program starts execution
def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + 6)
   stddraw.setCanvasSize(canvas_w, canvas_h)
   stddraw.setXscale(-0.5, grid_w + 6 - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # Initialize game state
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   grid = GameGrid(grid_h, grid_w)
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino
   grid.next_tetromino = create_tetromino()

   # Add pause state
   is_paused = False
   last_time = time.time()  # For tracking time between automatic drops

   display_game_menu(grid_h, grid_w)

   # the main game loop
   while True:
      current_time = time.time()

      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():
         key_typed = stddraw.nextKeyTyped().lower()  # make it case insensitive

         # Pause/unpause with 'p'
         if key_typed == 'p':
            is_paused = not is_paused
            grid.display()  # Refresh display to show/hide pause message
            stddraw.show(0)  # Force immediate display update

         # Restart game with 'r'
         elif key_typed == 'r':
            # Reset game state
            grid = GameGrid(grid_h, grid_w)
            current_tetromino = create_tetromino()
            grid.current_tetromino = current_tetromino
            grid.next_tetromino = create_tetromino()
            is_paused = False
            last_time = current_time
            continue

         # Only process movement keys if not paused
         if not is_paused:
            if key_typed == "left":
               current_tetromino.move(key_typed, grid)
            elif key_typed == "right":
               current_tetromino.move(key_typed, grid)
            elif key_typed == "down":
               current_tetromino.move(key_typed, grid)
            elif key_typed == "up":
               current_tetromino.rotate(grid)
            elif key_typed == "space":
               current_tetromino.hard_drop(grid)

         stddraw.clearKeysTyped()

      # Skip game logic if paused
      if is_paused:
         # Show pause message
         stddraw.setFontSize(36)
         stddraw.setPenColor(Color(180, 70, 100))
         stddraw.text(grid_w / 2, grid_h / 2, "PAUSED")
         stddraw.show(0)
         continue

      # Automatic downward movement (once per second)
      if current_time - last_time > 0.3:  # 1 second has passed
         last_time = current_time
         # move the active tetromino down by one
         success = current_tetromino.move("down", grid)

         if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            game_over = grid.update_grid(tiles, pos)

            grid.remove_full_rows()

            # end the main game loop if the game is over
            if game_over:
               # Show win/lose message
               stddraw.setFontSize(36)
               stddraw.setPenColor(Color(180, 70, 100))

               if grid.has_won:
                  stddraw.text(grid_w / 2, grid_h / 2, "YOU WIN!")
               else:
                  stddraw.text(grid_w / 2, grid_h / 2, "GAME OVER!")

               stddraw.show(3000)
               break

            # create the next tetromino to enter the game grid
            current_tetromino = grid.next_tetromino
            grid.current_tetromino = current_tetromino
            grid.next_tetromino = create_tetromino()

      grid.display()
      stddraw.show(50)  # Show for 50ms (controls game speed)

   print("Game over")

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped().lower()  # make it case insensitive

         # Pause/unpause with 'p'
         if key_typed == 'p':
            is_paused = not is_paused
            if is_paused:
               # Show pause message
               stddraw.setFontFamily("Arial")
               stddraw.setFontSize(48)
               stddraw.setPenColor(Color(255, 0, 0))
               stddraw.text(grid_w / 2, grid_h / 2, "PAUSED")
               stddraw.show(100)

         # Restart game with 'r'
         elif key_typed == 'r':
            # Reset game state
            grid = GameGrid(grid_h, grid_w)
            current_tetromino = create_tetromino()
            grid.current_tetromino = current_tetromino
            grid.next_tetromino = create_tetromino()
            is_paused = False
            continue

         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         # rotation
         elif key_typed == "up":
            current_tetromino.rotate(grid)
         # hard drop
         elif key_typed == "space":
            current_tetromino.hard_drop(grid)
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

         # Skip game logic if paused
         if is_paused:
            grid.display()
            continue

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)

         grid.remove_full_rows()

         # end the main game loop if the game is over
         if game_over:
            # Show win/lose message
            stddraw.setFontSize(36)
            stddraw.setPenColor(Color(180, 70, 100))
            
            if grid.has_won:
               stddraw.text(grid.grid_width / 2, grid.grid_height / 2, "YOU WIN!")
            else:
               stddraw.text(grid.grid_width / 2, grid.grid_height / 2, "GAME OVER!")
            
            stddraw.show(3000)
          
            break
         


         # create the next tetromino to enter the game grid
         current_tetromino = grid.next_tetromino  # Use the next tetromino
         grid.current_tetromino = current_tetromino
         grid.next_tetromino = create_tetromino()  # Create a new next tetromino

      # display the game grid with the current tetromino
      grid.display()

   # print a message on the console when the game is over
   print("Game over")

# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I','O','Z','L','J','S','T']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(255, 230, 240)  # Light pink background
   button_color = Color(255, 180, 200)  # Medium pink button
   text_color = Color(200, 80, 120)  # Dark pink text
   name_color = Color(200, 80, 120)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)

   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "START"
   stddraw.text(img_center_x, 5, text_to_display)

   # Add 3-line text on the right side of the menu
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(22)
   stddraw.setPenColor(Color(180, 70, 100))  # Slightly darker pink for contrast

   # Calculate position for the text (right side of the screen)
   text_x = grid_width + 3  # Positioned to the right of the main grid
   center_y = grid_height / 2  # Starting Y position
   line_spacing = 1.5  # Space between lines

   # The three lines of text
   line1 = "Sudenur Bilgin"
   line2 = "Melike Gürcan"
   line3 = "Pınar Günal"

   # Draw each line
   stddraw.text(text_x, center_y + line_spacing, line1)
   stddraw.text(text_x, center_y, line2)
   stddraw.text(text_x, center_y - line_spacing, line3)

   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               pygame.mixer.init()
               pygame.mixer.music.load('tetris99.mp3')
               pygame.mixer.music.set_volume(0.06)
               pygame.mixer.music.play(-1)
               break  # break the loop to end the method and start the game
# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start()
