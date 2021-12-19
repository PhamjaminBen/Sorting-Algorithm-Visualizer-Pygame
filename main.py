import pygame
import random
import math
pygame.init()

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


def generate_starting_list(n: int ,min_val: int, max_val: int) -> list:
  '''
  Generates a random list for the algorithm to work with
  '''
  lst = []

  for _ in range(n):
    val = random.randint(min_val, max_val)
    lst.append(val)
  
  return lst


def draw(draw_info: DrawInformation, algo_name: str, ascending: bool):
  '''
  Draws the pygame display using the info provided
  '''
  draw_info.window.fill(draw_info.BACKGROUND_COLOR)

  title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
  draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

  controls_text = draw_info.FONT.render("R- Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
  draw_info.window.blit(controls_text, (draw_info.width/2 - controls_text.get_width()/2, 45))

  sorting_text = draw_info.FONT.render("I - Insertion Sort | B - Bubble sort", 1, draw_info.BLACK)
  draw_info.window.blit(sorting_text, (draw_info.width/2 - sorting_text.get_width()/2, 75))

  draw_list(draw_info)
  pygame.display.update()


def draw_list(draw_info: DrawInformation, color_positions = {}, clear_bg = False):
  '''
  Draws the contents of the list on the pygame display
  Color_positions overrides the gradient shading of bars with custom colors
  '''
  lst = draw_info.lst

  if clear_bg: #clears the background of the list so new values can be displayed
    clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
    pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

  #drawing all of the bars
  for i, val in enumerate(lst):
    x = draw_info.start_x + i*draw_info.bar_width
    y = draw_info.height - (val-draw_info.min_val)*draw_info.bar_height

    color = draw_info.GRADIENTS[i%3] 

    if i in color_positions:
      color = color_positions[i]

    pygame.draw.rect(draw_info.window, color, (x,y, draw_info.bar_width, draw_info.height)) #draws the bar

    if clear_bg: pygame.display.update() 


def bubble_sort(draw_info: DrawInformation, ascending = True):
  '''
  Algorithm for bubble sort visualization

  '''
  lst = draw_info.lst

  for i in range(len(lst)-1):
    for j in range(len(lst)-1-i):
      num1 = lst[j]
      num2 = lst[j+1]

      if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
        lst[j], lst[j+1] = lst[j+1],lst[j]
        draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
        yield True
  
  return lst


def main():
  '''
  Main function called upon execution of the algorithm
  '''
  run = True 
  clock = pygame.time.Clock() #Regulates how quickly the main loop will run

  n = 50
  min_val = 0
  max_val = 100

  lst = generate_starting_list(n, min_val, max_val)
  draw_info = DrawInformation(800, 600, lst)
  sorting = False
  ascending = True

  sorting_algorithm = bubble_sort
  sorting_algo_name = "Bubble sort"
  sorting_algorithm_generator = None

  draw(draw_info, sorting_algo_name, ascending)
  
  #main loop constantly running
  while run:
    clock.tick(60) #maximum # of times per second loop runs

    #attempts to get the next iteration of the sorting algorithm, if error caught, then sorting is over
    if sorting:
      try:
        next(sorting_algorithm_generator)
      except StopIteration:
        sorting = False
      else:
        draw(draw_info, sorting_algo_name, ascending)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type != pygame.KEYDOWN:
        continue
      
      if event.key == pygame.K_r:
        lst = generate_starting_list(n, min_val,max_val)
        draw_info.set_list(lst)
        sorting = False
        draw(draw_info, sorting_algo_name, ascending)
      
      elif event.key == pygame.K_SPACE and sorting == False:
        sorting = True
        sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
      
      elif event.key == pygame.K_a and not sorting:
        ascending = True
        draw(draw_info, sorting_algo_name, ascending)
      
      elif event.key == pygame.K_d and not sorting:
        ascending = False
        draw(draw_info, sorting_algo_name, ascending)

  
  pygame.quit() 


if __name__ == "__main__":
  main()


