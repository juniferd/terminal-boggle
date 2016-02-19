import random
from collections import Counter, defaultdict
from itertools import product, permutations

class Boggle(object):

    # the boggle dice
    dice = open('boggle_dice.txt').read().split()
    k_dice = {}
    for i, die in enumerate(dice):
        k_dice[i] = die

    # dictionary words
    words = open('dictionary.txt').read().split()
    dict_words = {}
    for word in words:
        # we only need to save the words that have 3-16 letters
        # why 18? in case there are any 16-letter Q words... 
        if len(word) > 2 and len(word) < 18:
            dict_words[word] = word

    
    # get the dice for instance of game
    def get_dice(self):
        game_dice = {}

        # get 16 unique dice
        while len(game_dice) < 16:
            rdie = random.randint(0,25) 
            game_dice[rdie] = Boggle.k_dice[rdie]

        return game_dice

    # get the letters for the dice
    def get_die_letters(self, dice):
        game_letters = {}

        # get random letter on each die
        for die in dice:
            rnum = random.randint(0,5)
            letter = Boggle.k_dice[die][rnum]
            game_letters[die] = letter

        return game_letters

    # shuffle and place letters on nxn board
    def layout_board(self, letters, n=4):
        layout = {}
        shuffled = []
        # print "here are the letters:\n", letters
        
        for letter in letters:
            shuffled.append(letters[letter])
        
        # print "here are the letters in a list:\n", shuffled
        random.shuffle(shuffled)

        # print "here are the letters shuffled:\n", shuffled

        # break this into chunks of 4
        layout = [shuffled[x:x+n] for x in xrange(0, len(shuffled), n)]

        return layout

    # set up the board
    def set_board(self):
        game_dice = self.get_dice()
        game_letters = self.get_die_letters(game_dice)
        board = self.layout_board(game_letters)

        return board

    # find all the possible words present on the current boggle board
    def find_all_words(self, board):
        pass

    # make a map for letters and coordinates on board
    def make_letter_maps(self, board, word):
        unpacked_board = []
        letter_map = defaultdict(list)
        user_letters = []

        ## unpacked_board is an array of sorted letters of current board ['a','b',...]
        ## letter_map is a dict of letters to coordinates {'a':[(x1,y1),(x2,y2)], 'b':[(x3,y3)],...}
        ## letter_map can have a key that holds multiple coordinates
        for i in range(0,4):
            for j in range(0,4):
                unpacked_board.append(board[i][j])
                # x,y coordinates are reversed
                coord = (j,i)
                letter_map[board[i][j]].append(coord)

        
        
        ## user_letters is array of letters users entered ['a,','b',...]
        for letter in word:
            user_letters.append(letter)

        return unpacked_board, letter_map, user_letters

    # validate segments in a given path made up of coordinates x,y
    def validate_segment(self, path):
        ## path is tuple of tuples ((x1,y1),(x2,y2),...) 

        is_valid = False

        for i in range(0,len(path)-1):
            
            A = path[i]
            B = path[i+1]

            if A != B:
            ## if two coordinates are not identical
                for a,b in zip(A,B):
                ## for x,y coordinates in point A and B

                    diff = a - b
                    ## take the difference x1 - x2, y1 - y2
                
                    if diff > -2 and diff < 2:
                    ## check if difference is between -1 and 1
                        is_valid = True
                    else:
                    ## if any diff not valid, the whole path is not valid
                        is_valid = False
                        return is_valid

            else:
            ## two coordinates cannot be identical
                is_valid = False
                return is_valid

        return is_valid

    # check user word
    def check_word(self, word, board):
        ## TODO: BREAK THIS DOWN
        unpacked_board = []
        user_letters = []
        letter_map = defaultdict(list)
        
        ## first check to see if user's word is in the dictionary        
        if word in Boggle.dict_words:

            ## boggle land "Q" has a built-in "U" = "Qu"
            ## check for an QU combos in user's word, remove the subsequent U
            ## i'm doing this now since we've already checked to make sure
            ## the original word the user typed was in the dictionary

            word = word.replace('qu','q')
            
            unpacked_board, letter_map, user_letters = self.make_letter_maps(board, word)
            
            # then check to see if it is on the board
            
            a = Counter(user_letters)
            b = Counter(unpacked_board)

            minus_list = list(a - b)
            
            if len(minus_list) == 0:
                # then check to see if it follows board rules
                # x,y coordinates can be max +/- 1 away, used only once
                
                # first need to create all possible paths between letters
                find_coords = []
                find_paths = []
                is_valid = False
                for letter in word:
                    pos = letter_map[letter]
                    ## print "position of letter %s: %s" % (letter, pos)
                    find_coords.append(pos)
                
                for path in product(*find_coords):
                    find_paths.append(path)
                    ## print "possible path is:", path

                for path in find_paths:
                    # take difference between each coordinate
                    is_valid = self.validate_segment(path)
                    ## print list(path)
                    ## print "is segment valid?", is_valid
                    if is_valid == True:
                        print "good job! that's a valid word with possible path: ",path
                        break
                        
                if not is_valid:
                    print "no valid paths found!"

            else:
                print "hey! letter(s) %s not on the board!" % minus_list
        else:
        ## word isn't in dictionary
            print "try again"

    # show the board in a human-friendly way
    def show_board(self, board):
        print "-------------"
        print "play boggle!\n"
        for row in board:
            for letter in row:
                print " ",letter.upper(),
                if letter is "q":
                    print "u",
                else:
                    print " ",
            print "\n"

    # play a game of boggle
    def play(self):
        board = self.set_board()
        timer = True
        self.find_all_words(board)
        
        while timer is True:
            self.show_board(board)
            user_word = raw_input("> ")
            self.check_word(user_word.lower(), board)