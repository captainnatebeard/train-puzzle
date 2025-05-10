#!/usr/bin/env python3

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
boomImage = pygame.image.load("boom-sm.png")
stationLoc = (850, 60)
trainY = 120
trackLoc = (-15, 100)
input_rect = pygame.Rect(680, 350, 400, 500)
run_rect = pygame.Rect(360, 350, 200, 200)
run_text_rect = pygame.Rect(440, 430, 50, 50)
directions_rect = pygame.Rect(1200, 500, 400, 400)
clear_rect = pygame.Rect(360, 650, 200, 200)
clear_text_rect = pygame.Rect(430, 730, 100, 100)
base_font = pygame.font.Font(None, 32)
train1_start = 670
train2_start = 1030
description = "the two trains on the track are running the same codebase, try to get them to collide in as few lines \
as possible using only these 4 commands: MVL (move left), MVR (move right), STS (skip instruction if at the station), \
and JMP (jump to another line in the code, ex: 'JMP 3').  The box in the middle is for your code.  The green box runs \
your code.  The red box resets and clears                                                   Good luck!"


def main():
    instruction_set = []
    running = True
    active = False
    train1_x = train1_start
    train2_x = train2_start
    at_station1 = False
    at_station2 = False
    collision = False
    line = 0
    pc1 = 0
    pc2 = 0
    color_active = pygame.Color('lightskyblue2')
    color_passive = pygame.Color('lightskyblue3')
    trains_running = False
    first_click = True
    # main game loop
    while running:
        for event in pygame.event.get():
            if event.type == 256:  # (pygame.QUIT)
                running = False
            if event.type == 1026:  # mouse button release
                if input_rect.collidepoint(event.pos):
                    active = True
                    if first_click:
                        instruction_set.append('')
                        first_click = False
                else:
                    active = False
                if run_rect.collidepoint(event.pos) and (inst_valid(instruction_set[-1]) or instruction_set[-1] == ''):
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
            if active and event.type == pygame.KEYDOWN and not trains_running:
                if event.key == pygame.K_BACKSPACE:
                    instruction_set[line] = instruction_set[line][:-1]
                elif event.key == pygame.K_RETURN:
                    if inst_valid(instruction_set[line]):
                        line += 1
                        instruction_set.append('')
                else:
                    instruction_set[line] += event.unicode.upper()
        if trains_running and (inst_valid(instruction_set[-1]) or instruction_set[-1] == ''):
            if pc1 < len(instruction_set):
                train1_x, at_station1, pc1 = run_next_instruction(instruction_set, train1_x, at_station1, pc1)
            if pc2 < len(instruction_set):
                train2_x, at_station2, pc2 = run_next_instruction(instruction_set, train2_x, at_station2, pc2)
        if train1_x > train2_x - 115 or ((pc1 >= len(instruction_set) and pc2 >= len(instruction_set)) and
        not first_click):
            #time.sleep(5)
            trains_running = False
            draw_boom(train1_x)
            train_collision = train1_x
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
            text_surface = base_font.render(str('{num:02d}'.format(num=i)) + ': ' +
                                            instruction_set[i], True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5 + (120 * int(i / 22)), input_rect.y + 5 + ((i % 22) * 22)))
        screen.blit(trackImage, trackLoc)
        screen.blit(stationImage, stationLoc)
        draw_train(train1_x)
        draw_train(train2_x)
        draw_text(screen, description, (255, 255, 255), directions_rect, base_font)
        draw_text(screen, "RUN", (255, 255, 255), run_text_rect, base_font)
        draw_text(screen, "CLEAR", (255, 255, 255), clear_text_rect, base_font)
        if first_click:
            draw_text(screen, "CLICK HERE TO START CODING", (255, 255, 255), input_rect, base_font)
        pygame.display.flip()
        clock.tick(30)


def draw_train(train_x):
    screen.blit(trainImage, (train_x, trainY))

def draw_boom(boom_x):
    screen.blit(boomImage, (boom_x+30, trainY))
    pygame.display.flip()
    print("boom drawn")
    time.sleep(5)

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


def inst_valid(instruction):
    ret = True
    if instruction[0:3] not in instructions:
        ret = False
    if instruction[0:3] == 'JMP' and (not instruction[4:].isnumeric() or instruction[3] != ' '):
        ret = False
    if instruction[0:3] != 'JMP' and len(instruction) > 3:
        ret = False
    return ret


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
