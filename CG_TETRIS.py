import pygame
import random
import math

pygame.init()
pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))

def update_score(nscore):
    score = max_score()
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def draw_window(surface, grid, score, last_score ):
    surface.fill((0, 0, 0))
    start, end = 30, 25
    pygame.draw.rect(surface, (128, 128, 128), (start + 220, end, 300, 50))
    pygame.draw.rect(surface, (48,48,48), (start, end, 200, s_height - end-20))
    pygame.draw.rect(surface, (48,48,48), (start + s_width - 260, end, 210, s_height - end-20))
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 10, sy + 160))
    # last score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))
    sx = top_left_x - 200
    sy = top_left_y + 200
    surface.blit(label, (sx + 20, sy + 160))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    draw_grid(surface, grid)

def main(win,speed):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = speed
    level_time = 0
    score = 0
    end=False
    # run=False
    # end=True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                run = False
                end=True
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE:
                    while True:
                        current_piece.y += 1
                        if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                            current_piece.y -= 1
                            change_piece = True
                            break

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
            end=True
            update_score(score)

    clock=pygame.time.Clock()
    time=0
    global shape_stream, offset
    while end:
        win.fill((17,12,17))
        for i, stream in enumerate(shape_stream):
            draw_stream(stream, (i - 1) * 3 * block_size, offset[i], int(offset[i] / 40))
        pygame.draw.rect(win, (0, 150, 100), (top_left_x - 125, 50, 550, 550))
        time += clock.get_rawtime()
        clock.tick()
        if time<100:
            color=(255,255,255)
        elif time>=100 and time<200:
            color=(0,255,0)
        elif time>=200 and time<300:
            color=(0, 0, 255)
        elif time>=300:
            color = (0, 0, 255)
            time=0
        t = 'YOU LOST!'
        draw_text_name(win, 45, 150, t, 50, color)
        t = 'Press Q To QUIT'
        draw_text_name(win, 5, 200, t, 50, color)
        t = 'Press A To Play Again'
        draw_text_name(win, -30, 250, t, 50, color)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                return 1

def draw_text_name(surface, x, y,text, size, color):
    size-=22
    font = pygame.font.SysFont("bookmanoldstyle", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x+x , top_left_y+y))

def create_stream():
    stream = []
    for _ in range(6):
        temp = Piece(0, 0, random.choice(shapes))
        temp.rotation += random.randint(0, 4)
        stream.append(temp)
    return stream

def draw_shape(shape, surface, sx, sy):
    form = shape.shape[shape.rotation % len(shape.shape)]
    block_size_temp=20
    height = s_height + 50
    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                color=shape.color
                pygame.draw.rect(surface, color,(sx + j * block_size_temp, (sy % height) + (i+1) * block_size_temp - 100,
                                                 block_size_temp, block_size_temp), 0)

def draw_stream(shape_stream, x, offset, speed):
    for j, shape in enumerate(shape_stream):
        draw_shape(shape, win, x, offset + shape.y + j * block_size * 9)
        shape.y += speed
def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
def rotateLinePoints(start, end, degrees):
    startx, starty = start
    endx, endy = end
    middleX = (startx + endx) // 2
    middleY = (starty + endy) // 2
    inRadians = math.radians(degrees)
    newStart = rotate((middleX, middleY), start, inRadians)
    newEnd = rotate((middleX, middleY), end, inRadians)
    return newStart, newEnd
def drawScreen(screen):
    global counter
    counter += 2
    screen.fill((0,0,0))
    for line in lines:
        newStart, newEnd = rotateLinePoints(line[:2], line[2:], counter)
        pygame.draw.line(screen,(255,255,255), newStart, newEnd, 10)

