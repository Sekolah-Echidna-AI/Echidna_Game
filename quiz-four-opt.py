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

# COLORS
BG = (18, 32, 64)
CARD = (36, 64, 128)

BUTTON = (64, 112, 200)
BUTTON_HOVER = (90, 150, 240)

# GREEN = (60, 200, 120)
# RED = (220, 70, 70)
GREEN = (0, 255, 120)
RED = (255, 60, 60)

TEXT = (235, 240, 255)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 40)

questions = []

# -------------------------
# TEXT WRAP
# -------------------------
def draw_wrapped_text(text, rect, font, color):

    words = text.split(" ")
    lines = []
    current = ""

    for word in words:

        test = current + word + " "

        if font.size(test)[0] <= rect.width - 20:
            current = test
        else:
            lines.append(current.strip())
            current = word + " "

    lines.append(current.strip())

    line_height = font.get_height()
    total_height = len(lines) * line_height

    y = rect.y + (rect.height - total_height) / 2

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
# BUTTON CLASS
# -------------------------
class Button:

    def __init__(self, rect, text):

        self.rect = pygame.Rect(rect)
        self.text = text
        self.scale = 1.0
        self.color = BUTTON

    # def draw(self):

    #     mouse = pygame.mouse.get_pos()

    #     target_scale = 1.0
    #     target_color = BUTTON

    #     if self.rect.collidepoint(mouse):

    #         target_scale = 1.08
    #         target_color = BUTTON_HOVER

    #     # smooth animation
    #     self.scale += (target_scale - self.scale) * 0.2

    #     self.color = tuple(
    #         int(self.color[i] + (target_color[i] - self.color[i]) * 0.2)
    #         for i in range(3)
    #     )

    #     w = self.rect.width * self.scale
    #     h = self.rect.height * self.scale

    #     x = self.rect.centerx - w / 2
    #     y = self.rect.centery - h / 2

    #     draw_rect = pygame.Rect(x, y, w, h)

    #     pygame.draw.rect(screen, self.color, draw_rect, border_radius=12)

    #     txt = font.render(self.text, True, TEXT)

    #     screen.blit(
    #         txt,
    #         (
    #             draw_rect.centerx - txt.get_width() / 2,
    #             draw_rect.centery - txt.get_height() / 2,
    #         ),
    #     )
    def draw(self, override_color=None):

        mouse = pygame.mouse.get_pos()

        target_scale = 1.0
        target_color = BUTTON

        if self.rect.collidepoint(mouse):
            target_scale = 1.08
            target_color = BUTTON_HOVER

        if override_color:
            target_color = override_color

        # smooth animation
        self.scale += (target_scale - self.scale) * 0.2

        self.color = tuple(
            int(self.color[i] + (target_color[i] - self.color[i]) * 0.2)
            for i in range(3)
        )

        w = self.rect.width * self.scale
        h = self.rect.height * self.scale

        x = self.rect.centerx - w / 2
        y = self.rect.centery - h / 2

        draw_rect = pygame.Rect(x, y, w, h)

        pygame.draw.rect(screen, self.color, draw_rect, border_radius=12)

        txt = font.render(self.text, True, TEXT)

        screen.blit(
            txt,
            (
                draw_rect.centerx - txt.get_width() / 2,
                draw_rect.centery - txt.get_height() / 2,
            ),
        )

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# -------------------------
# PROGRESS BAR
# -------------------------
def draw_timer_bar(timer, max_time):

    w, h = screen.get_size()

    bar_w = w * 0.5
    bar_h = 20

    x = w / 2 - bar_w / 2
    y = 60

    progress = timer / max_time

    pygame.draw.rect(screen, (50, 70, 120), (x, y, bar_w, bar_h), border_radius=8)

    pygame.draw.rect(
        screen,
        (100, 200, 255),
        (x, y, bar_w * progress, bar_h),
        border_radius=8,
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

        start_btn = Button((w / 2 - 100, h * 0.4, 200, 60), "Start")
        import_btn = Button((w / 2 - 100, h * 0.52, 200, 60), "Import")
        help_btn = Button((w / 2 - 100, h * 0.64, 200, 60), "Help")

        start_btn.draw()
        import_btn.draw()
        help_btn.draw()

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()

                if start_btn.clicked(pos):
                    return

                if import_btn.clicked(pos):
                    import_questions()

                if help_btn.clicked(pos):
                    show_help()


# -------------------------
# HELP
# -------------------------
def show_help():

    running = True

    while running:

        w, h = screen.get_size()

        screen.fill(BG)

        lines = [
            "GAME RULES",
            "",
            "Import a JSON file",
            "Choose the correct answer",
            "You have limited time",
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
# MAIN GAME
# -------------------------
# def main():

#     if not questions:
#         return

#     score = 0
#     turn = 1
#     total = len(questions)

#     used = []

#     while turn <= total:

#         q = random.choice([x for x in questions if x not in used])
#         used.append(q)

#         question = q["question"]

#         options = q["options"].copy()
#         random.shuffle(options)

#         correct = q["answer"]

#         timer = 10
#         max_time = 10

#         answered = False
#         selected = None

#         while timer > 0:

#             dt = clock.tick(60) / 1000
#             timer -= dt

#             w, h = screen.get_size()

#             screen.fill(BG)

#             # score
#             screen.blit(font.render(f"Score: {score}", True, TEXT), (20, 20))

#             qc = font.render(f"{turn}/{total}", True, TEXT)
#             screen.blit(qc, (w - qc.get_width() - 20, 20))

#             draw_timer_bar(timer, max_time)

#             # question
#             q_rect = pygame.Rect(w * 0.2, h * 0.25, w * 0.6, 120)
#             pygame.draw.rect(screen, CARD, q_rect, border_radius=10)

#             draw_wrapped_text(question, q_rect, big_font, TEXT)

#             # buttons
#             buttons = [
#                 Button((w*0.15, h*0.5, w*0.3, 70), options[0]),
#                 Button((w*0.55, h*0.5, w*0.3, 70), options[1]),
#                 Button((w*0.15, h*0.65, w*0.3, 70), options[2]),
#                 Button((w*0.55, h*0.65, w*0.3, 70), options[3]),
#             ]

#             for i, b in enumerate(buttons):

#                 if answered:

#                     if options[i] == correct:
#                         b.color = GREEN

#                     elif i == selected:
#                         b.color = RED

#                 b.draw()

#             pygame.display.flip()

#             for event in pygame.event.get():

#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return

#                 if event.type == pygame.VIDEORESIZE:
#                     pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

#                 if event.type == pygame.MOUSEBUTTONDOWN and not answered:

#                     pos = pygame.mouse.get_pos()

#                     for i, b in enumerate(buttons):

#                         if b.clicked(pos):

#                             selected = i
#                             answered = True

#                             if options[i] == correct:
#                                 score += 1

#                             pygame.time.delay(900)

#                             timer = 0

#         turn += 1
def main():

    if not questions:
        return

    score = 0
    turn = 1
    total = len(questions)

    used = []

    while turn <= total:

        q = random.choice([x for x in questions if x not in used])
        used.append(q)

        question = q["question"]

        options = q["options"].copy()
        random.shuffle(options)

        correct = q["answer"]

        timer = 10
        max_time = 10

        answered = False
        selected = None
        feedback_timer = 0

        while True:

            dt = clock.tick(60) / 1000

            if not answered:
                timer -= dt
            else:
                feedback_timer -= dt

            w, h = screen.get_size()
            screen.fill(BG)

            # score
            screen.blit(font.render(f"Score: {score}", True, TEXT), (20, 20))

            qc = font.render(f"{turn}/{total}", True, TEXT)
            screen.blit(qc, (w - qc.get_width() - 20, 20))

            draw_timer_bar(timer, max_time)

            # question
            q_rect = pygame.Rect(w * 0.2, h * 0.25, w * 0.6, 120)
            pygame.draw.rect(screen, CARD, q_rect, border_radius=10)

            draw_wrapped_text(question, q_rect, big_font, TEXT)

            # buttons
            buttons = [
                Button((w*0.15, h*0.5, w*0.3, 70), options[0]),
                Button((w*0.55, h*0.5, w*0.3, 70), options[1]),
                Button((w*0.15, h*0.65, w*0.3, 70), options[2]),
                Button((w*0.55, h*0.65, w*0.3, 70), options[3]),
            ]

            # for i, b in enumerate(buttons):

            #     if answered:

            #         if options[i] == correct:
            #             pygame.draw.rect(screen, GREEN, b.rect, border_radius=12)

            #         elif i == selected:
            #             pygame.draw.rect(screen, RED, b.rect, border_radius=12)

            #     b.draw()
            for i, b in enumerate(buttons):

                color_override = None

                if answered:

                    if options[i] == correct:
                        color_override = GREEN

                    elif i == selected:
                        color_override = RED

                b.draw(color_override)

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.MOUSEBUTTONDOWN and not answered:

                    pos = pygame.mouse.get_pos()

                    for i, b in enumerate(buttons):

                        if b.clicked(pos):

                            selected = i
                            answered = True
                            feedback_timer = 1.0   # show result for 1 second

                            if options[i] == correct:
                                score += 1

            # next question after feedback
            if answered and feedback_timer <= 0:
                break

            # time up
            if timer <= 0 and not answered:
                answered = True
                feedback_timer = 1.0

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