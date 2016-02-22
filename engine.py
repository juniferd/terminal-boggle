import threading

import mechanics

## engine for game play

GAME_TIME=15
class Engine(object):
    def __init__(self):
        self.__timer_on = True
        self.__remaining_time = GAME_TIME
        self.__round_score = 0

    """
    menu_map = {
        'h': full_menu,
        'e': exit_round,
        's': start_round,
        'n': new_board,
        'r': rotate_board,
    }
    """
    # present a menu
    def menu(self):
        print "\ntype S to start playing"
        player_input = raw_input("> ").lower()
        
        ## FIX THIS LATER
        if player_input == 's':
            self.start_round()
        elif player_input == 'e':
            self.stop_round()

    # start a round
    def start_round(self):
        ##FIX THIS LATER
        game_words = self.play_game()
        
        print "Here are your valid words from the game: "
        for word in game_words:
            print word
        
        # show total words
        all_words = self.game.find_all_words()
        print "You found %s out of %s words" % (len(game_words), all_words)

        game_score = self.score_game(game_words)
        # score a game
        print "Your game score: ", game_score


        # add score to round_score
        self.__round_score += game_score
        print "Your round score: ", self.__round_score
        self.game_reset()
        print "-------------"

        # present the menu
        self.menu()
    
    # manually stop a round
    def stop_round(self):
        self.__round_score = 0
        self.menu()
    # change board to size nxn

    # score
    def score_game(self, words):
        scoring = {
            3 : 1,
            4 : 1,
            5 : 2,
            6 : 3,
            7 : 5,
            8 : 11
        }
        score = 0
        for word in words:
            length = int(words[word])
            if length >= 8:
                score = score + 11
            else:
                score = score + scoring[length]

        return score

    def game_reset(self):
        
        self.__timer_on = True
        self.__remaining_time = GAME_TIME

    def tick_timer(self):
        self.__remaining_time -= 1
        if self.__remaining_time <= 0:
            self.__timer_on = False
            print "%s seconds are up! press enter" % GAME_TIME

        if self.__timer_on:
            t = threading.Timer(1.0, self.tick_timer)
            t.start()

    # play a game of boggle
    def play_game(self):
        checked_words = {}
        boggle_game = mechanics.Boggle()
        self.game = boggle_game

        self.tick_timer()
        # play a timed game

        while self.__timer_on is True:
            boggle_game.show_board()
            user_word = raw_input("> ")
            if not self.__timer_on: 
                break

            this_word = boggle_game.check_word(user_word.lower(),True)
            if this_word is not None:
                checked_words[this_word] = len(this_word)

        return checked_words