def information_win(win):
    time=0
    clock=pygame.time.Clock()
    while True:
        drawScreen(win)
        pygame.draw.rect(win, (0, 150, 100), (top_left_x - 125, 50, 550, 550))
        t = 'INSTRUCTIONS'
        font = pygame.font.SysFont("signpainterttc", 85, bold=True)
        label = font.render(t, 1, (255, 255, 255))
        win.blit(label, (top_left_x + (-110), top_left_y + 0))
        t = 'Press Q to quit'
        draw_text_name(win, -100, 150, t, 40, (255, 255, 255))
        t = 'Press Left Arrow To Move Left'
        draw_text_name(win, -100, 180, t, 40, (255, 255, 255))
        t = 'Press Right Arrow To Move right'
        draw_text_name(win, -100, 210, t, 40, (255, 255, 255))
        t = 'Press Up Arrow To rotate the shape'
        draw_text_name(win, -100, 240, t, 40, (255, 255, 255))
        t = 'Press Down Arrow repeatedly To Move faster'
        draw_text_name(win, -100, 270, t, 40, (255, 255, 255))
        t = 'Press Space Bar For Hard Drop'
        draw_text_name(win, -100, 300, t, 40, (255, 255, 255))
        time += clock.get_rawtime()
        clock.tick()
        if time < 100:
            color = (255, 255, 255)
        elif time >= 100 and time < 200:
            color = (255,0, 0)
        elif time >= 200 and time < 300:
            color = (0, 0, 255)
        elif time >= 300:
            color = (0, 0, 255)
            time = 0
        t = 'PRESS A TO GO BACK'
        draw_text_name(win, -100, 400, t, 60, color)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT  or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                return 1

def main_menu(win):
    run = True
    global shape_stream,offset
    while run:
        win.fill((17,12,17))
        for i, stream in enumerate(shape_stream):
            draw_stream(stream, (i - 1) * 3 * block_size, offset[i], int(offset[i] / 40))
        pygame.draw.rect(win, (0, 150, 100), (top_left_x - 125, 50, 550, 550))
        t = 'DELHI TECHNOLOGICAL UNIVERSITY'
        draw_text_name(win, -50, 0, t, 47, (255, 255, 255))        
        t = 'Made by :'
        draw_text_name(win, 85, 260, t, 45, (255, 255, 255))
        t = 'SHUBHAM RANJAN'
        draw_text_name(win, 50, 300, t, 45, (255, 255, 255))
        t = 'HARSHIT MUHAL'
        draw_text_name(win, 50, 330, t, 45, (255, 255, 255))
        logo = pygame.image.load('logo2.png')
        logo = pygame.transform.scale(logo, (150, 150))
        win.blit(logo, (top_left_x + 85, 170))
        text = 'Press E Key To Play in Easy Mode'
        draw_text_name(win, -90, 390, text, 40, (255,255,255))
        text = 'Press M Key To Play in Medium Mode'
        draw_text_name(win, -90, 415, text, 40, (255, 255, 255))
        text = 'Press D Key To Play in Difficult Mode'
        draw_text_name(win, -90, 440, text, 40, (255,255,255))
        text = 'Press I To see Instructions'
        draw_text_name(win, -90, 465, text, 40, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    f=main(win,0.28)
                    if f==-1:
                        run = False
                if event.key == pygame.K_m:
                    f=main(win, 0.14)
                    if f==-1:
                        run = False
                if event.key == pygame.K_d:
                    f=main(win,0.09)
                    if f==-1:
                        run = False
                if event.key == pygame.K_i:
                    f=information_win(win)
                    if f==-1:
                        run = False
                if event.key == pygame.K_q:
                    run=False
    pygame.display.quit()
counter = 0
lines = []
square = 50
for x in range(0, s_width, square):
    for y in range(0, s_height, square):
        if random.random() > 0.5:
            lines.append([x, y, x + square, y + square])
        else:
            lines.append([x, y + square, x + square, y])

shape_stream = [create_stream() for _ in range(20)]
offset = [block_size * random.randrange(3, 10) for _ in range(len(shape_stream))]
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
pygame.mixer.music.load("Tetris.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
main_menu(win)
pygame.mixer.music.stop()

