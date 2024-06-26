import os
import pygame
from pygame.locals import *
from piece import Piece
from chess import Chess
from utils import Utils

class Game:
    def __init__(self):
        # dimenzija ekrana
        screen_width = 640
        screen_height = 750
        # zastavica da znamo jel prikazan menu igre
        self.menu_showed = False
        # zastavica za postavljanje petlje igre
        self.running = True
        # osnovna mapa za programske resurse
        self.resources = "res"
 
        # inicijalizirati prozor igre
        pygame.display.init()
        # inicijalizirati font za tekst
        pygame.font.init()

        # napravi prozor igre
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        # naslov prozora
        window_title = "Šah"
        # postavka naslova prozora
        pygame.display.set_caption(window_title)

        # lokacije ikone igre
        icon_src = os.path.join(self.resources, "chess_icon.png")
        # ucitavanje ikone igre
        icon = pygame.image.load(icon_src)
        # postavka ikone igre
        pygame.display.set_icon(icon)
        # azuriraj prikaz
        pygame.display.flip()
        # namjesti sat igre
        self.clock = pygame.time.Clock()


    def start_game(self):
        """Function containing main game loop""" 
        # offset sahovske ploce
        self.board_offset_x = 0
        self.board_offset_y = 50
        self.board_dimensions = (self.board_offset_x, self.board_offset_y)
        
        # lokacija slike sahovske ploce
        board_src = os.path.join(self.resources, "board.png")
        # load the chess board image
        self.board_img = pygame.image.load(board_src).convert()

        # sirina kvadrata sahovske ploce
        square_length = self.board_img.get_rect().width // 8

        # inicijalizirati popis koji pohranjuje sva mjesta za postavljanje šahovskih figura na ploču
        self.board_locations = []

        # izracunaj koordinate svakog polja na ploci
        for x in range(0, 8):
            self.board_locations.append([])
            for y in range(0, 8):
                self.board_locations[x].append([self.board_offset_x+(x*square_length), 
                                                self.board_offset_y+(y*square_length)])

        # lokacija slike koja ima figura
        pieces_src = os.path.join(self.resources, "pieces.png")
        # stvoriti objekt klase koji upravlja logikom igranja
        self.chess = Chess(self.screen, pieces_src, self.board_locations, square_length)

        # petlja igre
        while self.running:
            self.clock.tick(5)
            # anketni događaji
            for event in pygame.event.get():
                # dohvati pritisnute tipke
                key_pressed = pygame.key.get_pressed()
                # provijeri jeli igricu zatvorio korisnik
                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    # zastavice da se izadje iz petlje igre
                    self.running = False
                elif key_pressed[K_SPACE]:
                    self.chess.reset()
            
            winner = self.chess.winner

            if self.menu_showed == False:
                self.menu()
            elif len(winner) > 0:
                self.declare_winner(winner)
            else:
                self.game()
            
            

            #self.game()
            #self.declare_winner(winner)

            # azuriraj prikaz
            pygame.display.flip()
            # azuriraj dogadjaje
            pygame.event.pump()

        # poziv metode da se zaustavi pygame
        pygame.quit()
    

    def menu(self):
        """method to show game menu"""
        # boja pozadine
        bg_color = (255, 255, 255)
        # namjesti pozadinu boje
        self.screen.fill(bg_color)
        # crna boja
        black_color = (0, 0, 0)
        # koordinate za gumb "igraj"
        start_btn = pygame.Rect(270, 300, 100, 50)
        # prikazi gumb "igraj"
        pygame.draw.rect(self.screen, black_color, start_btn)

        # bijela boja
        white_color = (255, 255, 255)
        # napravi font za tekst
        big_font = pygame.font.SysFont("Times", 50, bold=True)
        small_font = pygame.font.SysFont("Times", 20)
        # prikaz teksta na pocetnoj stranici igre
        welcome_text = big_font.render("Šah", False, black_color)
        created_by = small_font.render("Napravili: David, Josip i Damir", True, black_color)
        start_btn_label = small_font.render("Igraj", True, white_color)
        
        # prikazi tekst dobrodoslice
        self.screen.blit(welcome_text, 
                      ((self.screen.get_width() - welcome_text.get_width()) // 2, 
                      150))
        # prikaz teksta na kraju
        self.screen.blit(created_by, 
                      ((self.screen.get_width() - created_by.get_width()) // 2, 
                      self.screen.get_height() - created_by.get_height() - 100))
        # prikaz teksta na gumbu "igraj"
        self.screen.blit(start_btn_label, 
                      ((start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2, 
                      start_btn.y + (start_btn.height - start_btn_label.get_height()) // 2)))

        # dohvati pritisnute tipke
        key_pressed = pygame.key.get_pressed()
        util = Utils()

        # provijeti jeli lijeva tipka misa pritisnuta
        if util.left_click_event():
            # poziv funkcije za dobijanje odgadjaja misa
            mouse_coords = util.get_mouse_event()

            # provijeri ako je gumb "igraj" pritisnut
            if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # promijena gumba pri prelasku misa preko njega
                pygame.draw.rect(self.screen, white_color, start_btn, 3)
                
                # promijen zastavice menija
                self.menu_showed = True
            # provijerra ako je tipka "enter" pritisnuta
            elif key_pressed[K_RETURN]:
                self.menu_showed = True


    def game(self):
        # boja pozadine
        color = (0,0,0)
        # namjesti boju pozadine
        self.screen.fill(color)
        
        # prikaz ploce saha
        self.screen.blit(self.board_img, self.board_dimensions)

        # poziv self.chess.***
        self.chess.play_turn()
        # nacrtaj figure na ploci saha
        self.chess.draw_pieces()


    def declare_winner(self, winner):
        # boja pozadine
        bg_color = (255, 255, 255)
        # namjestanje boje pozadine
        self.screen.fill(bg_color)
        # crna boja
        black_color = (0, 0, 0)
        # koordinate za gumb "igraj ponovo"
        reset_btn = pygame.Rect(250, 300, 140, 50)
        # pokazi gumb za "reset"
        pygame.draw.rect(self.screen, black_color, reset_btn)

        # bijela boja
        white_color = (255, 255, 255)
        # cnapravi font za tekst
        big_font = pygame.font.SysFont("times", 50)
        small_font = pygame.font.SysFont("times", 20)

        # tekst za prikaz pobijednika
        text = winner + " je pobijedio!" 
        winner_text = big_font.render(text, False, black_color)

        # prikzi tekst na gumbu "reset"
        reset_label = "Igraj ponovo"
        reset_btn_label = small_font.render(reset_label, True, white_color)

        # tekst pobijednika
        self.screen.blit(winner_text, 
                      ((self.screen.get_width() - winner_text.get_width()) // 2, 
                      150))
        
        # tekst na gumbu "reset"
        self.screen.blit(reset_btn_label, 
                      ((reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2, 
                      reset_btn.y + (reset_btn.height - reset_btn_label.get_height()) // 2)))

        # dohvati pritsnute tipke
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # provijeri ako je lijevi gumb misa kliknut
        if util.left_click_event():
            # poziv funkcije za dogadjaj misa
            mouse_coords = util.get_mouse_event()

            # provijeri ako je gumb "reset pritisnut"
            if reset_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # promijena gumba ako je predjeno misem preko njega
                pygame.draw.rect(self.screen, white_color, reset_btn, 3)
                
                # promijena zastavice menija
                self.menu_showed = False
            # provijeri ako je gumb "enter" pritisnut
            elif key_pressed[K_RETURN]:
                self.menu_showed = False
            # resetiraj igru
            self.chess.reset()
            # ocisti pobijednika
            self.chess.winner = ""