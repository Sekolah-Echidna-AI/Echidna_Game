# import pygame
# import random
# import json
# import tkinter as tk
# from tkinter import filedialog
# import asyncio

# pygame.init()

# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 700

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
# pygame.display.set_caption("Quiz Game")

# clock = pygame.time.Clock()

# # Blue theme
# BG = (22, 41, 84)
# CARD = (40, 73, 140)
# BUTTON = (70, 120, 200)
# TEXT = (240, 245, 255)
# ACCENT = (120, 180, 255)

# font = pygame.font.SysFont("arial", 28)
# big_font = pygame.font.SysFont("arial", 40)


# questions = []


# # ------------------------
# # TEXT WRAP FUNCTION
# # ------------------------

# def draw_wrapped_text(text, rect, font, color):

#     words = text.split(" ")
#     lines = []
#     current = ""

#     for word in words:

#         test = current + word + " "

#         if font.size(test)[0] < rect.width - 20:
#             current = test
#         else:
#             lines.append(current)
#             current = word + " "

#     lines.append(current)

#     y = rect.y + 10

#     for line in lines:
#         img = font.render(line, True, color)
#         screen.blit(img, (rect.x + 10, y))
#         y += font.get_height()


# # ------------------------
# # IMPORT JSON BUTTON
# # ------------------------

# def import_questions():

#     global questions

#     root = tk.Tk()
#     root.withdraw()

#     file_path = filedialog.askopenfilename(
#         filetypes=[("JSON Files", "*.json")]
#     )

#     if file_path:

#         with open(file_path, "r") as f:
#             questions = json.load(f)


# # ------------------------
# # DRAW GAME SCREEN
# # ------------------------

# def draw_game(question, options, score, timer, turn):

#     w, h = screen.get_size()

#     screen.fill(BG)

#     # import button
#     import_rect = pygame.Rect(w - 170, 20, 150, 40)
#     pygame.draw.rect(screen, ACCENT, import_rect, border_radius=8)

#     screen.blit(font.render("Import JSON", True, BG), (import_rect.x + 10, import_rect.y + 8))

#     # score
#     screen.blit(font.render(f"Score: {score}", True, TEXT), (20, 20))

#     # timer
#     screen.blit(font.render(f"Timer: {timer}", True, TEXT), (w//2 - 50, 20))

#     # question box
#     q_rect = pygame.Rect(w*0.2, h*0.35, w*0.6, 100)
#     pygame.draw.rect(screen, CARD, q_rect, border_radius=10)

#     draw_wrapped_text(question, q_rect, big_font, TEXT)

#     # answer buttons
#     option1_rect = pygame.Rect(w*0.2, h*0.65, w*0.25, 80)
#     option2_rect = pygame.Rect(w*0.55, h*0.65, w*0.25, 80)

#     pygame.draw.rect(screen, BUTTON, option1_rect, border_radius=10)
#     pygame.draw.rect(screen, BUTTON, option2_rect, border_radius=10)

#     draw_wrapped_text(options[0], option1_rect, font, TEXT)
#     draw_wrapped_text(options[1], option2_rect, font, TEXT)

#     pygame.display.flip()

#     return option1_rect, option2_rect, import_rect


# # ------------------------
# # FINAL SCREEN
# # ------------------------

# def show_final_score(score):

#     w, h = screen.get_size()

#     screen.fill(BG)

#     text = big_font.render(f"Final Score: {score}", True, TEXT)
#     screen.blit(text, (w/2 - text.get_width()/2, h*0.4))

#     restart_rect = pygame.Rect(w*0.3, h*0.6, 150, 60)
#     exit_rect = pygame.Rect(w*0.55, h*0.6, 150, 60)

#     pygame.draw.rect(screen, BUTTON, restart_rect, border_radius=10)
#     pygame.draw.rect(screen, BUTTON, exit_rect, border_radius=10)

#     screen.blit(font.render("Restart", True, TEXT), (restart_rect.x + 25, restart_rect.y + 18))
#     screen.blit(font.render("Exit", True, TEXT), (exit_rect.x + 45, exit_rect.y + 18))

#     pygame.display.flip()

#     return restart_rect, exit_rect


# # ------------------------
# # MAIN GAME LOOP
# # ------------------------

# async def main():

#     global questions

