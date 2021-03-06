import pygame
from Interface_GUI import Interface_GUI
import os
import pickle
import classes
from stats import Stats
from copy import deepcopy


width_w = 1000
height_w = 700

#green = (36, 143, 46)




def center_text(text, list):
    x = list[0]
    y = list[1]
    w = list[2]
    h = list[3]
    return text.get_rect(center=(int(x + 0.5 * w), int(y + 0.5 * h)))

class Menu(object):
    def __init__(self):
        self.num_decs = 1
        self.hotseat = False
        self.players = 2
        self.paused = False
        self.can_load = os.path.isfile('./save')
        self.time = 5
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 25)
        self.font_arrow = pygame.font.Font("OpenSans-Regular.ttf", 20)
        self.font_color = (0, 0, 0)
        self.basic_col = (29, 59, 207)
        self.up_col = (29, 186, 207)
        self.down_col = (29, 207, 56)
        self.width_rect = 250
        self.height_rect = 50
        self.center_x = int((width_w - self.width_rect) / 2)
        self.dist = 30
        self.bet = 10

        self.y_start = int(
            (height_w - 6 * self.height_rect - 5 * self.dist) / 2)  # 4 - liczba poziomych przycisków do wysrodkowania
        self.y_bet = self.y_start + self.dist + self.height_rect
        self.y_deck = self.y_start + 2 * (self.dist + self.height_rect)
        self.y_hotseat = self.y_start + 3 * (self.dist + self.height_rect)
        self.y_players = self.y_start + 4 * (self.dist + self.height_rect)
        self.y_stats = self.y_start + 5 * (self.dist + self.height_rect)

        self.up_down = int(self.height_rect / 2)  # wysokść up_down
        self.up_down_x = self.center_x + self.width_rect - self.up_down * 2

        self.button_load = pygame.Rect(self.center_x, self.y_start - 100, self.width_rect, self.height_rect)

        self.button_start = pygame.Rect(self.center_x, self.y_start, self.width_rect, self.height_rect)
        self.button_bet = pygame.Rect(self.center_x, self.y_bet, self.width_rect - self.up_down * 2, self.height_rect)
        self.button_bet_up = pygame.Rect(self.up_down_x, self.y_bet, self.up_down * 2, self.up_down)
        self.button_bet_down = pygame.Rect(self.up_down_x, self.y_bet + self.up_down, self.up_down * 2, self.up_down)

        self.button_deck = pygame.Rect(self.center_x, self.y_deck, self.width_rect - self.up_down * 2, self.height_rect)

        self.button_deck_up = pygame.Rect(self.up_down_x, self.y_deck, self.up_down * 2, self.up_down)
        self.button_deck_down = pygame.Rect(self.up_down_x, self.y_deck + self.up_down, self.up_down * 2, self.up_down)

        self.button_hotseat = pygame.Rect(self.center_x, self.y_hotseat, self.width_rect, self.height_rect)
        self.button_hotseat_off = pygame.Rect(self.up_down_x, self.y_hotseat, self.up_down * 2, self.up_down * 2)
        self.button_hotseat_up = pygame.Rect(self.up_down_x, self.y_hotseat, self.up_down * 2, self.up_down)
        self.button_hotseat_down = pygame.Rect(self.up_down_x, self.y_hotseat + self.up_down, self.up_down * 2, self.up_down)

        self.button_players = pygame.Rect(self.center_x, self.y_players, self.width_rect - self.up_down * 2, self.height_rect)
        self.button_players_up = pygame.Rect(self.up_down_x, self.y_players, self.up_down * 2, self.up_down)
        self.button_players_down = pygame.Rect(self.up_down_x, self.y_players + self.up_down, self.up_down * 2,
                                               self.up_down)
        self.button_stats = pygame.Rect(self.center_x, self.y_stats, self.width_rect, self.height_rect)

        #self.button_resume = pygame.Rect(self.center_x, self.y_start - 100, self.width_rect, self.height_rect)

    def draw(self, window):
        if os.path.isfile('./save'):
            pygame.draw.rect(window, self.basic_col, self.button_load)
            text_load = self.font.render('Load last game', True, self.font_color)
            window.blit(text_load, center_text(text_load, self.button_load))

        pygame.draw.rect(window, self.basic_col, self.button_start)

        pygame.draw.rect(window, self.basic_col, self.button_bet)
        pygame.draw.rect(window, self.up_col, self.button_bet_up)
        pygame.draw.rect(window, self.down_col, self.button_bet_down)

        pygame.draw.rect(window, self.basic_col, self.button_deck)
        pygame.draw.rect(window, self.up_col, self.button_deck_up)
        pygame.draw.rect(window, self.down_col, self.button_deck_down)
        pygame.draw.rect(window, self.basic_col, self.button_hotseat)
        pygame.draw.rect(window, self.basic_col, self.button_players)
        pygame.draw.rect(window, self.up_col, self.button_players_up)
        pygame.draw.rect(window, self.down_col, self.button_players_down)
        pygame.draw.rect(window, self.basic_col, self.button_stats)

        text_start = self.font.render('Start', True, self.font_color)
        text_bet = self.font.render("Bet " + str(self.bet) +"$", True, self.font_color)
        text_bet_up = self.font_arrow.render('↑', True, self.font_color)
        text_bet_down = self.font_arrow.render('↓', True, self.font_color)
        text_players_up = self.font_arrow.render('↑', True, self.font_color)
        text_players_down = self.font_arrow.render('↓', True, self.font_color)
        if self.players == 1:
            text_players = self.font.render('1 Player', True, self.font_color)
        else:
            text_players = self.font.render(str(self.players) + ' Players', True, self.font_color)
        window.blit(text_players_up, center_text(text_players_up, self.button_players_up))
        window.blit(text_players_down, center_text(text_players_down, self.button_players_down))

        if self.num_decs == 1:
            text_deck = self.font.render('1 Deck', True, self.font_color)
        else:
            text_deck = self.font.render(str(self.num_decs) + ' Decks', True, self.font_color)
        text_deck_up = self.font_arrow.render('↑', True, self.font_color)
        text_deck_down = self.font_arrow.render('↓', True, self.font_color)
        text_hotseat_up = self.font_arrow.render('↑', True, self.font_color)
        text_hotseat_down = self.font_arrow.render('↓', True, self.font_color)
        if not self.hotseat:
            text_hotseat = self.font.render('Time limit: OFF', True, self.font_color)
        else:
            text_hotseat = self.font.render('Time limit: ' + str(self.time) + "s", True, self.font_color)
            pygame.draw.rect(window, self.up_col, self.button_hotseat_up)
            pygame.draw.rect(window, self.down_col, self.button_hotseat_down)
            window.blit(text_hotseat_up, center_text(text_hotseat_up, self.button_hotseat_up))
            window.blit(text_hotseat_down, center_text(text_hotseat_down, self.button_hotseat_down))
        text_stats = self.font.render('Stats', True, self.font_color)

        window.blit(text_start, center_text(text_start, self.button_start))
        window.blit(text_bet, center_text(text_bet, self.button_bet))
        window.blit(text_bet_up, center_text(text_bet_up, self.button_bet_up))
        window.blit(text_bet_down, center_text(text_bet_down, self.button_bet_down))
        window.blit(text_deck, center_text(text_deck, self.button_deck))
        window.blit(text_deck_up, center_text(text_deck_up, self.button_deck_up))
        window.blit(text_deck_down, center_text(text_deck_down, self.button_deck_down))
        window.blit(text_hotseat, center_text(text_hotseat, self.button_hotseat))
        window.blit(text_players, center_text(text_players, self.button_players))
        window.blit(text_stats, center_text(text_stats, self.button_stats))

    def check_all_buttons(self, pos, window):

        if self.can_load and self.click(self.button_load, pos[0], pos[1]):
            list_all = pickle.load(open("save", "rb"))
            list = list_all[-1]
            interface_GUI = Interface_GUI(list[5], list[6], window, self.time, list[7])
            interface_GUI.game = list[0]
            interface_GUI.time_left = list[4]
            interface_GUI.current_player = list[8]
            return("load", interface_GUI, list, list_all)

        if self.click(self.button_start, pos[0], pos[1]):
            classes.NUM_PLAYERS = self.players
            classes.NUM_DECKS = self.num_decs
            classes.DEFAULT_BET = deepcopy([self.bet])
            interface_GUI = Interface_GUI(self.num_decs, self.hotseat, window, self.time, self.bet)
            #game.start_game()
            print("start game")
            return ("start", interface_GUI)       ##############
        if self.click(self.button_bet_up, pos[0], pos[1]):
            if self.bet < 1000:
                self.bet += 20
            print("bet:", self.bet)
            return("", 1)
        if self.click(self.button_bet_down, pos[0], pos[1]):
            if self.bet > 10:
                self.bet -= 20
            print("bet:", self.bet)

            return ("", 1)
        if self.click(self.button_deck_up, pos[0], pos[1]):
            if self.num_decs < 8:
                self.num_decs += 1
            print("number of decks:", self.num_decs)
            return("", 1)
        if self.click(self.button_deck_down, pos[0], pos[1]):
            if self.num_decs > 1:
                self.num_decs -= 1
            print("number of decks:", self.num_decs)
            return ("", 1)
        if self.click(self.button_hotseat, pos[0], pos[1]):
            self.hotseat = not (self.hotseat)
            if self.hotseat:
                self.players = 1
                self.button_hotseat = pygame.Rect(self.center_x, self.y_hotseat, self.width_rect-2*self.up_down, self.height_rect)
            else:
                self.button_hotseat = pygame.Rect(self.center_x, self.y_hotseat, self.width_rect, self.height_rect)
            return ("", 1)

        if self.click(self.button_hotseat_up, pos[0], pos[1]):
            if self.time < 200:
                self.time += 1
            return ("", 1)
        if self.click(self.button_hotseat_down, pos[0], pos[1]):
            if self.time > 1:
                self.time -= 1
            return ("", 1)
        if self.click(self.button_players_up, pos[0], pos[1]):
            if self.players < 4 and not self.hotseat:
                self.players += 1
            return ("", 1)
        if self.click(self.button_players_down, pos[0], pos[1]):
            if self.players > 1:
                self.players -= 1
            return ("", 1)
        if self.click(self.button_stats, pos[0], pos[1]):
            print("go to stats(w przygotowaniu)")
            if os.path.isfile('./stats'):
                stats = Stats(pickle.load(open("stats", "rb")), window)
            else:
                stats = Stats([[0,0,0]], window)
            return ("stats", stats)
        if self.paused and self.click(self.button_resume, pos[0], pos[1]):
            game.resume()
            print("resuming")
            return ("", 1)
        else:
            return("", 0)

    def click(self, button, x, y):
        if button.x < x < button.x + button.w and button.y < y < button.y + button.h:
            # print("d")
            return True



    def add_resume_button(self):
        self.paused = True


