import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import random

# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and font size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self):
      # set the number on this tile
      self.number = random.choice([2, 4])
      # set the colors of this tile
      if self.number == 2:
         self.background_color = Color(255, 209, 220)
         self.foreground_color = Color(231, 84, 128)
         self.box_color = Color(231, 84, 128)
      elif self.number == 4:
         self.background_color = Color(255, 182, 193)  # blush pink
         self.foreground_color = Color(200, 80, 120)
         self.box_color = Color(200, 80, 120)
         self.set_color_by_number()

   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1):  # length defaults to 1
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))

   def set_color_by_number(self):
      if self.number == 2:
         self.background_color = Color(244, 217, 208)  # F4D9D0 - soft blush
         self.foreground_color = Color(146, 26, 64)  # 921A40 - deep wine
         self.box_color = Color(146, 26, 64)

      elif self.number == 4:
         self.background_color = Color(247, 200, 192)  # D9ABAB - pink beige
         self.foreground_color = Color(146, 26, 64)
         self.box_color = Color(146, 26, 64)

      elif self.number == 8:
         self.background_color = Color(199, 91, 122)  # C75B7A - rose
         self.foreground_color = Color(110, 20, 40)
         self.box_color = Color(110, 20, 40)

      elif self.number == 16:
         self.background_color = Color(146, 26, 64)  # 921A40 - deep wine
         self.foreground_color = Color(244, 217, 208)
         self.box_color = Color(244, 217, 208)

      elif self.number == 32:
         self.background_color = Color(110, 20, 50)  # deeper burgundy
         self.foreground_color = Color(244, 217, 208)
         self.box_color = Color(244, 217, 208)

      elif self.number == 64:
         self.background_color = Color(90, 15, 40)  # rich plum-brown
         self.foreground_color = Color(217, 171, 171)
         self.box_color = Color(217, 171, 171)

      elif self.number == 128:
         self.background_color = Color(70, 10, 30)  # dark red-brown
         self.foreground_color = Color(199, 91, 122)
         self.box_color = Color(199, 91, 122)

      elif self.number == 256:
         self.background_color = Color(50, 5, 20)  # near black-cherry
         self.foreground_color = Color(217, 171, 171)
         self.box_color = Color(217, 171, 171)

      elif self.number == 512:
         self.background_color = Color(30, 0, 10)  # very dark wine
         self.foreground_color = Color(244, 217, 208)
         self.box_color = Color(244, 217, 208)

      elif self.number == 1024:
         self.background_color = Color(20, 0, 0)  # deep red-black
         self.foreground_color = Color(255, 255, 255)  # white
         self.box_color = Color(255, 255, 255)

      elif self.number == 2048:
         self.background_color = Color(10, 0, 0)  # ultra-dark brown
         self.foreground_color = Color(255, 255, 255)
         self.box_color = Color(255, 255, 255)
