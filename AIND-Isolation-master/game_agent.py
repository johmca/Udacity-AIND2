"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    This heuristic sets out to maintain a healthy distance from the opponent
    in the belief that this will lead to having more squares avalable.

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

    #If game state is a loser for the player then return -inf
    if game.is_loser(player):
        return float("-inf")
    
     #If game state is a winner for the player then return +inf
    if game.is_winner(player):
        return float("inf")

    #Get the opponent
    opponent = game.get_opponent(player)

##    #Get location of player
##    y1,x1 = game.get_player_location(player)
##
##    #Get location of opponent
##    y2,x2 = game.get_player_location(opponent)    
##
##    #Return the distance between the player and opponent so that distance is
##    #maximised
##    return float (10**math.sqrt((y1 - y2)**2 + (x1 - x2)**2))

    #return the negative of the number of moves available to the opponent
    return float (-10**len(game.get_legal_moves(opponent)))



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    This heuristic values game states where the opponent's available moves are
    judged to be more peripheral than the player's own moves most highly (I am assuming a peripheral position will tend
    to have fewer moves available)
    
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
    #If game state is a loser for the player then return -inf
    if game.is_loser(player):
        return float("-inf")
    
     #If game state is a winner for the player then return +inf
    if game.is_winner(player):
        return float("inf")

    #Get the opponent
    opponent = game.get_opponent(player)

##    #Get location of player
##    y1,x1 = game.get_player_location(player)
##
##    #Get location of opponent
##    y2,x2 = game.get_player_location(opponent)

    w, h = game.width / 2., game.height / 2. #Centre of board (h,w)

    #For each of the players's available moves calculate the distance from
    #the centre of the board and find the average distance across all
    #available moves
    player_moves=game.get_legal_moves(player)
    move_count = 0
    player_average_distance = 0
    player_total_distance = 0

##    for move in player_moves:
##        y, x = move
##        distance = math.sqrt((h - y)**2 + (w - x)**2)
##        player_total_distance = player_total_distance + distance
##        move_count += 1
##
##    if move_count != 0:
##        player_average_distance = player_total_distance / move_count

    #For each of the opponent's available moves calculate the distance from
    #the centre of the board and find the average distance
    opponent_moves=game.get_legal_moves(opponent)
    move_count = 0
    opponent_average_distance = 0
    opponent_total_distance = 0
    for move in opponent_moves:
        y, x = move
        #distance = math.sqrt((h - y)**2 + (w - x)**2)
        distance = ((h - y)**2 + (w - x)**2)
        opponent_total_distance = opponent_total_distance + distance
        move_count += 1

    if move_count != 0:
        opponent_average_distance = opponent_total_distance / move_count

    #normalise the output so all scores in range 0 to 1
##    max_distance = math.sqrt((3.5)**2 + (3.5)**2) #max distance possible on board is diag
##    min_distance = 0
##    norm_distance = (average_distance - min_distance)/(max_distance-min_distance)
    
    
##    print('Average distance of all available opponent moves',average_distance)
##    print('Max distance form centre',max_distance)
##    print('Normalised Average distance',norm_distance)

    #return the log of the average distance fo the opponent's available moves
    return float(10**opponent_average_distance)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    This heuristic scores game states where the Player has the most blocking moves
    on his opponent as having the highest value.

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
    #If game state is a loser for the player then return -inf
    if game.is_loser(player):
        return float("-inf")
    
     #If game state is a winner for the player then return +inf
    if game.is_winner(player):
        return float("inf")

    #Get the opponent
    opponent = game.get_opponent(player)

    #Get list of legal moves for player
    player_moves=game.get_legal_moves(player)

    #Get list of legal moves for opponent
    opponent_moves=game.get_legal_moves(opponent)

    #Count the number of blocking moves available to player (the more the better)
    blocking_moves = 0
    for move in player_moves:
        if move in opponent_moves:
            blocking_moves += 1
            
    #normalise the output so all scores in range 0 to 1
