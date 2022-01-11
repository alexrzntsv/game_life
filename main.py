import pygame
from pygame.locals import *
import random

class Button:
    def __init__(self, surface, width, height, x, y):
        self.surface = surface
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.inactive_color = (220, 220, 220)
        self.active_color = (128, 128, 128)


    def draw(self, message):
        mouse = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 30)
        text = font.render(message, True, [0, 0, 0])
        textpos = (self.x + 5, self.y + 10)
        if (self.x < mouse[0] < self.x + self.width) and (self.y < mouse[1] < self.y + self.height):
            pygame.draw.rect(self.surface, self.active_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, self.inactive_color, (self.x, self.y, self.width, self.height))
        self.surface.blit(text, textpos)


class Cell:
    def __init__(self, x, y, state=0):
        self.x = x
        self.y = y
        self.state = state

    def is_alive(self):
        return self.state

class CellList:
    def __init__(self, surface, cell_size, nrows, ncolumns, randomize=False):
        self.surface = surface
        self.cell_size = cell_size
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.list = self.make(randomize)

    def make(self, randomize):
        if randomize:
            cell_list = [[Cell(column * self.cell_size, row * self.cell_size, random.randint(0, 1))
                          for column in range(0, self.ncolumns)] for row in range(0, self.nrows)]
        else:
            cell_list = [[Cell(column * self.cell_size, row * self.cell_size, 0)
                          for column in range(0, self.ncolumns)] for row in range(0, self.nrows)]
        return cell_list

    def get_neighbours(self, cell):
        cell_list = self.list
        neighbours_list = []
        for y in range(cell[0] - 1, cell[0] + 2):
            for x in range(cell[1] - 1, cell[1] + 2):
                if y == cell[0] and x == cell[1]:
                    pass
                else:
                    try:
                        neighbours_list.append(cell_list[y][x].is_alive())
                    except IndexError:
                        pass
        return neighbours_list

    def update(self):
        cell_list = self.list
        cell_list = [[(cell_list[y][x], sum(self.get_neighbours((y, x)))) for x in range(len(cell_list[y]))]
                     for y in range(len(cell_list))]

        def new_cel(arg):
            if (arg[0].is_alive() == 0) and (arg[1] == 3):
                return 1
            elif (arg[0].is_alive() == 1) and (arg[1] == 2 or arg[1] == 3):
                return 1
            else:
                return 0

        cell_list = [[Cell(y * self.cell_size, x * self.cell_size, new_cel(cell_list[y][x]))
                      for x in range(len(cell_list[y]))] for y in range(len(cell_list))]
        self.list = cell_list

    def draw(self):
        cell_list = self.list
        for y in range(0, len(cell_list)):
            for x in range(0, len(cell_list[y])):
                if cell_list[y][x].is_alive() == 0:
                    pygame.draw.rect(self.surface, pygame.Color('white'),
                                     (x * self.cell_size + 1, y * self.cell_size + 1,
                                      self.cell_size - 1, self.cell_size - 1))
                elif cell_list[y][x].is_alive() == 1:
                    pygame.draw.rect(self.surface, pygame.Color('green'),
                                     (x * self.cell_size + 1, y * self.cell_size + 1,
                                      self.cell_size - 1, self.cell_size - 1))



class Life:
    def __init__(self, width=200, height=400, cell_size=20, fps=5, randomize=False):
        self.width = width
        self.height = height - 59

        self.cell_size = cell_size
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.fps = fps

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.rects = CellList(self.screen, self.cell_size, self.cell_height, self.cell_width, randomize)

    def make_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))



    def run_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Life')
        self.screen.fill(pygame.Color('white'))
        button_start = Button(self.screen, 60, 40, 10, self.height + 10)
        button_stop = Button(self.screen, 60, 40, 100, self.height + 10)
        button_new_game = Button(self.screen, 120, 40, 190, self.height + 10)
        button_fill_randomly = Button(self.screen, 180, 40, 340, self.height + 10)
        running = False
        game = True
        counter = 0
        while game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game = False
                elif event.type == MOUSEBUTTONDOWN:
                    if (button_start.x < pygame.mouse.get_pos()[0] < button_start.x + button_start.width)\
                            and (button_start.y < pygame.mouse.get_pos()[1] < button_start.y + button_start.height):
                        running = True
                    elif (button_stop.x < pygame.mouse.get_pos()[0] < button_stop.x + button_stop.width)\
                            and (button_stop.y < pygame.mouse.get_pos()[1] < button_stop.y + button_stop.height):
                        running = False
                    elif (button_new_game.x < pygame.mouse.get_pos()[0] < button_new_game.x + button_new_game.width)\
                            and (button_new_game.y < pygame.mouse.get_pos()[1] < button_new_game.y + button_new_game.height):
                        running = False
                        return run(randomize=False)
                    elif (button_fill_randomly.x < pygame.mouse.get_pos()[0] < button_fill_randomly.x + button_fill_randomly.width)\
                            and (button_fill_randomly.y < pygame.mouse.get_pos()[1] < button_fill_randomly.y + button_fill_randomly.height):
                        running = False
                        return run(randomize=True)
                    else:
                        if counter == 0:
                            x_pos = pygame.mouse.get_pos()[0] // self.cell_size
                            y_pos = pygame.mouse.get_pos()[1] // self.cell_size
                            try:
                                if self.rects.list[y_pos][x_pos].is_alive() == 0:
                                    self.rects.list[y_pos][x_pos].state = 1
                                elif self.rects.list[y_pos][x_pos].is_alive() == 1:
                                    self.rects.list[y_pos][x_pos].state = 0
                            except IndexError:
                                pass
            self.make_grid()
            self.rects.draw()
            if running == True:
                self.rects.update()
                counter+=1
            button_start.draw('Start')
            button_stop.draw('Stop')
            button_new_game.draw('New Game')
            button_fill_randomly.draw('Fill randomly')
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

def run(randomize=False):
    game = Life(680, 480, 20, 5, randomize)
    game.run_game()

if __name__ == '__main__':
    run()
