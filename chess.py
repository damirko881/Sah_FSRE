import pygame

from piece import Piece
from utils import Utils


class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        # površina za prikazivanje
        self.screen = screen
        # kreiraj objekt klase za prikazivanje šahovskih figura na tabli
        self.chess_pieces = Piece(pieces_src, cols=6, rows=2)
        # čuvanje koordinate polja šahovske table
        self.board_locations = square_coords
        # dužina stranice polja šahovske table
        self.square_length = square_length
        # rječnik za praćenje redosljeda igrača
        self.turn = {"black": 0,
                     "white": 0}

        # lista koja sadži moguće poteze za odabranu figuru
        self.moves = []
        #
        self.utils = Utils()

        # mapiranje imena figura na indekse liste koja sadrži koordinate figura na sprite sheetu-u
        self.pieces = {
            "white_pawn":   5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook":   4,
            "white_king":   0,
            "white_queen":  1,
            "black_pawn":   11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook":   10,
            "black_king":   6,
            "black_queen":  7
        }

        # lista koja sadrži zarobljene figure
        self.captured = []
        #
        self.winner = ""

        self.reset()
    
    def reset(self):
        # očisti liste poteza
        self.moves = []

        # slučajno određivanje redosljeda igrača
        x = 0
        if(x == 1):
            self.turn["black"] = 1
        elif(x == 0):
            self.turn["white"] = 1

        # Dvodimenzionalni rječnik koji sadrži detalje o svakom polju na ploči
        # format pohrane je [piece_name, currently_selected, x_y_coordinate]
        self.piece_location = {}
        x = 0
        for i in range(97, 105):
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a>0:
                # [piece name, currently selected, board coordinates]
                self.piece_location[chr(i)][a] = ["", False, [x,y]]
                a = a - 1
                y = y + 1
            x = x + 1

        # Resetiranje ploče
        for i in range(97, 105): #ASSCI vrijednost 'a' do 'h'
            x = 8
            while x>0:
                if(x==8):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "black_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "black_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "black_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "black_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "black_king"
                elif(x==7):
                    self.piece_location[chr(i)][x][0] = "black_pawn"
                elif(x==2):
                    self.piece_location[chr(i)][x][0] = "white_pawn"
                elif(x==1):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "white_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "white_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "white_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "white_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "white_king"
                x = x - 1


    # 
    def play_turn(self):
        # bijela boja
        white_color = (255, 255, 255)
        # kreiranje fontova za tekstove
        small_font = pygame.font.SysFont("comicsansms", 20)
        # kreiranje teksta koji će se prikazati na igračevom meniju
        if self.turn["black"]:
            turn_text = small_font.render("Igra: Crni", True, white_color)
        elif self.turn["white"]:
            turn_text = small_font.render("Igra: Bijeli", True, white_color)
        
        # prikazivanje teksta dobrodošlice
        self.screen.blit(turn_text, 
                      ((self.screen.get_width() - turn_text.get_width()) // 2,
                      10))
        
        # dopusti igraču s crnim figurama da igra
        if(self.turn["black"]):
            self.move_piece("black")
        # dopusti igraču s bjelim figurama da igra
        elif(self.turn["white"]):
            self.move_piece("white")

    # metoda za crtanje figura na šahovskoj ploči
    def draw_pieces(self):
        transparent_green = (0,194,39,170)
        transparent_blue = (28,21,212,170)

        # kreiranje transparenten površine
        surface = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_green)

        surface1 = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_blue)

        # petlja za promjenu boje pozadine odabrane figure
        for val in self.piece_location.values():
            for value in val.values() :
                # ime figure na trenutnoj lokaciji
                piece_name = value[0]
                # x, y koordinate trenutne figure
                piece_coord_x, piece_coord_y = value[2]

                # promjena boje pozadine figure ako je odabrano
                if value[1] and len(value[0]) > 5:
                    # ako je odabrana crna figura
                    if value[0][:5] == "black":
                        self.screen.blit(surface, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface, self.board_locations[x_coord][y_coord])
                    # ako je odabrana bijela figura
                    elif value[0][:5] == "white":
                        self.screen.blit(surface1, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface1, self.board_locations[x_coord][y_coord])
        
        # crtanje svih figura na šahovskoj ploči
        for val in self.piece_location.values():
            for value in val.values() :
                # ime figure na trenutnoj lokaciji
                piece_name = value[0]
                # x, y koordinate trenutne figure
                piece_coord_x, piece_coord_y = value[2]
                # provjeri da li postoji figura na kvadratu
                if(len(value[0]) > 1):
                    # nacrtaj figuru na ploči
                    self.chess_pieces.draw(self.screen, piece_name, 
                                            self.board_locations[piece_coord_x][piece_coord_y])


    # metoda za pronalaženje mogućih poteza odabrane figure
    def possible_moves(self, piece_name, piece_coord):
        # lista za pohranu mjesta za postavljanje figure
        positions = []
        # pronađi moguća mjesta za postavljanje figure
        if len(piece_name) > 0:
            # dobij x, y koordinatu
            x_coord, y_coord = piece_coord
            # izračunaj poteze za lovca
            if piece_name[6:] == "bishop":
                positions = self.diagonal_moves(positions, piece_name, piece_coord)
            
            #  izračunaj poteze za pijuna
            elif piece_name[6:] == "pawn":
                # pretvori indeks liste u ključ rječnika
                columnChar = chr(97 + x_coord)
                rowNo = 8 - y_coord

                # izračunaj poteze za crnog pijuna
                if piece_name == "black_pawn":
                    if y_coord + 1 < 8:
                        # dobij redak ispred crnog pijuna
                        rowNo = rowNo - 1
                        front_piece = self.piece_location[columnChar][rowNo][0]
                
                        # pijuni ne mogu potezati kada ih blokira drugi pijun
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord+1])
                            # crni pijuni mogu potezati dva polja unaprijed za prvi potez
                            if y_coord < 2:
                                positions.append([x_coord, y_coord+2])

                        # EM PASSANT
                        # dijagonalno lijevo
                        if x_coord - 1 >= 0 and y_coord + 1 < 8:
                            x = x_coord - 1
                            y = y_coord + 1
                            
                            # pretvori indeks liste u ključ rječnika
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                        # dijagonalno desno
                        if x_coord + 1 < 8  and y_coord + 1 < 8:
                            x = x_coord + 1
                            y = y_coord + 1

                            # pretvori indeks liste u ključ rječnika
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                # izračunaj poteze za bijelog pijuna
                elif piece_name == "white_pawn":
                    if y_coord - 1 >= 0:
                        # dobij redak ispred bijelog pijuna
                        rowNo = rowNo + 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # pijuni ne mogu potezati kada ih blokira drugi pijun
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord-1])
                            # bijeli pijuni mogu potezati dva polja unaprijed za prvi potez
                            if y_coord > 5:
                                positions.append([x_coord, y_coord-2])

                        # EM PASSANT
                        # dijagonalno lijevo
                        if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                            x = x_coord - 1
                            y = y_coord - 1
                            
                            #pretvori indeks liste u ključ rječnika
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])

                            
                        # dijagonalno desno
                        if x_coord + 1 < 8  and y_coord - 1 >= 0:
                            x = x_coord + 1
                            y = y_coord - 1

                            # pretvori indeks liste u ključ rječnika
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])


            # izračunaj poteze za topa
            elif piece_name[6:] == "rook":
                #pronađi linearne poteze
                positions = self.linear_moves(positions, piece_name, piece_coord)

            #izračunaj poteze za konja
            elif piece_name[6:] == "knight":
                #lijevi potezi
                if(x_coord - 2) >= 0:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-2, y_coord+1])
                # gornji potezi
                if(y_coord - 2) >= 0:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord-2])
                # desni potezi
                if(x_coord + 2) < 8:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+2, y_coord+1])
                # donji potezi
                if(y_coord + 2) < 8:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord+2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+2])

            #  izračunaj poteze za kralja
            elif piece_name[6:] == "king":
                if(y_coord - 1) >= 0:
                    #  gornje mjesto
                    positions.append([x_coord, y_coord-1])

                if(y_coord + 1) < 8:
                    # donje mjesto
                    positions.append([x_coord, y_coord+1])

                if(x_coord - 1) >= 0:
                    # lijevo mjesto
                    positions.append([x_coord-1, y_coord])
                    # gornje lijevo mjesto
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-1])
                    # donje lijevo mjesto
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-1, y_coord+1])
                    
                if(x_coord + 1) < 8:
                    # desno mjesto
                    positions.append([x_coord+1, y_coord])
                    # gornje desno mjesto
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+1, y_coord-1])
                    # donje desno mjesto
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+1])
                
            # izračunaj poteze za kraljicu
            elif piece_name[6:] == "queen":
                # pronađi dijagonalne pozicije
                positions = self.diagonal_moves(positions, piece_name, piece_coord)

                # pronađi linearne poteze
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # lista pozicija koje treba ukloniti
            to_remove = []

            # ukloni pozicije koje se preklapaju s drugim figurama trenutnog igrača
            for pos in positions:
                x, y = pos

                # pretvori indeks liste u ključ rječnika
                columnChar = chr(97 + x)
                rowNo = 8 - y

                # pronađi figure za uklanjanje
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if(des_piece_name[:5] == piece_name[:5]):
                    to_remove.append(pos)

            # ukloni poziciju iz liste pozicija
            for i in to_remove:
                positions.remove(i)

        # vrati listu koja sadrži moguće poteze za odabranu figuru
        return positions


    def move_piece(self, turn):
        # dohvati koordinate odabranog kvadrata na ploči
        square = self.get_selected_square()

        # ako je kvadrat odabran
        if square:
            # dohvati ime figure na odabranom kvadratu
            piece_name = square[0]
            # boja figure na odabranom kvadratu
            piece_color = piece_name[:5]
            # slovo stupca na ploči
            columnChar = square[1]
            # redni broj retka na ploči
            rowNo = square[2]

            # dohvati x, y koordinate
            x, y = self.piece_location[columnChar][rowNo][2]

            # ako postoji figura na odabranom kvadratu
            if(len(piece_name) > 0) and (piece_color == turn):
                # pronađi moguće poteze za figuru
                self.moves = self.possible_moves(piece_name, [x,y])

            #  mehanizam šaha
            p = self.piece_location[columnChar][rowNo]

            for i in self.moves:
                if i == [x, y]:
                    if(p[0][:5] == turn) or len(p[0]) == 0:
                        self.validate_move([x,y])
                    else:
                        self.capture_piece(turn, [columnChar, rowNo], [x,y])

            # osamo igrač s rednim redkom može igrati
            if(piece_color == turn):
                # promijeni oznaku odabira za sve druge figure
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][1] = False

                # promijeni oznaku odabira za odabranu figuru
                self.piece_location[columnChar][rowNo][1] = True
                
            
    def get_selected_square(self):
        # get left event
        left_click = self.utils.left_click_event()

        # if there's a mouse event
        if left_click:
            # get mouse event
            mouse_event = self.utils.get_mouse_event()

            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(self.board_locations[i][j][0], self.board_locations[i][j][1], 
                            self.square_length, self.square_length)
                    collision = rect.collidepoint(mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        # find x, y coordinates the selected square
                        for k in range(len(self.board_locations)):
                            #
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    #reset color of all selected pieces
                                    for val in self.piece_location.values():
                                        for value in val.values() :
                                            # [piece name, currently selected, board coordinates]
                                            if not value[1]:
                                                value[1] = False

                                    # get column character and row number of the chess piece
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    # get the name of the 
                                    piece_name = self.piece_location[columnChar][rowNo][0]
                                    
                                    return [piece_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None


    def capture_piece(self, turn, chess_board_coord, piece_coord):
        # get x, y coordinate of the destination piece
        x, y = piece_coord

        # get chess board coordinate
        columnChar, rowNo = chess_board_coord

        p = self.piece_location[columnChar][rowNo]
        
        if p[0] == "white_king":
            self.winner = "Crni"
            print("Crni je pobijedio")
        elif p[0] == "black_king":
            self.winner = "Bijeli"
            print("Bijeli je pobijedio")

        # add the captured piece to list
        self.captured.append(p)
        # move source piece to its destination
        self.validate_move(piece_coord)


    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]

        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]

                if board_piece[1]:
                    # unselect the source piece
                    self.piece_location[k][key][1] = False
                    # get the name of the source piece
                    piece_name = self.piece_location[k][key][0]
                    # move the source piece to the destination piece
                    self.piece_location[desColChar][desRowNo][0] = piece_name
                    
                    src_name = self.piece_location[k][key][0]
                    # remove source piece from its current position
                    self.piece_location[k][key][0] = ""

                    # change turn
                    if(self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif("white"):
                        self.turn["black"] = 1
                        self.turn["white"] = 0

                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print("{} moved from {} to {}".format(src_name,  src_location, des_location))


    # helper function to find diagonal moves
    def diagonal_moves(self, positions, piece_name, piece_coord):
        # reset x and y coordinate values
        x, y = piece_coord
        # find top left diagonal spots
        while(True):
            x = x - 1
            y = y - 1
            if(x < 0 or y < 0):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom right diagonal spots
        while(True):
            x = x + 1
            y = y + 1
            if(x > 7 or y > 7):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom left diagonal spots
        while(True):
            x = x - 1
            y = y + 1
            if (x < 0 or y > 7):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find top right diagonal spots
        while(True):
            x = x + 1
            y = y - 1
            if(x > 7 or y < 0):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        return positions
    

    # helper function to find horizontal and vertical moves
    def linear_moves(self, positions, piece_name, piece_coord):
        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the left
        while(x > 0):
            x = x - 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
                    

        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the right
        while(x < 7):
            x = x + 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break    

        # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves upwards
        while(y > 0):
            y = y - 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves downwards
        while(y < 7):
            y = y + 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break


        return positions