#     score = 0
#     turn = 1
#     used = []

#     if not questions:
#         import_questions()

#     total_questions = len(questions)

#     while turn <= total_questions:

#         q = random.choice([x for x in questions if x not in used])
#         used.append(q)

#         question = q["question"]
#         options = q["options"]
#         correct = q["answer"]

#         timer = 10
#         answered = False

#         while timer > 0:

#             clock.tick(60)
#             timer -= 1/60

#             option1_rect, option2_rect, import_rect = draw_game(
#                 question,
#                 options,
#                 score,
#                 int(timer),
#                 turn
#             )

#             for event in pygame.event.get():

#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return

#                 if event.type == pygame.VIDEORESIZE:
#                     pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

#                 if event.type == pygame.MOUSEBUTTONDOWN:

#                     pos = pygame.mouse.get_pos()

#                     if import_rect.collidepoint(pos):
#                         import_questions()

#                     if not answered:

#                         if option1_rect.collidepoint(pos):

#                             answered = True
#                             if options[0] == correct:
#                                 score += 1
#                             timer = 0

#                         elif option2_rect.collidepoint(pos):

#                             answered = True
#                             if options[1] == correct:
#                                 score += 1
#                             timer = 0

#         turn += 1

#     restart_rect, exit_rect = show_final_score(score)

#     while True:

#         for event in pygame.event.get():

#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return

#             if event.type == pygame.MOUSEBUTTONDOWN:

#                 pos = pygame.mouse.get_pos()

#                 if restart_rect.collidepoint(pos):
#                     main()

#                 if exit_rect.collidepoint(pos):
#                     pygame.quit()
#                     return
#         await asyncio.sleep(0)


# asyncio.run(main())

import pygame
import random
import json
import tkinter as tk
from tkinter import filedialog
import asyncio

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Quiz Game")

clock = pygame.time.Clock()

# Elegant blue theme
BG = (18, 32, 64)
CARD = (36, 64, 128)
BUTTON = (64, 112, 200)
BUTTON_HOVER = (90, 150, 240)
TEXT = (235, 240, 255)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 40)

questions = []


# -------------------------
# TEXT WRAP
# -------------------------
# def draw_wrapped_text(text, rect, font, color):

#     words = text.split(" ")
#     lines = []
#     current = ""

#     for word in words:

#         test = current + word + " "

#         if font.size(test)[0] < rect.width - 20:
#             current = test
#         else:
#             lines.append(current)
#             current = word + " "

#     lines.append(current)

#     y = rect.y + 10

#     for line in lines:
#         img = font.render(line, True, color)
#         screen.blit(img, (rect.x + 10, y))
#         y += font.get_height()
def draw_wrapped_text(text, rect, font, color):

    words = text.split(" ")
    lines = []
    current = ""

    # Wrap lines
    for word in words:
        test = current + word + " "

        if font.size(test)[0] <= rect.width - 20:
            current = test
        else:
            lines.append(current.strip())
            current = word + " "

    lines.append(current.strip())

    # Calculate total text height
    line_height = font.get_height()
    total_text_height = len(lines) * line_height

    # Start Y so text is vertically centered
    y = rect.y + (rect.height - total_text_height) / 2

    # Draw each line centered
    for line in lines:

        img = font.render(line, True, color)

        x = rect.x + (rect.width - img.get_width()) / 2

        screen.blit(img, (x, y))

        y += line_height


# -------------------------
# FILE IMPORT
# -------------------------
def import_questions():

    global questions

    root = tk.Tk()
    root.withdraw()

    path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

    if path:
        with open(path, "r") as f:
            questions = json.load(f)


# -------------------------
# BUTTON DRAW
# -------------------------
def draw_button(rect, text):

    mouse = pygame.mouse.get_pos()

    color = BUTTON
    if rect.collidepoint(mouse):
        color = BUTTON_HOVER

    pygame.draw.rect(screen, color, rect, border_radius=10)

    txt = font.render(text, True, TEXT)
    screen.blit(
        txt,
        (
            rect.x + rect.width / 2 - txt.get_width() / 2,
            rect.y + rect.height / 2 - txt.get_height() / 2,
        ),
    )


