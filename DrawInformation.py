import pygame
import math

class DrawInformation:
  '''
  Class to be initialized at the beginning of the program
  Passes values to itself such as width, height, unsorted list, etc.
  Passed to all the different functions
  '''

  #Colors in RGB Representation
  BLACK = 0,0,0
  WHITE = 255,255,255
  GREEN = 0,255,0
  RED = 255,0,0
  GREY = 128,128,128
  BACKGROUND_COLOR = WHITE

  GRADIENTS = [ #gradients used for the bars in the list
    (128,128,128),
    (160,160,160),
    (192,192,192)
  ]

  FONT = pygame.font.SysFont('comicsans', 20)
  LARGE_FONT = pygame.font.SysFont('comicsans',30)

  SIDE_PAD = 100 #padding from the left and right, in pixels
  TOP_PAD = 150 #padding from the top, in pixels

  iterations = 0
  
  def __init__(self, width: int, height: int, lst: list):
    self.width = width
    self.height = height

    #create the window in pygame using width and height
    self.window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Sorting Algorithm Visualizer")

    self.set_list(lst)

  def set_list(self, lst: list):
    '''
    Sets attributes that are related to the list, so that they scale properly with the window size
    '''
    self.lst = lst
    self.min_val = min(lst)
    self.max_val = max(lst)

    #calculates width and height of each bar
    self.bar_width = round((self.width - self.SIDE_PAD) / len(lst))
    self.bar_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val)) #Increment of height per value

    self.start_x = self.SIDE_PAD // 2 #start drawing after the padding
