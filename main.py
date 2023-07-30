class game:
    def __init__(self):
        # presenting the cube where the INDEX of each list is the PLACE and the first number of each list is the actual PIECE
        self.cube = [[i, 0] for i in range(20)]
        # each side the PLACES of the pieces that makes it
        self.side_pieces = {"red": [0, 3, 5, 6, 7, 4, 2, 1], "orange": [14, 16, 19, 18, 17, 15, 12, 13], "white": [2, 4, 7, 11, 19, 16, 14, 9],
                            "yellow": [0, 3, 5, 10, 17, 15, 12, 8], "blue": [2, 1, 0, 8, 12, 13, 14, 9], "green": [5, 6, 7, 11, 19, 18, 17, 10]}
        self.corners = [0, 2, 5, 7, 12, 14, 17, 19]
        for i in self.corners:
            self.cube[i] = [i,0,1]
        self.moves = {"right": "green", "left": "blue", "up": "red",
                      "down": "orange", "front": "white", "back": "yellow"}
        # the colors that each PIECE has
        self.pieces = {}
        for i in range(20):
            result = []
            for color in self.side_pieces:
                if i in self.side_pieces[color]:
                    result.append(color)
            self.pieces[i] = result

    def show(self):
        passed = []
        passed2 = []
        for color in self.side_pieces:
            print(color)
            print("_______________________________\n")
            counter = 0

            my_list = self.flip_list(self.side_pieces[color])
            for place in my_list:
                piece = self.cube[place]

                if place in self.corners:
                    if piece[0] in passed2:
                        number = 3 - piece[1] - piece[2]
                    elif piece[0] in passed:
                        number = piece[2]
                        passed2.append(piece[0])
                    else:
                        number = piece[1]
                        passed.append(piece[0])
                    print(f'{self.pieces[piece[0]][(number)]:<6}', end=" | ")
                else:
                    if piece[0] in passed:
                        number = (piece[1] + 1) % 2
                    else:
                        number = piece[1]
                        passed.append(piece[0])
                    print(f'{self.pieces[piece[0]][number]:<6}', end=" | ")

                counter += 1
                if counter == 4:
                    print(f'{color:<6}', end=" | ")
                    counter += 1
                if counter % 3 == 0:
                    print("\n_______________________________\n")

    @staticmethod
    def flip_list(list):
        return_list = list[:3]
        return_list.append(list[7])
        return_list.append(list[3])
        return_list += list[4:7][::-1]
        return return_list

    def turn(self, move, prime=False):
        mylist = self.side_pieces[self.moves[move]]
        if prime:
            mylist = mylist[::-1]
            mylist = mylist[-3:] + mylist[:-3]
        print(mylist)
        temp_corner = self.cube[mylist[0]]
        temp_edge = self.cube[mylist[1]]
        for i in range(3):
            self.cube[mylist[i*2]] = self.cube[mylist[i*2 + 2]]
            self.cube[mylist[i*2 + 1]] = self.cube[mylist[i*2 + 3]]

        self.cube[mylist[-2]] = temp_corner
        self.cube[mylist[-1]] = temp_edge

        for i in range(4):
            if move == "right" or move == "left":
                self.cube[mylist[i*2]][1] = (self.cube[mylist[i*2]][1] + 1) % 2
                self.cube[mylist[i*2]][2] = (self.cube[mylist[i*2]][2] + 1) % 2
            if move == "front" or move == "back":
                self.cube[mylist[i*2 + 1]][1] =  (self.cube[mylist[i*2 + 1]][1] + 1) % 2
                self.cube[mylist[i*2]][1] = 3 - self.cube[mylist[i*2]][1] - self.cube[mylist[i*2]][2]
            if move == "up" or move == "down":
                self.cube[mylist[i*2]][2] = 3 - self.cube[mylist[i*2]][1] - self.cube[mylist[i*2]][2]

        print(self.cube)


cube = game()
cube.turn("right",prime=False)
cube.show()
