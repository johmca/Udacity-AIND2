"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    
    #return 0 #jm01a Just add this here to allow it to run

    raise NotImplementedError


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer): #IsolationPlayer is base class above
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def min_value (self, game, depth):
        
        debug = False
        if debug is True:
            print('Running min_value at depth', depth,'for',game.active_player)
        
        #Abandon search if timeout breached
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #If we reached our depth limit then return a score for this player
##        if depth <=0:
##            print('Depth limit reached')
##            return self.score(game, self)

        #Get list of legal moves
        legal_moves = game.get_legal_moves()
        
        #Check if we have reached a terminal state (no moves left). If so return
        #utility value of the board which will be
        #     +inf if the specified player has won the game
        #     -inf if the specified player has lost the game
        #     0 otherwise.
        #Pass the player object (instance of Minimax_player) into the utility method as self

        if not legal_moves:
            utility = game.utility(None)
            if debug is True:
                print('utlity value is',utility)
            return utility
        if debug is True:
            print('Legal moves...',legal_moves)
        
        
        #Generate a new game state for each move possible in legal_moves list and
        #Call the max_value method (alternate min and max) passing:
        #   i)    proposed new game state
        #   ii)   depth limit less 1 ( we are counting down to zero)    
        score = float("inf")
        for move in legal_moves:
            if debug is True:
                print('Next Action at level',depth,'=',move)
            next_state = game.forecast_move(move)
            if debug is True:
                print('Testing next game state using max_value for',game.active_player,'at level',depth)
                print(next_state.to_string_jm(['1','2'],depth))
            score = min(score, self.max_value(next_state, depth -1))
            if debug is True:
                print('running min at level',depth,'=',score)
        return score
                                            
                                         
                
    def max_value (self, game, depth):

        debug = False
        
        if debug is True:
            print('Running max_value at depth', depth,'for',game.active_player)
        #Abandon search if timeout breached
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #If we reached our depth limit then return a score for this player
        #if depth <=0:
        #    print('depth limit reached')
        #    return self.score(game, self)

        #Get list of legal moves
        legal_moves = game.get_legal_moves()
        
        
        #Check if we have reached a terminal state (no moves left). If so return
        #utility value of the board which will be
        #     +inf if the specified player has won the game
        #     -inf if the specified player has lost the game
        #     0 otherwise.
        #Pass the player object (instance of Minimax_player) into the utility method as self
        if not legal_moves:
            utility = game.utility(None)
            if debug is True:
                print('utlity value is',utility)
            return utility

        if debug is True:
            print('Legal moves...',legal_moves)
        
        #Generate a new game state for each move possible in legal_moves list and for each
        #   Call the min_value method to generate child nodes for each board abd return a score
        #   return the highest score from all child nodes abck to the caller (min_value)
        score = float("-inf")
        for move in legal_moves:
            if debug is True:
                print('Next Action at level',depth,'=',move)
            next_state = game.forecast_move(move)
            if debug is True:
                print('Testing next game state using min_value for',game.active_player,'at level',depth)
                print(next_state.to_string_jm(['1','2'],depth))
            score = max(score, self.min_value(next_state, depth -1))
            if debug is True:
                print('running max at level',depth,'=',score)
        return score
       

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures. This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        -------------------Pseudocode--------------------------------------------

        function MINIMAX(state) returns action                               
 
             return arg max a ∈ ACTIONS(s) MIN_VALUE(RESULT(state, a))

        function MIN-VALUE(state) returns a utility value
 
            if TERMINAL-TEST(state) then return UTILITY(state) v ← ∞
           for each a in ACTIONS(state) do
              v ← MIN(v, MAX-VALUE(RESULT(state, a)))
                return v

        function MAX-VALUE(state) returns a utility value
 
            if TERMINAL-TEST(state) then return UTILITY(state) v ← −∞
           for each a in ACTIONS(state) do
              v ← MAX(v, MIN-VALUE(RESULT(state, a)))
                return v

        -------------------Description--------------------------------------------

        Minimax receives a game state and obtains a set of valid moves.
        We then loop round each of these possible moves using it to 
        compute a new top level game state in which Player 1 (Max) has made the
        first move an dis waiting for Player 2 (Min).

        Each game state is then processed by the min_vlaue function and the max_value
        function in alternate turns. We start with the min_value function since the next
        move is Player 2 (seeks to minimise the score).

        min_value calls max_value and max_value calls min_value. Each of these functions
        gets the list of available moves for the current player and creates new game
        states for each move before calling min_value or max_value again. In this way the
        tree of all possible game states is processed until either
         i)  We run of time (if we have a time constraint)
         ii) We exceed our depth limit (if we have a depth constraint)
         iii)We reach an end gae state where no further moves are available to the current
             player

        When an end game state is reached we call the utility() function to calculate
        the value of the state. The utility() function calculates the value to be
        −∞ if Player2 wins or ∞ if Player 1 wins. At this point the instance of the
        recursive min_value/ max_value function that is running ends and returns the
        utility value to the previous instance of the min_value/ max_value function
        that is running. This instance either continues round the loop of possible
        game states or if no further moves can be mode ends and passes the lowest
        or highest score )depening on whether it is min or max) back up the stack.

        
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        #jm01 Set debug on/off
        debug = False
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        

        # TODO: finish this function!
        if debug is True:
            print('Starting MINIMAX:I need to work out the optimum move for this game state', game.active_player,'using the minimax algorithm')
            #depth =10
            print('Depth limit=',depth)
        
        #Get all legal moves for current player
        legal_moves=game.get_legal_moves()
        if legal_moves is None:
            if debug is True:
                print('There are no legal moves for player',game.active_player)
            return (-1,-1)
        
        if debug is True:
            print('MINIMX: Legal moves for',game.active_player,'=',legal_moves)
            print('MINIMAX: Test each move with minimax')

        best_score = float("-inf")
        best_move = None
        
        #Apply legal moves in turn to the current game state (empty board)
        #to create new possible game states
        #Apply the alternating minimax functions recursivley to each game state
        #to process the tree of all game states down to the end games,
        #obtain a utlity value for the end games and then percolate these
        #back up the tree using minimax
        for move in legal_moves:
            new_game=game.forecast_move(move)
            if debug is True:
                print('################################################################################')
                print('MINIMAX:TEST NEW TOP LEVEL GAMESTATE...')
                print('################################################################################')
                print(new_game.to_string_jm()) 
            score = self.min_value(new_game, depth -1)
            if debug is True:
                print('################################################################################')
                print(new_game.to_string_jm())
                print('Score calculated for top level game =',score)
                print('################################################################################')
            
           #If score of new game state is greater than previous best score use
           #this move as it produced a better game state
            if score >best_score:
                best_score =score
                best_move = move
         
        #Return the selected move
        if debug is True:
            print("Best move for",game.active_player,'=',best_move)
            print("Number of moves taken=",)
       
        return best_move

        raise NotImplementedError



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        raise NotImplementedError

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        raise NotImplementedError



    
