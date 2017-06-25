"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
    #This method sets up two players and the initial game board
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

 #jm01 Created this function to be passed into get_move as a parameter
 #     It should calculate time left but I've fixed it to 5s for now
    def timeLimit(self): 
        return 5000

    def test_minimax(self):
        #Set up board
        print("Setting up inital board for simple minimax player test....")
        self.setUp()

        #Put some moves on board to create different start states
        
        # Player 1 move 1
        self.game.active_player==self.player1
        self.game.apply_move((0,0))
        # Player 2 move 1
        self.game.active_player==self.player2
        self.game.apply_move((0,2))
##        # Player 1 move 2
##        self.game.active_player==self.player1
##        self.game.apply_move((2,1))
##        # Player 2 move 2
##        self.game.active_player==self.player2
##        self.game.apply_move((2,0))

        #Print inital board
        print("\nInital state:\n{}".format(self.game.to_string()))

        #Calculate player 1 best next move using MiniMax
        best_move = (-1,-1)
        MinimaxPlayer= game_agent.MinimaxPlayer()
        best_move = MinimaxPlayer.get_move(self.game,self.timeLimit)
        print ('Best move for Player 1 is',best_move)

    def test_alfabeta(self):
        #Set up board
        print("Setting up inital board for alphabeta player test....")
        self.setUp()

        #Put some moves on board to create different start states
        
        # Player 1 move 1
        self.game.active_player==self.player1
        self.game.apply_move((0,0))
        # Player 2 move 1
        self.game.active_player==self.player2
        self.game.apply_move((0,2))
##        # Player 1 move 2
##        self.game.active_player==self.player1
##        self.game.apply_move((2,1))
##        # Player 2 move 2
##        self.game.active_player==self.player2
##        self.game.apply_move((2,0))

        #Print inital board
        print("\nInital state:\n{}".format(self.game.to_string()))

        #Calculate player 1 best next move using MiniMax with AlphaBeta pruning
        best_move = (-1,-1)
        AlphaBetaPlayer= game_agent.AlphaBetaPlayer()
        best_move = AlphaBetaPlayer.get_move(self.game,self.timeLimit)
        print ('Best move for Player 1 is',best_move)
    
            

if __name__ == '__main__':
    unittest.main()
