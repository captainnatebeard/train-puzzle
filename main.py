import pygame
import time


pygame.init()
clock = pygame.time.Clock()
instructions = ['MVL', 'MVR', 'JMP', 'STS']
screen = pygame.display.set_mode((1800, 900))
pygame.display.set_caption("train")
trainImage = pygame.image.load("toy-train-sm.png")
trackImage = pygame.image.load("tracks_long.png")
stationImage = pygame.image.load("station-sm.png")
stationLoc = (820, 60)
trainY = 120
trackLoc = (80, 100)
input_rect = pygame.Rect(600, 350, 400, 500)
run_rect = pygame.Rect(300, 350, 200, 200)
directions_rect = pygame.Rect(1200, 500, 400, 400)
clear_rect = pygame.Rect(300, 650, 200, 200)
color_active = pygame.Color('lightskyblue2')
color_passive = pygame.Color('lightskyblue3')
color = color_passive
base_font = pygame.font.Font(None, 32)
train1_start = 650
train2_start = 1000
description = "the two trains on the track are running the same codebase, try to get them to collide using only \
these 4 commands: MVL (move left), MVR (move right), STS (skip instruction if at the station), and JMP \
(jump to another line in the code).  The box in the middle is for your code.  The green box runs your code.  \
The red box resets and clears                                                                   Good luck!"


def main():
    pygame.init()
    instruction_set = []
    running = True
    active = False
    train1_x = train1_start
    train2_x = train2_start
    at_station1 = False
    at_station2 = False
    line = 0
    pc1 = 0
    pc2 = 0
    instruction_set.append('')
    trains_running = False
    # Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == 256: #(pygame.QUIT)
                running = False
            if event.type == 1026: #mouse click up
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if run_rect.collidepoint(event.pos):
                    trains_running = True
                if clear_rect.collidepoint(event.pos):
                    instruction_set = []
                    line = 0
                    instruction_set.append('')
                    trains_running = False
                    train1_x = train1_start
                    train2_x = train2_start
                    pc1 = 0
                    pc2 = 0
                click_pos = event.pos
                print(click_pos)
            if active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    instruction_set[line] = instruction_set[line][:-1]
                elif event.key == pygame.K_RETURN:
                    if instruction_set[line][0:3] in instructions and \
                        ((instruction_set[line][0:3] == 'JMP' and len(instruction_set[line]) > 3
                            and instruction_set[line][3] == ' ' and instruction_set[line][4:].isnumeric())
                            or (len(instruction_set[line]) == 3 and instruction_set[line][0:3] != 'JMP')):
                        line += 1
                        instruction_set.append('')
                else:
                    instruction_set[line] += event.unicode.upper()
        if trains_running:
            train1_x, at_station1, pc1 = run_next_instruction(instruction_set, train1_x, at_station1, pc1)
            train2_x, at_station2, pc2 = run_next_instruction(instruction_set, train2_x, at_station2, pc2)
        if train1_x > train2_x - 120 or pc1 >= len(instruction_set) or pc2 >= len(instruction_set):
            time.sleep(5)
            line = 0
            instruction_set.append('')
            trains_running = False
            train1_x = train1_start
            train2_x = train2_start
            pc1 = 0
            pc2 = 0
        screen.fill((255, 100, 100))
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)
        pygame.draw.rect(screen, pygame.Color('red'), clear_rect)
        pygame.draw.rect(screen, pygame.Color('green'), run_rect)
        for i in range(len(instruction_set)):
            text_surface = base_font.render(str(i) + ': ' + instruction_set[i], True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5 + (i*22)))
        screen.blit(trackImage, trackLoc)
        screen.blit(stationImage, stationLoc)
        draw_train(train1_x)
        draw_train(train2_x)
        draw_text(screen, description, (255,255,255), directions_rect, base_font)
        pygame.display.flip()
        clock.tick(30)


def draw_train(train_x):
    screen.blit(trainImage, (train_x, trainY))


def run_next_instruction(instruction_set, train_x, at_station, pc):
    instruction = instruction_set[pc]
    if instruction == 'STS' and at_station:
        pc += 2
    elif instruction[0:3] == 'JMP':
        pc = int(instruction[4:])
    else:
        pc += 1
    if instruction == 'MVL':
        train_x -= 5
    if instruction == 'MVR':
        train_x += 5
    if train_x == stationLoc[0]:
        at_station = True
    else:
        at_station = False
    return train_x, at_station, pc


def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2
    font_height = font.size("Tg")[1]
    while text:
        i = 1
        if y + font_height > rect.bottom:
            break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing
        text = text[i:]
    return text

if __name__ == "__main__":
    main()