# -------------------------
# START MENU
# -------------------------
def start_menu():

    while True:

        w, h = screen.get_size()
        screen.fill(BG)

        title = big_font.render("QUIZ GAME", True, TEXT)
        screen.blit(title, (w / 2 - title.get_width() / 2, h * 0.2))

        start_rect = pygame.Rect(w / 2 - 100, h * 0.4, 200, 60)
        import_rect = pygame.Rect(w / 2 - 100, h * 0.52, 200, 60)
        help_rect = pygame.Rect(w / 2 - 100, h * 0.64, 200, 60)

        draw_button(start_rect, "Start")
        draw_button(import_rect, "Import Questions")
        draw_button(help_rect, "Help")

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()

                if start_rect.collidepoint(pos):
                    return

                if import_rect.collidepoint(pos):
                    import_questions()

                if help_rect.collidepoint(pos):
                    show_help()


# -------------------------
# HELP SCREEN
# -------------------------
def show_help():

    running = True

    while running:

        w, h = screen.get_size()
        screen.fill(BG)

        lines = [
            "GAME RULES",
            "",
            "1. Import questions JSON",
            "2. Click Start",
            "3. Choose the correct answer",
            "4. Each question has a timer",
            "5. Score increases for correct answers",
            "",
            "Press ESC to return"
        ]

        for i, line in enumerate(lines):

            txt = font.render(line, True, TEXT)
            screen.blit(txt, (w / 2 - txt.get_width() / 2, 150 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


# -------------------------
# GAME SCREEN
# -------------------------
def draw_game(question, options, score, timer, turn, total):

    w, h = screen.get_size()

    screen.fill(BG)

    # score
    screen.blit(font.render(f"Score: {score}", True, TEXT), (20, 20))

    # question count (TOP RIGHT)
    qc = font.render(f"{turn}/{total}", True, TEXT)
    screen.blit(qc, (w - qc.get_width() - 20, 20))

    # timer
    timer_text = font.render(f"Timer: {timer}", True, TEXT)
    screen.blit(timer_text, (w / 2 - timer_text.get_width() / 2, 20))

    # question card
    q_rect = pygame.Rect(w * 0.2, h * 0.35, w * 0.6, 100)
    pygame.draw.rect(screen, CARD, q_rect, border_radius=10)

    draw_wrapped_text(question, q_rect, big_font, TEXT)

    # answer buttons
    option1_rect = pygame.Rect(w * 0.2, h * 0.6, w * 0.25, 80)
    option2_rect = pygame.Rect(w * 0.55, h * 0.6, w * 0.25, 80)

    draw_button(option1_rect, "")
    draw_button(option2_rect, "")

    draw_wrapped_text(options[0], option1_rect, font, TEXT)
    draw_wrapped_text(options[1], option2_rect, font, TEXT)

    # import button (BOTTOM LEFT)
    import_rect = pygame.Rect(20, h - 70, 200, 50)
    draw_button(import_rect, "Import JSON")

    # help button (BOTTOM RIGHT)
    help_rect = pygame.Rect(w - 200 - 20, h - 70, 200, 50)
    draw_button(help_rect, "Help")

    pygame.display.flip()

    return option1_rect, option2_rect, import_rect, help_rect


# -------------------------
# MAIN GAME
# -------------------------
def main():

    if not questions:
        return

    score = 0
    turn = 1
    used = []
    total = len(questions)

    while turn <= total:

        q = random.choice([x for x in questions if x not in used])
        used.append(q)

        question = q["question"]
        options = q["options"]
        correct = q["answer"]

        timer = 10
        answered = False

        while timer > 0:

            clock.tick(60)
            timer -= 1 / 60

            option1_rect, option2_rect, import_rect, help_rect = draw_game(
                question, options, score, int(timer), turn, total
            )

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()

                    if import_rect.collidepoint(pos):
                        import_questions()

                    if help_rect.collidepoint(pos):
                        show_help()

                    if not answered:

                        if option1_rect.collidepoint(pos):

                            answered = True
                            if options[0] == correct:
                                score += 1

                            timer = 0

                        elif option2_rect.collidepoint(pos):

                            answered = True
                            if options[1] == correct:
                                score += 1

                            timer = 0

        turn += 1


# -------------------------
# RUN PROGRAM
# -------------------------
async def app(): 
    while True:

        start_menu()
        main()
        await asyncio.sleep(0)

asyncio.run(app())