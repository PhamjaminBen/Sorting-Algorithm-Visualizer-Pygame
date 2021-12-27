import pygame
import random
import math

from pygame.key import start_text_input
pygame.init()
from DrawInformation import DrawInformation


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

  sorting_text = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | Q - Quick Sort", 1, draw_info.BLACK)
  draw_info.window.blit(sorting_text, (draw_info.width/2 - sorting_text.get_width()/2, 75))

  stats_text = draw_info.FONT.render(f"Iterations: {draw_info.iterations}", 1, draw_info.BLACK)
  draw_info.window.blit(stats_text, (10,10))

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
      draw_info.iterations += 1
      num1 = lst[j]
      num2 = lst[j+1]

      if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
        lst[j], lst[j+1] = lst[j+1],lst[j]
        draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
        yield True
  
  return lst

def insertion_sort(draw_info: DrawInformation, ascending = True):
  '''
  Algorithm for insertion sort visualization
  '''
  lst = draw_info.lst
  for i in range(1,len(lst)):
    key = lst[i]
    j = i-1

    while j >= 0 and ((key < lst[j] and ascending) or (key > lst[j] and not ascending)):
      draw_info.iterations += 1
      lst[j+1] = lst[j]
      j -= 1
    
    lst[j+1] = key
    draw_list(draw_info, {j: draw_info.RED, i: draw_info.GREEN}, True)
    yield True

  return lst


def quick_sort(draw_info: DrawInformation, ascending = True, l = None, h = None):
   # Create an auxiliary stack
    h = len(draw_info.lst)-1
    l = 0
    size = h - l + 1
    stack = [0] * (size)
 
    # initialize top of stack
    top = -1
 
    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h
 
    # Keep popping from stack while is not empty
    while top >= 0:
 
        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
 
        # Set pivot element at its correct position in
        # sorted array
        p = partition(l, h,draw_info, ascending )
        yield True
 
        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
 
        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
  
def partition(l, h, draw_info :DrawInformation, ascending = True):
    arr = draw_info.lst
    i = ( l - 1 )
    x = arr[h]
 
    for j in range(l, h):
        if   (arr[j] <= x and ascending) or (arr[j] >= x and not ascending):
 
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            draw_info.iterations += 1
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
 
    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    return (i + 1)



def selection_sort(draw_info: DrawInformation, ascending = True):
  '''
  Algorithm for selection sort visualization
  '''
  lst = draw_info.lst

  for i in range(len(lst)):
    extreme_pos = i

    for j in range(i+1,len(lst)):
      draw_info.iterations += 1
      if (lst[j] < lst[extreme_pos] and ascending) or (lst[j] > lst[extreme_pos] and not ascending):
        extreme_pos = j
      draw_list(draw_info, {j: draw_info.RED}, True)
    
    if extreme_pos != i:
      lst[i], lst[extreme_pos] = lst[extreme_pos], lst[i]
      draw_list(draw_info, {i: draw_info.GREEN, extreme_pos: draw_info.RED}, True)

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
  clock.tick(100) #maximum # of times per second loop runs
  while run:

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
        draw_info.iterations = 0
        sorting = True
        sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
      
      elif event.key == pygame.K_a and not sorting:
        ascending = True
        draw(draw_info, sorting_algo_name, ascending)
      
      elif event.key == pygame.K_d and not sorting:
        ascending = False
        draw(draw_info, sorting_algo_name, ascending)
      
      elif event.key == pygame.K_i and not sorting:
        sorting_algorithm = insertion_sort
        sorting_algo_name = "Insertion Sort"
        sorting_algorithm_generator = None
        # clock.tick(5)
        draw(draw_info, sorting_algo_name, ascending)
      
      elif event.key == pygame.K_b and not sorting:
        sorting_algorithm = bubble_sort
        sorting_algo_name = "Bubble Sort"
        sorting_algorithm_generator = None
        # clock.tick(5)
        draw(draw_info, sorting_algo_name, ascending) 

      elif event.key == pygame.K_s and not sorting:
        sorting_algorithm = selection_sort
        sorting_algo_name = "Selection Sort"     
        sorting_algorithm_generator = None
        # clock.tick(5)
        draw(draw_info, sorting_algo_name, ascending)
      
      elif event.key == pygame.K_q and not sorting:
        sorting_algorithm = quick_sort
        sorting_algo_name = "Quick Sort"
        sorting_algorithm_generator = None
        draw(draw_info, sorting_algo_name, ascending)

  
  pygame.quit() 


if __name__ == "__main__":
  main()