##    max_blocks = 8
##    min_blocks = 0
##    norm_blocks = (blocking_moves - min_blocks)/(max_blocks-min_blocks)

    w, h = game.width / 2., game.height / 2. #Centre of board (h,w)

    player_moves=game.get_legal_moves(player)
    move_count = 0
    player_average_distance = 0
    player_total_distance = 0

    for move in player_moves:
        y, x = move
        distance = math.sqrt((h - y)**2 + (w - x)**2)
        player_total_distance = player_total_distance + distance
        move_count += 1

    if move_count != 0:
        player_average_distance = player_total_distance / move_count


    
    opponent_moves=game.get_legal_moves(opponent)
    move_count = 0
    opponent_average_distance = 0
    opponent_total_distance = 0
    for move in opponent_moves:
        y, x = move
        #distance = math.sqrt((h - y)**2 + (w - x)**2)
        distance = ((h - y)**2 + (w - x)**2)
        opponent_total_distance = opponent_total_distance + distance
        move_count += 1

    if move_count != 0:
        opponent_average_distance = opponent_total_distance / move_count
            

    return float(10*(len(player_moves))-(6*len(opponent_moves))-(8*player_average_distance)+(2*opponent_average_distance)+blocking_moves)


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
        #jm01 Store the number of nodes visited in our minimax tree search
        self.numberofnodesvisited=0 

class MinimaxPlayer(IsolationPlayer):
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
        """
        This function is called alternately with the max_value function. It is called
        for a miniimising level in the game tree i.e. Player 2.
        It generates each possible move for the  player and creates a game board
        for each of these before calling the max_value function for each game board.
        It finds the maximum score returned by the calls to max_value i.e. the max score across
        all the nodes at this level and passes back to the calling max_value function


        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            The depth of the current board in the tree

        Returns : int
        -------
        The maximum score of all the nodes at the current depth in the tree
            
        """
        debug = False
        if debug is True:
            print('Running min_value at depth', depth,'for',game.active_player)
        
        #Abandon search if timeout breached
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #If we reached our depth limit then return a score for this player
        if depth <=0:
            if debug is True:print('Depth limit reached')
            return self.score(game, self)

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
        min_score = float("inf")
        for move in legal_moves:
            if debug is True:
                print('Next Action at level',depth,'=',move)
            next_state = game.forecast_move(move)
            self.numberofnodesvisited +=1
            if debug is True:
                print('Testing next game state using max_value for',game.active_player,'at level',depth)
                print(next_state.to_string(['1','2'],depth))
##            score = min(score, self.max_value(next_state, depth -1))
            score = self.max_value(next_state, depth -1)
            if score < min_score:
                min_score = score
            if debug is True: print('running min at level',depth,'=',score)

        return min_score
                                            
                                         
                
    def max_value (self, game, depth):
        """
        This function is called alternately with the min_value function. It is called
        for a maximising level in the game tree i.e. Player 1.
        It generates each possible move for the current player and creates a game board
        for eahc of these before calling the min_value function for each game board.
        It finds the maximum score returned by the calls to min_value i.e. the max score across
        all the nodes at this level and passes back to the calling min_value function


        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            The depth of the current board in the tree

        Returns : int
        -------
        The maximum score of all the nodes at the current depth in the tree
            
        """
        debug = False
        
        if debug is True: print('Running max_value at depth', depth,'for',game.active_player)

        #Abandon search if timeout breached
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #If we reached our depth limit then return a score for this player
        if depth <=0:
            print('depth limit reached')
            return self.score(game, self)

        #Get list of legal moves
        legal_moves = game.get_legal_moves()
                
        #Check if we have reached a terminal state (no moves left). If so return
        #utility value of the board which will be
        #     +inf if the specified player has won the game
        #     -inf if the specified player has lost the game
        #     0 otherwise.
        if not legal_moves:
            utility = game.utility(None)
            if debug is True:print('utlity value is',utility)
            return utility

        if debug is True:print('Legal moves...',legal_moves)
        
        #Generate a new game state for each move possible in legal_moves list and for each
        #   Call the min_value method to generate child nodes for each board abd return a score
        #   return the highest score from all child nodes abck to the caller (min_value)
        max_score = float("-inf")
        for move in legal_moves:
            if debug is True:print('Next Action at level',depth,'=',move)
            next_state = game.forecast_move(move)
            self.numberofnodesvisited +=1
            if debug is True:
                print('Testing next game state using min_value for',game.active_player,'at level',depth)
                print(next_state.to_string())

            score = self.min_value(next_state, depth -1)
            if score > max_score:
                max_score = score
                
            if debug is True: print('running max at level',depth,'=',score)

        return max_score

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

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
         if Player2 wins or if Player 1 wins. At this point the instance of the
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
            self.numberofnodesvisited +=1
            if debug is True:
                print('################################################################################')
                print('MINIMAX:TEST NEW TOP LEVEL GAMESTATE...')
                print('################################################################################')
                print(new_game.to_string()) 
            score = self.min_value(new_game, depth -1)
            if debug is True:
                print('################################################################################')
                print(new_game.to_string())
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
            print('Number of ndoes visited=',self.numberofnodesvisited)
       
        return best_move


        #raise NotImplementedError


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.

    Iterative Deepening is a strategy which test the game tree iteratively, each time
    deepening the search depth until a time limit is encountered and at that point
    the best known move is used. While this may appear to be inneficient this is not the
    case due to the exponential growth in nodes as we get deeper in the tree.

    AlphaBeta pruning is a search strategy designed to reduce the branches and nodes
    of the game tree that are searched. Branches that do not contribute to the result are
    ignored or "pruned".

    
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
        debug = False

        #Set time left to number of ms left in current turn
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            #Implement Iterative Deepening strategy. This means that we generate our
            #game tree to a specified depth and if we still have time we generate another
            #tree extending the depth of the seach by 1. We continue doing this until we timeout
            #and at that point we return what we think is our best move.            
            if debug is True:print('Get best move using iterative deepening')
            to_depth=1
            while True:              
                best_move = self.alphabeta(game, to_depth)
                to_depth+=1
                
                
        except SearchTimeout:
            #When timeout encountered we break here 
            pass


        # Return the best move from the last completed search iteration. If no best move
        #then use first legal move.
