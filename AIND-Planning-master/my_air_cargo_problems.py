from aimacode.logic import PropKB
from aimacode.planning import Action
from aimacode.search import (
    Node, Problem,
)
from aimacode.utils import expr
from lp_utils import (
    FluentState, encode_state, decode_state,
)
from my_planning_graph import PlanningGraph

from functools import lru_cache


class AirCargoProblem(Problem):
    def __init__(self, cargos, planes, airports, initial: FluentState, goal: list):
        """

        :param cargos: list of str
            cargos in the problem
        :param planes: list of str
            planes in the problem
        :param airports: list of str
            airports in the problem
        :param initial: FluentState object
            positive and negative literal fluents (as expr) describing initial state
        :param goal: list of expr
            literal fluents required for goal test
        """

        self.state_map = initial.pos + initial.neg
        self.initial_state_TF = encode_state(initial, self.state_map)
        print('Now in AirCargoProblem initiation...',self.state_map, self.initial_state_TF,goal,'preparing to call problem.__init__')
        Problem.__init__(self, self.initial_state_TF, goal=goal)
        self.cargos = cargos
        print('Back in AirCargoProblem()........cargos,planes and airports..',cargos,planes,airports)
        self.planes = planes
        self.airports = airports
        self.actions_list = self.get_actions() #CALL MY ROUTINES TO BUILD LIST OF ACTIONS

    def get_actions(self):
        """
        This method creates concrete actions (no variables) for all actions in the problem
        domain action schema and turns them into complete Action objects as defined in the
        aimacode.planning module. It is computationally expensive to call this method directly;
        however, it is called in the constructor and the results cached in the `actions_list` property.

        Returns:
        ----------
        list<Action>
            list of Action objects


        Action scheemas for the air cargo problem as defined in the book at p367 as follows..

        Action(Fly(p,from,to),
            PRECOND:At(p,from)^Plane(p)^Airport(from)^Airport(to)
            EFFECT:¬At(p,from)^At(p,to)
        )

        Action(Load(c,p,a),
            PRECOND: At(c,a)^At(p,a)^Cargo(c)^Plane(p)^Airport(a)
            EFFECT:At(c,a)^In(c,p)
        )

        Action(Unload(c,p,a),
            PRECOND: In(c,p)^At(p,a)^Cargo(c)^Plane(p)^Airport(a)
            EFFECT:At(c,a)^¬In(c,p)
        )

        We create an instance of the Action (an action object) by passing the formatted strings to Actions() function

        For example to create a fly action from JFK to SFO construct the following string

        {-----Action-----} {--PRECOND------}               -------EFFECT -------------]
                            --Pos------ --Neg--             ---Add----               ---Rem-----
        Fly(P1, JFK, SFO) [[At(P1, JFK)], []]                [[At(P1, SFO)],        [At(P1, JFK)]]

        This would make the string to create a load action loading cargo C1 onto Plane P1 at JFK something like...

        Load(C1, P1, JFK) [[At(C1,JFK)^At(P1,JFK)],[]]    [[At(C1,JFK^In(C1,P1))],  []]

        And this would make the string to create a unload action unloading cargo C1 from Plane P1 at SFO something like...

        Unload(C1, P1, SFO) [[In(C1,P1)^At(P1,SFO)],[]]    [[At(C1,SFO))],          [¬In(C1,P1)]]

        """




        # TODO create concrete Action objects based on the domain action schema for: Load, Unload, and Fly
        # concrete actions definition: specific literal action that does not include variables as with the schema
        # for example, the action schema 'Load(c, p, a)' can represent the concrete actions 'Load(C1, P1, SFO)'
        # or 'Load(C2, P2, JFK)'.  The actions for the planning problem must be concrete because the problems in
        # forward search and Planning Graphs must use Propositional Logic

        def load_actions():
            """Create all concrete Load actions and return a list of action objects

            :return: list of Action objects
            """
            # print('Now creating load actions....')
            loads = []

            # # TODO create all load ground actions from the domain Load action

            for c in self.cargos:
                for p in self.planes:
                    for a in self.airports:
                       #precond_pos = [expr("In({}, {})^At({},{})^Cargo({})^Plane({})^Airport({})".format(c, p, p, a,c,p,a))]
                        precond_pos = [expr("At({}, {})".format(c, a)),
                                       expr("At({}, {})".format(p, a))
                                       ]
                        precond_neg = []
                        effect_add = [expr("In({},{})".format(c, p))]
                        effect_rem = [expr("At({},{})".format(c, a))]
                        #Use Action() function defined in aimacode.planning.py to create action object from the action expression
                        # print(expr("Load({}, {}, {})".format(c, p, a)),
                        #       [precond_pos, precond_neg],
                        #       [effect_add, effect_rem])
                        loadAction = Action(expr("Load({}, {}, {})".format(c, p, a)),
                                              [precond_pos, precond_neg],
                                              [effect_add, effect_rem])


                        # Add new action object to list of action objects
                        loads.append(loadAction)
            return loads

        def unload_actions():
            """Create all concrete Unload actions and return a list of action objects

            :return: list of Action objects
            """
            # print('Now creating unload actions....')
            unloads = []
            # TODO create all Unload ground actions from the domain Unload action

            for c in self.cargos:
                for p in self.planes:
                    for a in self.airports:
                        # print('cargo',c,'plane',p,'airport',a)
                        #Construct strings to make into Action objects in the following format
                        # String = Unload(C1, P1, SFO) [[In(C1,P1)^At(P1,SFO)],[]]    [[At(C1,SFO)^¬In(C1,P1))],[]]
                        # TODO create all load ground actions from the domain Load action
                        #precond_pos = [expr("In({}, {})^At({},{})^Cargo({})^Plane({})^Airport({})".format(c, p, p, a,c,p,a))]
                        precond_pos = [expr("In({}, {})".format(c, p)),
                                       expr("At({},{})".format(p, a))
                                       ]
                        precond_neg = []
                        effect_add = [expr("At({}, {})".format(c, a))]
                        effect_rem = [expr("In({},{})".format(c,p))]
                        #Use Action() function defined in aimacode.planning.py to create action object from the action expression
                        # print(expr("Unload({}, {}, {})".format(c, p, a)),
                        #       [precond_pos, precond_neg],
                        #       [effect_add, effect_rem])
                        unloadAction = Action(expr("Unload({}, {}, {})".format(c, p, a)),
                                              [precond_pos, precond_neg],
                                              [effect_add, effect_rem])


                        # Add new action object to list of action objects
                        unloads.append(unloadAction)
            return unloads

        def fly_actions():
            """Create all concrete Fly actions and return a list of action objects

            :return: list of Action objects
            """
            # print('Now creating all possible fly actions....')
            flys = []
            for fr in self.airports:
                for to in self.airports:
                    if fr != to:
            # Construct fly actions for each possible plane and airport using the fly action schema for formatting
            # e.g. Fly(P1, JFK, SFO) [[At(P1, JFK)], []] [[At(P1, SFO)], [At(P1, JFK)]]
                        for p in self.planes:
                            precond_pos = [expr("At({}, {})".format(p, fr)),
                                           ]
                            precond_neg = []
                            effect_add = [expr("At({}, {})".format(p, to))]
                            effect_rem = [expr("At({}, {})".format(p, fr))]
            #Use Action() function defined in aimacode.planning.py to create action object from the action expression
                            # print (expr("Fly({}, {}, {})".format(p, fr, to)),
                            #              [precond_pos, precond_neg],
                            #              [effect_add, effect_rem])
                            fly = Action(expr("Fly({}, {}, {})".format(p, fr, to)),
                                         [precond_pos, precond_neg],
                                         [effect_add, effect_rem])
            #Add new action object to list of action objects
                            flys.append(fly)

            #return list of action objects.
            return flys

        #Return the concatenated list of load, unoad and fly actions

        return load_actions() + unload_actions() + fly_actions()


    def actions(self, state: str) -> list:
        """ Return the actions that can be executed in the given state.

        Any action which as a precondition that is present in the state may be legally executed

        More formally put (p368) - An action a can be executed in state s if s entails the precondition of a.

        :param state: str
            state represented as T/F string of mapped fluents (state variables)
            e.g. 'FTTTFF'
        :return: list of Action objects
        """
        # TODO implement

        # print('Now running actions() function to get all actions that may be executed in state',state)
        possible_actions = []
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        # print('Current state', state, kb.clauses)
        # print('Number of actions in actions_list=',len(self.actions_list))
        for action in self.actions_list:
            # print('Now checking action',action.name,action.args)
            is_possible = True
            # Loop round +ve preconds for the action and check if exist in state clauses. If not found
            #action is not possible
            # print('+ve preconds for action=',action.precond_pos)
            for clause in action.precond_pos:
                if clause not in kb.clauses:
                    is_possible = False
            # Loop round -ve preconds for the action and check if exist in state clauses. If found
            #action is not possible
            # print('-ve preconds for action=', action.precond_neg)
            for clause in action.precond_neg:
                if clause in kb.clauses:
                    is_possible = False
            #If aciton not ruled as impossible then add to list of possible actions for return to caller
            if is_possible:
                possible_actions.append(action)
        # print('List of possible actions',possible_actions)
        return possible_actions

    def result(self, state: str, action: Action):
        """ Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        This routine simply takes the current state, pos and neg, and copies to a new version depending
        on the action's effects which can be add or rem.

        So if the action has a add effect the new state will contain that effect in its pos section
        If the action has a rem effect then the new state will contain that effect in its neg section

        More formally put (p368) - The result of executing action a in state s is defined as a state s' which is represented
        by the set of fluents formed by starting with s, removing the fluents that appear as negative literals in the
        action's effects (what we wil call the delete list or DEL(a), and addign the fluents that are positie literals
        in the action's effects (what we will call the add list or ADD(a).

        :param state: state entering node
        :param action: Action applied
        :return: resulting state after action
        """
        # TODO implement
        #print('Running result() function...')
        new_state = FluentState([], [])
        old_state = decode_state(state, self.state_map)
        for fluent in old_state.pos:
            if fluent not in action.effect_rem:
                new_state.pos.append(fluent)
        for fluent in action.effect_add:
            if fluent not in new_state.pos:
                new_state.pos.append(fluent)
        for fluent in old_state.neg:
            if fluent not in action.effect_add:
                new_state.neg.append(fluent)
        for fluent in action.effect_rem:
            if fluent not in new_state.neg:
                new_state.neg.append(fluent)

        return encode_state(new_state, self.state_map)

    def goal_test(self, state: str) -> bool:
        """ Test the state to see if goal is reached

        :param state: str representing state
        :return: bool
        """
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for clause in self.goal:
            if clause not in kb.clauses:
                return False
        return True

    def h_1(self, node: Node):
        # note that this is not a true heuristic
        h_const = 1
        return h_const

    @lru_cache(maxsize=8192)
    def h_pg_levelsum(self, node: Node):
        """This heuristic uses a planning graph representation of the problem
        state space to estimate the sum of all actions that must be carried
        out from the current state in order to satisfy each individual goal
        condition.
        """
        # requires implemented PlanningGraph class
        pg = PlanningGraph(self, node.state)
        pg_levelsum = pg.h_levelsum()
        return pg_levelsum

    @lru_cache(maxsize=8192)

    def h_ignore_preconditions(self, node: Node):
        """This heuristic estimates the minimum number of actions that must be
        carried out from the current state in order to satisfy all of the goal
        conditions by ignoring the preconditions required for an action to be
        executed.

        From book p376...
        Search is not efficient without a good heuristic function. Recall from Chapter 3 that a heuristic funciton h(s)
        estimates the distance from state s to the goal and from that we can derive an ADMISSIBLE heuristic for this distance
        - one that does NOT overestomate - then we can use A* search to find optimal solutions. An admissible heuristic can
        be derived by defining a RELAXED PROBLEM that is easier to solve. The exact cost of a solution to this easier problem becomes
        the heuristic value of the original problem.

        There are 2 ways to relax a problem
        i) Creating more lines between nodes (edges)
        ii) Grouping nodes together resulting in a smaller state space

        The technique used here is the former. We relax the problem by removing preconditions from our actions generating
        more lines. Every on eof our actions is then applicable for every state. Any of our goal fluents (variables)
        can be achieved in a single action. Of course our goal state will have multiple fluents describing it in which case
         our heuristic simply counds how many actions are required to achieve these.

        So if the node state is TTTTFFFFF we need and the goal state is At(C1,JFK)^At(C2,SFO) then we need to
        check if the T/F flag corresponding to the goal state conditions are T or F. If they are F then we can set
         them to T by applying one of our actions so count this in our count.The total number of actions counted is the
         value of our heuristic.

        Logic is...

           - set action count to 0
           - Loop through the goal state conditions and for each goal condition
               look up the state map using the goal condition and get its position in the list
               look up the node state using this posiiton
               if node state at this position is FALSE then add 1 to action count

        And thats all there is to it

        """
        # TODO implement (see Russell-Norvig Ed-3 10.2.3  or Russell-Norvig Ed-2 11.2)
        # print('NOW RUNNING h_ignore_preconditions heuristic............',node)

        count = 0
        for goal_condition in self.goal:
            # print('goal condition is',goal_condition)
            # print('state map is',self.state_map)
            found = self.state_map.index(goal_condition)
            # print('found goal condition at',found)
            value=node.state[found]
            # print('Node state',node.state,'has value',value,'at position',found)
            if value == 'F': count +=1

        # print('Number of actions =',count)
        return count