class Game:
    def __init__(self):
        self.ms_max = 50.0
        pygame.init()
        self.window = pygame.display.set_mode((width_w, height_w))
        self.time = 0.0
        self.clock = pygame.time.Clock()
        self.work = True
        self.in_menu = True
        self.in_game = False
        self.menu = Menu()

    def main_loop(self):
        while self.work:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.work = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.in_menu:
                        self.menu.check_all_buttons(event.pos)
                    elif self.in_game:
                        game.pause()
                        print("pause")
                        # self..check_all_buttons(event.pos)

                    # print("klawisz myszki", event.button, "wcisniety na poz", event.pos)

            # ograniczenie ilości klatek

            self.time += self.clock.tick()
            if self.time >= self.ms_max:
                self.time = 0.0
                self.tick()
            self.draw()

    def start_game(self):
        self.in_menu = False
        self.in_game = True
        # ...........

    def pause(self):
        self.in_game = False
        self.in_menu = True
        self.menu.add_resume_button()

    def resume(self):
        self.in_game = True
        self.in_menu = False

    def tick(self):
        self.window.fill(green)

    def draw(self):
        if self.in_menu:
            self.menu.draw(self.window)
        pygame.display.flip()


print("dziala2")
if __name__ == "__main__":
    print("dziala")
    game = Game()
    game.main_loop()