##        if best_move==(-1,-1):
##            legal_moves = game.get_legal_moves()
##            if len(legal_moves)!=0:
##                best_move=legal_moves[0]
##        if debug is True:print('Returning best move =',best_move)
        
        return best_move

    def min_value (self, game, depth, alpha, beta):
        """
        This function is called alternately with the max_value function. It is called
        for minimising levels in the game tree.
        
        It generates each possible move for the  player and creates a game board
        for each of these before calling the max_value function for each game board.
        It finds the maximum score returned by the calls to max_value i.e. the max score across
        all the nodes at this level and passes back to the calling max_value function


        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            The depth of the current board in the tree

        alpha: float
            The value of the best choice we have found so far for MAX (highest value)

        beta : float
          The value of the best choice we have found so far for MIN (lowest value) 

        Returns : int
        -------
        The minimum score accross all the nodes processed so far at the current depth in the tree
            
        """
        debug = False

        if debug is True: print('Running alfabeta min_value at depth', depth,'for',game.active_player)
        
        #Abandon search if timeout breached
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Get list of legal moves
        legal_moves = game.get_legal_moves()
        
        #Check if we have reached a terminal state (no moves left).
        #If so caluclate and return the utility value of the board to the level above
        if len(legal_moves)==0:
            return self.score(game, self)

        #If we reached our depth limit then caluclate and return the utility value
        #of the board to the level above 
        if depth ==0:
            return self.score(game, self)
               
        #Generate a new game state for each move possible in legal_moves list. For each
        #legal move apply the move to the current game to create a possible game state and
        #call the scoring functions for each possible state returning a score
        value=float('+inf')
        for move in legal_moves:
            if debug is True: print('Next Action at level',depth,'=',move)
            next_state = game.forecast_move(move)
            self.numberofnodesvisited +=1
            if debug is True:
                print('Testing next game state using max_value for',game.active_player,'at level',depth)
                print(next_state.to_string())
           
            #calculate the score for the children of this node (next level is down is a max level) passing the game board (proposed),
            #the depth and the values of alpha and beta from this level
            value =  min(value, self.max_value(next_state, depth -1,alpha,beta))


            #If score returned from next level down (max level) is less than the current lower bound (alpha)
            #then stop processing nodes at this level as they will never be used. Return the current min score
            #from this level to the calling level.
            if   value <= alpha:
                return value
                
            #If score is < Beta (upper bound) then set Beta to equal the score. New Beta will be used on subsequent scoring of game states
            #at this level.
            beta = min(beta, value)
            
         #If we do get through processing all nodes at this level then return the minimum score accrued at this level 
        return value
                                            
                                         
                
    def max_value (self, game, depth, alpha, beta):
        """
        This function is called alternately with the min_value function. It is called
        for a maximising level in the game tree i.e. Player 1.
        
        It generates each possible move for the current player. It creates a game board
        for each of these before calling the min_value function for each game board passing
        the current values of Alpha and Beta.

        Min_value and Max_Value are then called alternately and recursively until the full
        game tree has been revealed.

        The recursion rolls back with the Min_Value and Max_Value functions returning their
        score back up the tree.

        The intsances of the min_value function called from here return a value and we
        take the maximum of these and pass this back to the calling funciton.
        
        This version of the min_value and max_value functions utlise Alpha Beta pruning to
        reduce the search space by ensuring we don't visit branches of the game tree that will
        never be used.


        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            The depth of the current board in the tree

        alpha : float
            The current value of Alfa (the maximum lower bound)

        beta : float
            The current value of Beta (the mimimum upper bound)           

        Returns : int
        -------
        The maximum score of all the nodes processed at the current depth in the tree
            
        """
        debug = False
        
        if debug is True: print('Running alfabeta max_value at depth', depth,'for',game.active_player)

        #Abandon search if timeout breached
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Get list of legal moves
        legal_moves = game.get_legal_moves()
                
        #Check if we have reached a terminal state (no moves left) and return score of game if we have
        if len(legal_moves)==0:
            return self.score(game, self)

        #If we reached our depth limit then return a score for this game
        if depth ==0:
            return self.score(game, self)

        
        #Generate a new game state for each move possible in legal_moves list. For each
        #legal move apply the move to the current game to create a possible game state and
        #call the max_value/ min_value methods for each possible state returning a score
        value = float('-inf')
        for move in legal_moves:
            next_state = game.forecast_move(move)
            self.numberofnodesvisited +=1


            #calculate the score for the children of this node (next level is down is a min) passing the game board (proposed),
            #the depth and the values of alpha and beta 
            value = max(value, self.min_value(next_state, depth -1,alpha,beta))

            #If score returned from next level down (min level) is >= the current upper bound (beta)
            #then stop processing nodes at this level as they will never be used. Return the max score
            #at this level to the calling level.
            if   value >= beta:
                return value
                
            #If score is > Alpha then set Alpha to equal score (new Alpha will be used on subsequent iterations of game states)
            alpha = max(alpha, value)

        #If we do get through processing all nodes at this level then return the maximum score at this level 
        return value

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        This is an elaboration on the simple MiniMax above. It adds

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

        # TODO: finish this function!
        debug = False
        
        #Abandon search if timeout breached
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Get list of legal moves
        legal_moves = game.get_legal_moves()
                
        #Check if we have reached a terminal state (no moves left). If so return 
        #move (-1,-1) indicating there are no possible moves
        if len(legal_moves)==0:
            if debug is True: print('No legal moves')
            return (-1,-1)

        if debug is True:
            print(game.to_string())
            print('Legal moves...',legal_moves)
               
       
        best_move=legal_moves[random.randint(0,len(legal_moves))-1] #assign random move as default best move

        #Generate a new game state for each move possible move in legal_moves list and for each game state
        #call the scoring functions iteratively to generate the game tree and return scores
        #back up the tree.  
        for move in legal_moves:
            if debug is True: print('Next Action at level',depth,'=',move)
            next_state = game.forecast_move(move)
            self.numberofnodesvisited +=1

        #Calculate score for this node by calling alphabeta min function (next level down is min)
            score = self.min_value(next_state, depth -1, alpha, beta)

            #If score is >= Alpha (lower bound) then set Alpha to equal score and store this as best move
            #New Alpha will be used on subsequent calls to the scoring functions at this level
            if   score >= alpha:
                alpha = score
                best_move = move
                
            #If score is >=beta (upper bound) then return stored best move as the best move and stop searching
            if score >=beta:
                return best_move

            #alpha = max(alpha, score)
            
        #return the stored best move
        return best_move

       