def air_cargo_p1() -> AirCargoProblem:
    # Problem definition in PDDL............
    # Init(At(C1, SFO) ∧ At(C2, JFK)
    # ∧ At(P1, SFO) ∧ At(P2, JFK)
    # ∧ Cargo(C1) ∧ Cargo(C2)
    # ∧ Plane(P1) ∧ Plane(P2)
    # ∧ Airport(JFK) ∧ Airport(SFO))
    # Goal(At(C1, JFK) ∧ At(C2, SFO))

    cargos = ['C1', 'C2']
    planes = ['P1', 'P2']
    airports = ['JFK', 'SFO']
    pos = [expr('At(C1, SFO)'),   #Cargo1 at SFO
           expr('At(C2, JFK)'),   #Cargo2 at JFK
           expr('At(P1, SFO)'),   #Plane1 at SFO
           expr('At(P2, JFK)'),   #Plane2 at JFK
           ]
    neg = [expr('At(C2, SFO)'),   #Cargo2 not at SFO
           expr('In(C2, P1)'),    #Cargo2 not in P1
           expr('In(C2, P2)'),    #Cargo2 not in P2
           expr('At(C1, JFK)'),   #Cargo1 not at JFK
           expr('In(C1, P1)'),    #Cargo1 not in P1
           expr('In(C1, P2)'),    #Cargo1 not in P2
           expr('At(P1, JFK)'),   #Plane1 not at JFK
           expr('At(P2, SFO)'),   #Plane2 not at SFO
           ]
    init = FluentState(pos, neg)
    goal = [expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p2() -> AirCargoProblem:

    # Problem definition in PDDL............
    # Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL)
    # ∧ At(P1, SFO) ∧ At(P2, JFK) ∧ At(P3, ATL)
    # ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3)
    # ∧ Plane(P1) ∧ Plane(P2) ∧ Plane(P3)
    # ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL))
    # Goal(At(C1, JFK) ∧ At(C2, SFO) ∧ At(C3, SFO))
    # TODO implement Problem 2 definition

    cargos = ['C1', 'C2','C3']
    planes = ['P1', 'P2','P3']
    airports = ['JFK', 'SFO','ATL']
    pos = [expr('At(C1, SFO)'),  # Cargo1 at SFO
           expr('At(C2, JFK)'),  # Cargo2 at JFK
           expr('At(C3, ATL)'),  # Cargo3 at ATL
           expr('At(P1, SFO)'),  # Plane1 at SFO
           expr('At(P2, JFK)'),  # Plane2 at JFK
           expr('At(P3, ATL)'),  # Plane3 at ATL
           ]
    neg = [
           expr('At(C3, SFO)'),  # Cargo3 not at SFO
           expr('At(C3, JFK)'),  # Cargo3 not at JFK
           expr('In(C3, P1)'),  # Cargo3 not in P1
           expr('In(C3, P2)'),  # Cargo3 not in P2
           expr('In(C3, P3)'),  # Cargo3 not in P3
           expr('At(C2, SFO)'),  #Cargo2 not at SFO
           expr('At(C2, ATL)'),  #Cargo2 not at ATL
           expr('In(C2, P1)'),  #Cargo2 not in P1
           expr('In(C2, P2)'),  #Cargo2 not in P2
           expr('In(C2, P3)'),  #Cargo2 not in P3
           expr('At(C1, JFK)'),  #Cargo1 not at JFK
           expr('At(C1, ATL)'),  # Cargo1 not at ATL
           expr('In(C1, P1)'),  #Cargo1 not in P1
           expr('In(C1, P2)'),  #Cargo1 not in P2
           expr('In(C1, P3)'),  # Cargo1 not in P3
           expr('At(P1, JFK)'),  #Plane1 not at JFK
           expr('At(P1, ATL)'),  # Plane1 not at ATL
           expr('At(P2, SFO)'),  #Plane2 not at SFO
           expr('At(P2, ATL)'),  # Plane2 not at ATL
           expr('At(P3, SFO)'),  # Plane2 not at SFO
           expr('At(P3, JFK)'),  # Plane2 not at ATL
           ]
    init = FluentState(pos, neg)
    goal = [expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            expr('At(C3, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)

def air_cargo_p3() -> AirCargoProblem:
    # Problem definition in PDDL............
    # Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) ∧ At(C4, ORD)
    # ∧ At(P1, SFO) ∧ At(P2, JFK)
    # ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3) ∧ Cargo(C4)
    # ∧ Plane(P1) ∧ Plane(P2)
    # ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL) ∧ Airport(ORD))
    # Goal(At(C1, JFK) ∧ At(C3, JFK) ∧ At(C2, SFO) ∧ At(C4, SFO))
    # TODO implement Problem 3 definition
    cargos = ['C1', 'C2','C3','C4']
    planes = ['P1', 'P2']
    airports = ['JFK', 'SFO','ATL','ORD']
    pos = [expr('At(C1, SFO)'),  # Cargo1 at SFO
           expr('At(C2, JFK)'),  # Cargo2 at JFK
           expr('At(C3, ATL)'),  # Cargo3 at ATL
           expr('At(C4, ORD)'),  # Cargo4 at ORD
           expr('At(P1, SFO)'),  # Plane1 at SFO
           expr('At(P2, JFK)'),  # Plane2 at JFK
           ]
    neg = [
           expr('At(C4, SFO)'),  # Cargo4 not at SFO
           expr('At(C4, JFK)'),  # Cargo4 not at JFK
           expr('At(C4, ATL)'),  # Cargo4 not at ATL
           expr('In(C4, P1)'),  # Cargo4 not in P1
           expr('In(C4, P2)'),  # Cargo4 not in P2
           expr('At(C3, SFO)'),  # Cargo3 not at SFO
           expr('At(C3, JFK)'),  # Cargo3 not at JFK
           expr('At(C3, ORD)'),  # Cargo3 not at ORD
           expr('In(C3, P1)'),   # Cargo3 not in P1
           expr('In(C3, P2)'),   # Cargo3 not in P2
           expr('At(C2, SFO)'),  #Cargo2 not at SFO
           expr('At(C2, ATL)'),  #Cargo2 not at ATL
           expr('At(C2, ORD)'),  # Cargo2 not at ORD
           expr('In(C2, P1)'),  #Cargo2 not in P1
           expr('In(C2, P2)'),  #Cargo2 not in P2
           expr('At(C1, JFK)'),  #Cargo1 not at JFK
           expr('At(C1, ATL)'),  # Cargo1 not at ATL
           expr('At(C1, ORD)'),  # Cargo1 not at ORD
           expr('In(C1, P1)'),  #Cargo1 not in P1
           expr('In(C1, P2)'),  #Cargo1 not in P2
           expr('At(P1, JFK)'),  #Plane1 not at JFK
           expr('At(P1, ATL)'),  # Plane1 not at ATL
           expr('At(P1, ORD)'),  # Plane1 not at ORD
           expr('At(P2, SFO)'),   #Plane2 not at SFO
           expr('At(P2, ATL)'),  # Plane2 not at ATL
           expr('At(P2, ORD)'),  # Plane2 not at ORD
           ]
    init = FluentState(pos, neg)
    goal = [expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            expr('At(C3, JFK)'),
            expr('At(C4, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)
