# Setting up the Game & Importing Modules
import pygame
import requests
import copy
pygame.font.init()

# All the Variables Used
WIDTH = 600
HEIGHT = 650
background_colour = (251, 247, 245)
BLACK = (0,0,0) # Defined Black Colour
number_colour = (50, 35, 150)
buffer = 5

num_font = pygame.font.SysFont('comicsansms', 35)

resp = requests.get('http://sugoku.herokuapp.com/board?difficulty=easy') # sudoku api
grid = resp.json()['board']
grid_orig = copy.deepcopy(grid)




# As the Name suggests, A function that draws the board
def draw_grid(win):
    for x in range(0,10):
        if (x % 3 == 0):
            pygame.draw.line(win, BLACK, (55 + 55*x, 55),(55 + 55*x, 550), 4) # For the 9*9 Sub Boxes
            pygame.draw.line(win, BLACK, (55, 55*x + 55),(550, 55*x + 55), 4)
    
        pygame.draw.line(win, BLACK, (55 + 55*x, 55),(55 + 55*x, 550), 2) # For the Grid Outlet
        pygame.draw.line(win, BLACK, (55, 55*x + 55),(550, 55*x + 55), 2)


# Numbers Inputed by User
def user_input(win, position):
    x, y = position[1], position[0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if (grid_orig[x-1][y-1] != 0):
                    return
                if (event.key == 48): # Checking With Zero (Ascii)
                    grid[x-1][y-1] = event.key - 48
                    pygame.draw.rect(win, background_colour, (position[0] * 55 + buffer, position[1] * 55 + buffer, 55 - 2 * buffer, 55 - 2 * buffer))
                    pygame.display.update()
                    return
                if (0 < event.key - 48 < 10): # Checking for valid input
                    pygame.draw.rect(win, background_colour, (position[0] * 55 + buffer, position[1] * 55 + buffer, 55 - 2 * buffer, 55 - 2 * buffer))
                    val2 = num_font.render(str(event.key - 48), True, BLACK)
                    win.blit(val2, (position[0] * 55 + 20, position[1] * 55))
                    grid[x-1][y-1] = event.key - 48
                    pygame.display.update()
                    return
                return



# Inserting Numbers
def insert_grid(win):
    for x in range(0, len(grid[0])):
        for y in range(0, len(grid[0])):
            if (0 < grid[x][y] < 10):
                val1 = num_font.render(str(grid[x][y]), True, number_colour)
                win.blit(val1, ((y + 1) * 55 + 20, (x + 1) * 55 + 5))


# The Main function that runs
def core():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('SUDOKU')
    win.fill(background_colour)
    
    draw_grid(win)
    insert_grid(win)
    win
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                user_input(win, (pos[0] // 55, pos[1] // 55))
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
if __name__ == '__main__':
    core()