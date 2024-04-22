import pygame
import sys
import random
from words import *

pygame.init()       #initializes all the modules

# Constants

width, height = 600, 800

SCREEN = pygame.display.set_mode((width, height))
background = pygame.image.load("Starting Tiles.png")
background_rect = background.get_rect(center=(318, 300))
icon = pygame.image.load("icon.png")

pygame.display.set_caption("Wordle")
pygame.display.set_icon(icon)

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

words_for_guess =['reach']

CORRECT_WORD = random.choice(words_for_guess).lower()

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("FreeSansBold.otf", 25)

SCREEN.fill("white")
SCREEN.blit(background, background_rect)
pygame.display.update()

LETTER_X_SPAC = 85
LETTER_Y_SPAC = 12
LETTER_SIZE = 75

# Global variables

guesses_count = 0

# guesses is a 2D list that will store guesses. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[] for _ in range(6)]


curr_guess = []
curr_guess_str = ""
current_letter_bg_x = 110

# keyboard_letters is a list stor all the keyboard object. An keyboard is that button th with all the letters you see.
keyboard_letters = []

result = ""

class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, includ text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, empty it.
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pygame.display.update()

class keyboard:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 50, 50)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the keyboard and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+25))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

# Draw the keyboard_letters on the screen.

keyboard_x, keyboard_y = 15, 600

for i in range(3):
    for letter in ALPHABET[i]:
        new_keyboard = keyboard(keyboard_x, keyboard_y, letter)
        keyboard_letters.append(new_keyboard)
        new_keyboard.draw()
        keyboard_x += 55
    keyboard_y += 60
    if i == 0:
        keyboard_x = 50
    elif i == 1:
        keyboard_x = 105

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global curr_guess, curr_guess_str, guesses_count, current_letter_bg_x, result
    game_decided = False
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                for keyboard in keyboard_letters:
                    if keyboard.text == lowercase_letter.upper():
                        keyboard.bg_color = GREEN
                        keyboard.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                for keyboard in keyboard_letters:
                    if keyboard.text == lowercase_letter.upper():
                        keyboard.bg_color = YELLOW
                        keyboard.draw()
                guess_to_check[i].text_color = "white"
                result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            for keyboard in keyboard_letters:
                if keyboard.text == lowercase_letter.upper():
                    keyboard.bg_color = GREY
                    keyboard.draw()
            guess_to_check[i].text_color = "white"
            result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()
    
    guesses_count += 1
    curr_guess = []
    curr_guess_str = ""
    current_letter_bg_x = 110

    if guesses_count == 6 and result == "":
        result = "L"

def play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(width/2, 700))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD.upper()}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(width/2, 650))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, curr_guess, curr_guess_str, result
    SCREEN.fill("white")
    SCREEN.blit(background, background_rect)
    guesses_count = 0
    CORRECT_WORD = random.choice(words_for_guess).lower()
    guesses = [[] for _ in range(6)]
    curr_guess = []
    curr_guess_str = ""
    result = ""
    pygame.display.update()
    for keyboard in keyboard_letters:
        keyboard.bg_color = OUTLINE
        keyboard.draw()

def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global curr_guess_str, current_letter_bg_x
    curr_guess_str += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count*100+LETTER_Y_SPAC))
    current_letter_bg_x += LETTER_X_SPAC
    guesses[guesses_count].append(new_letter)
    curr_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global curr_guess_str, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    curr_guess_str = curr_guess_str[:-1]
    curr_guess.pop()
    current_letter_bg_x -= LETTER_X_SPAC

while True:
    if result != "":
        play_again()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if result != "":
                    reset()
                else:
                    if len(curr_guess_str) == 5 and curr_guess_str.upper() in WORDS:
                        check_guess(curr_guess)

            elif event.key == pygame.K_BACKSPACE:
                if len(curr_guess_str) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(curr_guess_str) < 5:
                        create_new_letter()
                        