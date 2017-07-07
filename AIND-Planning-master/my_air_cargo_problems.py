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
        print('Now in AirCargoProblem initiation...')
        self.state_map = initial.pos + initial.neg
        self.initial_state_TF = encode_state(initial, self.state_map)
        Problem.__init__(self, self.initial_state_TF, goal=goal)
        self.cargos = cargos
        print('cargos..',cargos)
        self.planes = planes
        print('planes..', planes)
        self.airports = airports
        print('airports..', airports)
        self.actions_list = self.get_actions()

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
            print('Now creating load actions....')
            loads = []

            # # TODO create all load ground actions from the domain Load action

            for c in self.cargos:
                for p in self.planes:
                    for a in self.airports:
                        # print('cargo',c,'plane',p,'airport',a)
                        #Construct strings to make into Action objects in the following format
                        # String = Load(C1, P1, SFO) [[In(C1,P1)^At(P1,SFO)],[]]    [[At(C1,SFO)^¬In(C1,P1))],[]]
                        # TODO create all load ground actions from the domain Load action
                        precond_pos = [expr("In({}, {})^At({},{})".format(c, p, p, a))]
                        precond_neg = []
                        effect_add = [expr("At({}, {})^In({},{})".format(c, a, c, p))]
                        effect_rem = []
                        #Use Action() function defined in aimacode.planning.py to create action object from the action expression
                        print(expr("Load({}, {}, {})".format(c, p, a)),
                              [precond_pos, precond_neg],
                              [effect_add, effect_rem])
                        loadAction = Action(expr("Load({}, {}, {})".format(c, p, a)),
                                              [precond_pos, precond_neg],
                                              [effect_add, effect_rem])

                        loads.append(loadAction)
                        # Add new action object to list of action objects
                        loads.append(loadAction)


            return loads

        def unload_actions():
            """Create all concrete Unload actions and return a list of action objects

            :return: list of Action objects
            """
            print('Now creating unload actions....')
            unloads = []
            # TODO create all Unload ground actions from the domain Unload action

            for c in self.cargos:
                for p in self.planes:
                    for a in self.airports:
                        # print('cargo',c,'plane',p,'airport',a)
                        #Construct strings to make into Action objects in the following format
                        # String = Unload(C1, P1, SFO) [[In(C1,P1)^At(P1,SFO)],[]]    [[At(C1,SFO)^¬In(C1,P1))],[]]
                        # TODO create all load ground actions from the domain Load action
                        precond_pos = [expr("In({}, {})^At({},{})".format(c, p, p, a))]
                        precond_neg = []
                        effect_add = [expr("At({}, {})".format(c, a, c, p))]
                        effect_rem = [expr("In({},{})".format(c,p))]
                        #Use Action() function defined in aimacode.planning.py to create action object from the action expression
                        print(expr("Unload({}, {}, {})".format(c, p, a)),
                              [precond_pos, precond_neg],
                              [effect_add, effect_rem])
                        unloadAction = Action(expr("Unload({}, {}, {})".format(c, p, a)),
                                              [precond_pos, precond_neg],
                                              [effect_add, effect_rem])

                        unloads.append(unloadAction)
                        # Add new action object to list of action objects
                        unloads.append(unloadAction)

            return unloads

        def fly_actions():
            """Create all concrete Fly actions and return a list of action objects

            :return: list of Action objects
            """
            print('Now creating all possible fly actions....')
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
                            print (expr("Fly({}, {}, {})".format(p, fr, to)),
                                         [precond_pos, precond_neg],
                                         [effect_add, effect_rem])
                            fly = Action(expr("Fly({}, {}, {})".format(p, fr, to)),
                                         [precond_pos, precond_neg],
                                         [effect_add, effect_rem])
            #Add new action object to list of action objects
                            flys.append(fly)

            #return list of action objects.
            return flys

        return load_actions() + unload_actions() + fly_actions()

    def actions(self, state: str) -> list:
        """ Return the actions that can be executed in the given state.

        :param state: str
            state represented as T/F string of mapped fluents (state variables)
            e.g. 'FTTTFF'
        :return: list of Action objects
        """
        # TODO implement
        possible_actions = []
        return possible_actions

    def result(self, state: str, action: Action):
        """ Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        :param state: state entering node
        :param action: Action applied
        :return: resulting state after action
        """
        # TODO implement
        new_state = FluentState([], [])
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
        """
        # TODO implement (see Russell-Norvig Ed-3 10.2.3  or Russell-Norvig Ed-2 11.2)
        count = 0
        return count


def air_cargo_p1() -> AirCargoProblem:
    print('Creating problem 1....')
    print('Initial state = [Cargo1 at SFO, Plane 1 at SFO, Cargo2 at JFK, Plane2 at JFK])')
    print('Goal state = [Cargo2 at JFK and Cargo2 at SFO]')

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
           expr('At(C1, JFK)'),
           expr('In(C1, P1)'),
           expr('In(C1, P2)'),
           expr('At(P1, JFK)'),
           expr('At(P2, SFO)'),
           ]
    init = FluentState(pos, neg)
    goal = [expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p2() -> AirCargoProblem:
    # TODO implement Problem 2 definition
    pass


def air_cargo_p3() -> AirCargoProblem:
    # TODO implement Problem 3 definition
    pass
