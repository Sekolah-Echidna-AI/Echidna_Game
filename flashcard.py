import pygame
import sys
import json
import tkinter as tk
from tkinter import filedialog
import asyncio

pygame.init()

SCREEN = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption("Quiz App")

BG_COLOUR = "#0a092d"
FLASHCARD_COLOUR = "#2e3856"
FLIPPED_COLOUR = "#595e6d"
BUTTON_COLOR = "#3b82f6"

# -------------------------
# QUIZ DATA DEFAULT
# -------------------------
quiz_data = {
    "Ibukota Indonesia adalah?": "Jakarta",
    "Siapa penemu teori relativitas?": "Albert Einstein"
}

questions = list(quiz_data.keys())
answers = list(quiz_data.values())

index = 0
card_turned = False
show_help = False


# -------------------------
# LOAD JSON FUNCTION
# -------------------------
def load_json():

    global quiz_data, questions, answers, index, card_turned

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json")]
    )

    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            quiz_data = json.load(f)

        questions = list(quiz_data.keys())
        answers = list(quiz_data.values())
        index = 0
        card_turned = False


# -------------------------
# TEXT WRAP
# -------------------------
def render_wrapped_text(text, font, color, rect):

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:

        test_line = current_line + word + " "
        width, _ = font.size(test_line)

        if width < rect.width - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    rendered = []
    for line in lines:
        rendered.append(font.render(line.strip(), True, color))

    return rendered


# -------------------------
# DRAW BUTTON
# -------------------------
def draw_button(surface, rect, text, font):

    pygame.draw.rect(surface, BUTTON_COLOR, rect, border_radius=8)

    label = font.render(text, True, "white")
    label_rect = label.get_rect(center=rect.center)

    surface.blit(label, label_rect)


# -------------------------
# MAIN LOOP
# -------------------------
async def main():
    index = 0
    card_turned = False
    show_help = False
    while True:

        width, height = SCREEN.get_size()

        FONT = pygame.font.SysFont("Arial", int(height * 0.045))
        BUTTON_FONT = pygame.font.SysFont("Arial", int(height * 0.03))

        button_w = width * 0.12
        button_h = height * 0.05

        help_button = pygame.Rect(
            width * 0.02,
            height * 0.02,
            button_w,
            button_h
        )

        import_button = pygame.Rect(
            width - button_w - width * 0.02,
            height * 0.02,
            button_w,
            button_h
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if help_button.collidepoint(event.pos):
                    show_help = True

                if import_button.collidepoint(event.pos):
                    load_json()

            if event.type == pygame.KEYDOWN:

                if show_help:
                    if event.key == pygame.K_ESCAPE:
                        show_help = False
                    continue

                if event.key == pygame.K_SPACE:
                    card_turned = not card_turned

                elif event.key == pygame.K_RIGHT and index < len(questions) - 1:
                    index += 1
                    card_turned = False

                elif event.key == pygame.K_LEFT and index > 0:
                    index -= 1
                    card_turned = False

        SCREEN.fill(BG_COLOUR)

        # -------------------------
        # HELP SCREEN
        # -------------------------
        if show_help:

            title_font = pygame.font.SysFont("Arial", int(height * 0.07))
            text_font = pygame.font.SysFont("Arial", int(height * 0.045))

            title = title_font.render("Controls", True, "white")
            SCREEN.blit(title, title.get_rect(center=(width / 2, height * 0.2)))

            controls = [
                "SPACE  : Flip card (question / answer)",
                "LEFT   : Previous card",
                "RIGHT  : Next card",
                "ESC    : Close help screen"
            ]

            for i, line in enumerate(controls):

                txt = text_font.render(line, True, "white")
                SCREEN.blit(
                    txt,
                    txt.get_rect(center=(width / 2, height * (0.4 + i * 0.1)))
                )

            pygame.display.update()
            continue

        # -------------------------
        # CARD SIZE
        # -------------------------
        card_w = width * 0.7
        card_h = height * 0.4

        card_x = (width - card_w) / 2
        card_y = (height - card_h) / 2

        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

        if not card_turned:
            text = questions[index]
            color = FLASHCARD_COLOUR
        else:
            text = answers[index]
            color = FLIPPED_COLOUR

        pygame.draw.rect(SCREEN, color, card_rect, border_radius=15)

        lines = render_wrapped_text(text, FONT, "white", card_rect)

        total_h = len(lines) * FONT.get_height()
        start_y = card_rect.centery - total_h / 2

        for i, line in enumerate(lines):

            rect = line.get_rect(
                center=(width / 2, start_y + i * FONT.get_height())
            )

            SCREEN.blit(line, rect)

        # -------------------------
        # INDEX TEXT
        # -------------------------
        idx_font = pygame.font.SysFont("Arial", int(height * 0.03))

        idx_text = idx_font.render(
            f"{index+1}/{len(questions)}",
            True,
            "white"
        )

        SCREEN.blit(idx_text, (width * 0.48, height * 0.9))

        # -------------------------
        # BUTTONS
        # -------------------------
        draw_button(SCREEN, help_button, "Help", BUTTON_FONT)
        draw_button(SCREEN, import_button, "Import JSON", BUTTON_FONT)

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())