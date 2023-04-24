import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
size=[800,600]

# Screen initialization
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Paint Program")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 170, 51)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up drawing variables
radius = 12
drawing = False
color = BLACK

# Setting up the fons
font = pygame.font.SysFont("Minecraftia", 50)
font_msg = pygame.font.SysFont("Minecraftia", 20)
font_col = (0, 0, 0)

percent_text = font.render(str(""), True, BLUE)
close_text = font_msg.render("Too close to the dot!", True, RED)
status_text = font_msg.render("0", True, RED)

def reversed_y(x1, y1, x2, y2, x3, y3):
    """
    Determines whether a point (x3, -y3) lies on the line passing through (x1, y1) and (x2, y2).
    """
    # Check if the line is vertical
    if x2 - x1 == 0:
        return x3 == x1 and y3 == -y1

    # Compute the slope of the line passing through (x1, y1) and (x2, y2)
    slope = (y2 - y1) / (x2 - x1)

    # Compute the y-intercept of the line passing through (x1, y1) and (x2, y2)
    y_intercept = y1 - slope * x1

    # Check if (x3, -y3) lies on the line passing through (x1, y1) and (x2, y2)
    return y3 == -slope * x3 - y_intercept


def isInLine(x0, y0, x1, y1, x, y):
    k = (y1-y0)/(x1-x0)
    b = y0 - k*x0
    new_y = k*x + b
    new_x =0
    temp_y =1

def delta(start, end):
    start_x = start[0]-400
    start_y = start[1]-300
    end_x = end[0]-400
    end_y  = end[1]-300
    a = math.sqrt(start_x**2 + start_y**2)
    b = math.sqrt(end_x**2 + end_y**2)
    return abs(a-b)

def radi(start):
    a = math.sqrt((start[0] - 400) ** 2 + (start[1] - 300) ** 2)
    return a


start = 0
start_pos = 0, 0


# Create a list to store all the elements drawn on the screen
percent = 0
elements = []
el_set = {(1, 1)}
sum = 0


best_score = 0
best_color = (0, 0, 0)

status_circ = 0
status_close = 0
wrongside = 0
default = 0
newscore = 0
timeUp = 0

n_perc = 0


s_cnt =1


t_cnt =1
TU_ticks = 0


# Game loop
while True:
    if s_cnt:
        s_t = 0
        s_t = pygame.time.get_ticks()
        s_cnt = 0
        t_p = pygame.mouse.get_pos()

    if t_cnt:
        TU_ticks = 0
        TU_ticks = pygame.time.get_ticks()
        t_cnt = 0

    TU_seconds = (pygame.time.get_ticks() - TU_ticks)/1000
    seconds = (pygame.time.get_ticks() - s_t)/1000


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if start:
            start = 0
            start_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            elements = []
            start, drawing = 1, 1
            n_perc = 0
            wrongside = 0
            default = 0
            timeUp = 0
            TU_seconds = 0
            newscore = 0
            t_cnt=1

            pos = pygame.mouse.get_pos()
            if(radi(start_pos)<=100):
                status_circ = 1
            # Create a new circle element and add it to the list of elements
            element = {"type": "circle", "color": color, "radius": radius, "pos": pos}
            elements.append(element)


        elif event.type == pygame.MOUSEBUTTONUP:

            if(percent>best_score and not timeUp):
                newscore = 1
                best_score = percent
                best_color = font_col
            elif not (timeUp or wrongside or status_circ):
                default = 1

            radius = 8
            percent = 0
            el_set = {(1, 1)}
            drawing = False

        elif event.type == pygame.MOUSEMOTION and drawing:
            if TU_seconds>9:
                timeUp = 1
                drawing = 0
            if seconds>0.008:
                seconds = 0
                s_cnt = 1
                if(t_p==pos):
                    if(radius<12):
                        radius+=1
                else:
                    if(radius>2):
                        radius-=1

            pos = pygame.mouse.get_pos()
            if (radi(pos) <= 10):
                status_circ = 1
                default = 0
            if (delta(start_pos, pos) < 25):
                circle_color = GREEN
            elif (delta(start_pos, pos) > 25 and delta(start_pos, pos) < 35):
                circle_color = YELLOW
            else:
                circle_color = (255, 0, 0)


            lenn = len(el_set) // 2

            if(len(el_set)>13):
                for i in el_set:
                    sum+=delta(i, start_pos)
                temp = (sum/(lenn+1))
                sum = 0
                percent = (1-temp/radi(start_pos)*0.7)
                if(percent>0.7):
                    font_col = (int(255-(((percent-0.7)/0.3)*255)), int(((percent-0.7)/0.3)*255), 0)
                else:
                    font_col = (255, 0, 0)
                if(isInLine(400, 300,start_pos[0], start_pos[1],pos[0], pos[1])==1):
                    default=1
                    drawing=0
                if (reversed_y(400, 300, start_pos[0], start_pos[1], pos[0], pos[1]) == 1):
                    default = 1
                    drawing = 0

                if(percent<0):
                    n_perc = 1
                    wrongside = 1
                    drawing = 0

                if n_perc:
                    percent_text = font.render('XX:xx%', True, font_col)
                else:
                    percent_text = font.render(str(round(percent * 100, 2)) + '%', True, font_col)


            prev_pos = elements[-1]["pos"]  # Get the previous mouse position
            distance = max(abs(pos[0] - prev_pos[0]), abs(
                pos[1] - prev_pos[1]))  # Get the distance between the current and previous mouse positions
            for i in range(distance):
                x = int(prev_pos[0] + (pos[0] - prev_pos[0]) * float(i) / distance)
                y = int(prev_pos[1] + (pos[1] - prev_pos[1]) * float(i) / distance)
                # Create a new circle element and add it to the list of elements
                element = {"type": "circle", "color": circle_color, "radius": radius, "pos": (x, y)}

                elements.append(element)
                el_set.add((x,y))
    k = (start_pos[0] - 400) / (start_pos[1] - 300)
    b = start_pos[1] - start_pos[0]
    # Draw the screen
    screen.fill(BLACK)
    screen.blit(percent_text, (320, 250))
    pygame.draw.circle(screen, (255, 255, 255), (400, 300), 6, width=0)
    if timeUp and not wrongside and not default:
        status_text = font_msg.render("Too slow", True, (0, 255, 0))
        screen.blit(status_text, (300, 340))
    if newscore and not wrongside and not default and not status_close:
        status_text = font_msg.render("New best score", True, (0, 255, 0))
        screen.blit(status_text, (300, 340))
    if wrongside:
        status_text = font_msg.render("Wrong side!", True, (0, 255, 0))
        screen.blit(status_text, (300, 340))
        drawing = 0
    if default and not wrongside and not status_circ:
        status_text = font_msg.render("Best: ", True, WHITE)
        bst_2 = font_msg.render(str(round(best_score * 100, 2)) + '%', True, best_color)
        screen.blit(status_text, (340, 340))
        screen.blit(bst_2, (410, 340))
    if status_close and not drawing and not wrongside and not status_circ:
        screen.blit(close_text, (300, 340))
    else:
        status_close = 0
    if status_circ and not wrongside and not default:
        screen.blit(close_text, (300, 340))
        drawing = 0
        status_circ = 0
        status_close = 1


    for element in elements:
        if element["type"] == "circle":
            pygame.draw.circle(screen, element["color"], element["pos"], element["radius"])

    pygame.display.flip()