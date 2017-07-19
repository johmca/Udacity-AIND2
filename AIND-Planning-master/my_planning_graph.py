from aimacode.planning import Action
from aimacode.search import Problem
from aimacode.utils import expr
from lp_utils import decode_state


class PgNode():
    """Base class for planning graph nodes.

    includes instance sets common to both types of nodes used in a planning graph
    * parents: the set of nodes in the previous level
    * children: the set of nodes in the subsequent level
    * mutex: the set of sibling nodes that are mutually exclusive with this node
    """

    def __init__(self):
        self.parents = set()
        self.children = set()
        self.mutex = set()

    def is_mutex(self, other) -> bool:
        """Boolean test for mutual exclusion

        :param other: PgNode
            the other node to compare with
        :return: bool
            True if this node and the other are marked mutually exclusive (mutex)
        """
        if other in self.mutex:
            return True
        return False

    def show(self):
        """helper print for debugging shows counts of parents, children, siblings

        :return:
            print only
        """
        print("{} parents".format(len(self.parents)))
        print("{} children".format(len(self.children)))
        print("{} mutex".format(len(self.mutex)))


class PgNode_s(PgNode):
    """A planning graph node representing a state (literal fluent) from a
    planning problem.

    Args:
    ----------
    symbol : str
        A string representing a literal expression from a planning problem
        domain.

    is_pos : bool
        Boolean flag indicating whether the literal expression is positive or
        negative.
    """

    def __init__(self, symbol: str, is_pos: bool):
        """S-level Planning Graph node constructor

        :param symbol: expr
        :param is_pos: bool

        Instance variables calculated:
            literal: expr
                    fluent in its literal form including negative operator if applicable

        Instance variables inherited from PgNode:
            parents: set of nodes connected to this node in previous A level; initially empty
            children: set of nodes connected to this node in next A level; initially empty
            mutex: set of sibling S-nodes that this node has mutual exclusion with; initially empty
        """
        PgNode.__init__(self)
        self.symbol = symbol
        self.is_pos = is_pos
        self.__hash = None

    def show(self):
        """helper print for debugging shows literal plus counts of parents,
        children, siblings

        :return:
            print only
        """
        if self.is_pos:
            print("\n*** {}".format(self.symbol))
        else:
            print("\n*** ~{}".format(self.symbol))
        PgNode.show(self)

    def __eq__(self, other):
        """equality test for nodes - compares only the literal for equality

        :param other: PgNode_s
        :return: bool
        """
        return (isinstance(other, self.__class__) and
                self.is_pos == other.is_pos and
                self.symbol == other.symbol)

    def __hash__(self):
        self.__hash = self.__hash or hash(self.symbol) ^ hash(self.is_pos)
        return self.__hash


class PgNode_a(PgNode):
    """A-type (action) Planning Graph node - inherited from PgNode """


    def __init__(self, action: Action):
        """A-level Planning Graph node constructor

        :param action: Action
            a ground action, i.e. this action cannot contain any variables
        Instance variables calculated:
            An A-level will always have an S-level as its parent and an S-level as its child.
            The preconditions and effects will become the parents and children of the A-level node
            However, when this node is created, it is not yet connected to the graph
            prenodes: set of *possible* parent S-nodes
            effnodes: set of *possible* child S-nodes
            is_persistent: bool   True if this is a persistence action, i.e. a no-op action
        Instance variables inherited from PgNode:
            parents: set of nodes connected to this node in previous S level; initially empty
            children: set of nodes connected to this node in next S level; initially empty
            mutex: set of sibling A-nodes that this node has mutual exclusion with; initially empty
        """
        PgNode.__init__(self)
        self.action = action
        self.prenodes = self.precond_s_nodes()
        self.effnodes = self.effect_s_nodes()
        self.is_persistent = self.prenodes == self.effnodes
        self.__hash = None

    def show(self):
        """helper print for debugging shows action plus counts of parents, children, siblings

        :return:
            print only
        """
        print("\n*** {!s}".format(self.action))
        PgNode.show(self)

    def precond_s_nodes(self):
        """precondition literals as S-nodes (represents possible parents for this node).
        It is computationally expensive to call this function; it is only called by the
        class constructor to populate the `prenodes` attribute.

        :return: set of PgNode_s
        """
        nodes = set()
        for p in self.action.precond_pos:
            nodes.add(PgNode_s(p, True))
        for p in self.action.precond_neg:
            nodes.add(PgNode_s(p, False))
        return nodes

    def effect_s_nodes(self):
        """effect literals as S-nodes (represents possible children for this node).
        It is computationally expensive to call this function; it is only called by the
        class constructor to populate the `effnodes` attribute.

        :return: set of PgNode_s
        """
        nodes = set()
        for e in self.action.effect_add:
            nodes.add(PgNode_s(e, True))
        for e in self.action.effect_rem:
            nodes.add(PgNode_s(e, False))
        return nodes

    def __eq__(self, other):
        """equality test for nodes - compares only the action name for equality

        :param other: PgNode_a
        :return: bool
        """
        return (isinstance(other, self.__class__) and
                self.is_persistent == other.is_persistent and
                self.action.name == other.action.name and
                self.action.args == other.action.args)

    def __hash__(self):
        self.__hash = self.__hash or hash(self.action.name) ^ hash(self.action.args)
        return self.__hash


def mutexify(node1: PgNode, node2: PgNode):
    """ adds sibling nodes to each other's mutual exclusion (mutex) set. These should be sibling nodes!

    :param node1: PgNode (or inherited PgNode_a, PgNode_s types)
    :param node2: PgNode (or inherited PgNode_a, PgNode_s types)
    :return:
        node mutex sets modified
    """
    if type(node1) != type(node2):
        raise TypeError('Attempted to mutex two nodes of different types')
    node1.mutex.add(node2)
    node2.mutex.add(node1)


class PlanningGraph():
    """
    A planning graph as described in chapter 10 of the AIMA text. The planning
    graph can be used to reason about 
    """

    def __init__(self, problem: Problem, state: str, serial_planning=True):
        """
        :param self is Planning Graph object that we are creating as new
        :param problem: PlanningProblem (or subclass such as AirCargoProblem or HaveCakeProblem)
        :param state: str (will be in form TFTTFF... representing fluent states)
        :param serial_planning: bool (whether or not to assume that only one action can occur at a time)
        Instance variable calculated:
            fs: FluentState
                the state represented as positive and negative fluent literal lists
            all_actions: list of the PlanningProblem valid ground actions combined with calculated no-op actions
            s_levels: list of sets of PgNode_s, where each set in the list represents an S-level in the planning graph
            a_levels: list of sets of PgNode_a, where each set in the list represents an A-level in the planning graph
        """
        print('Now running PlanningGraph initiation....')
        #Add data to Plannin Graph object
        self.problem = problem
        self.fs = decode_state(state, problem.state_map) #Decode the state TTFF string and map to give lists (+ve and -ve) of fluents in state
        self.serial = serial_planning
        self.all_actions = self.problem.actions_list + self.noop_actions(self.problem.state_map)
        self.s_levels = []
        self.a_levels = []
        self.create_graph() #call function to build the planning graph

    def noop_actions(self, literal_list):
        """create persistent action for each possible fluent

        "No-Op" actions are virtual actions (i.e., actions that only exist in
        the planning graph, not in the planning problem domain) that operate
        on each fluent (literal expression) from the problem domain. No op
        actions "pass through" the literal expressions from one level of the
        planning graph to the next.

        The no-op action list requires both a positive and a negative action
        for each literal expression. Positive no-op actions require the literal
        as a positive precondition and add the literal expression as an effect
        in the output, and negative no-op actions require the literal as a
        negative precondition and remove the literal expression as an effect in
        the output.

        This function should only be called by the class constructor.

        :param literal_list:
        :return: list of Action
        """
        action_list = []
        for fluent in literal_list:
            act1 = Action(expr("Noop_pos({})".format(fluent)), ([fluent], []), ([fluent], []))
            action_list.append(act1)
            act2 = Action(expr("Noop_neg({})".format(fluent)), ([], [fluent]), ([], [fluent]))
            action_list.append(act2)
        return action_list

    def create_graph(self):
        """ build a Planning Graph as described in Russell-Norvig 3rd Ed 10.3 or 2nd Ed 11.4

        The S0 initial level has been implemented for you.  It has no parents and includes all of
        the literal fluents that are part of the initial state passed to the constructor.  At the start
        of a problem planning search, this will be the same as the initial state of the problem.  However,
        the planning graph can be built from any state in the Planning Problem

        This function should only be called by the class constructor.

        :return:
            builds the graph by filling s_levels[] and a_levels[] lists with node sets for each level
        """
        # the graph should only be built during class construction
        if (len(self.s_levels) != 0) or (len(self.a_levels) != 0):
            raise Exception(
                'Planning Graph already created; construct a new planning graph for each new state in the planning sequence')

        # initialize S0 to literals in initial state provided.
        leveled = False
        level = 0
        self.s_levels.append(set())  # S0 set of s_nodes - empty to start
        # They have done the logic for S0 for us already!
        # for each fluent in the initial state, positive and negative, add the correct literal PgNode_s to s_Levels
        # list where each element represents a state level in the planning graph
        for literal in self.fs.pos:
            self.s_levels[level].add(PgNode_s(literal, True))
        for literal in self.fs.neg:
            self.s_levels[level].add(PgNode_s(literal, False))
        # no mutexes at the first level

        # continue to build the graph alternating A, S levels until last two S levels contain the same literals,
        # i.e. until it is "leveled"
        while not leveled:
            #Build action layer of plannin ggraph
            self.add_action_level(level)
            # Build mutually exclusive relationships between actions
            self.update_a_mutex(self.a_levels[level])

            level += 1 #Increment level count and move to build next level of planning graph

            self.add_literal_level(level) #JM - call add_literal() here passing level to build next state layer of planning graph

            self.update_s_mutex(self.s_levels[level])

            if self.s_levels[level] == self.s_levels[level - 1]:
                leveled = True

    def add_action_level(self, level):
        """ add an A (action) level to the Planning Graph

        :param level: int
            the level number alternates S0, A0, S1, A1, S2, .... etc the level number is also used as the
            index for the node set lists self.a_levels[] and self.s_levels[]
        :return: None but adds A nodes to the current level in self.a_levels[level]
        """
        # TODO add action A level to the planning graph as described in the Russell-Norvig text
        # 1. determine what actions to add and create those PgNode_a objects
        # 2. connect the nodes to the previous S literal level

        # for example, the A0 level will iterate through all possible actions for the problem and add a PgNode_a to
        # the a_levels[0] set if all prerequisite literals for the action hold in S0.  This can be accomplished by testing
        # to see if a proposed PgNode_a has pre-nodes that are a subset of the previous S level.  Once an
        # action node is added, it MUST be connected to the S node instances in the appropriate s_level set.
        self.a_levels.append(set())
        for action in self.all_actions:#Read through list of all possible actions
            new_action_node=PgNode_a(action) #Create new action node from the action
            #Test if action node is applicable at the this State by checking if its pre-node set of literals is contained
            #within the set of state literals belonging to the state (at same level)
            # e.g. An action, Eat Cake, will have a pre-node of Have Cake and
            # for the action Eat Cake to be added Have Cake literal must exist in the State literals at this same level
            if new_action_node.prenodes.issubset(self.s_levels[level]):
                print('Action ',action, 'can be applied at level', level,'Adding action node')
                # Add action node to planning graph at this level
                # a_levels is a list with each element being a set of nodes
                self.a_levels[level].add(new_action_node)

                #Link the new action node to the related state nodes as a child and link the related state nodes to the
                #new action node as parents
                    #Read round the nodes of the state at the same level
                    #If state node is a precondition of the action node then
                        # 1. add the action node as a child of the state node
                        # 2. add the state node as a parent of the action node
                for state_node in self.s_levels[level]:
                    print('State node', state_node)
                    if state_node in new_action_node.prenodes:
                        print('State node',state_node.symbol,'is pre-condition of new node')
                        state_node.children.add(new_action_node)
                        new_action_node.parents.add(state_node)

    def add_literal_level(self, level):
        """ add an S (literal) level to the Planning Graph

        :param level: int
            the level number alternates S0, A0, S1, A1, S2, .... etc the level number is also used as the
            index for the node set lists self.a_levels[] and self.s_levels[]
        :return: None but adds S nodes to the current level in self.s_levels[level]
        """
        # TODO add literal S level to the planning graph as described in the Russell-Norvig text
        # 1. determine what literals to add (these are the results of actions in previous level of graph)
        # 2. connect the nodes
        # for example, every A node in the previous level has a list of S nodes in effnodes that represent the effect
        #   produced by the action.  These literals will all be part of the new S level.  Since we are working with sets, they
        #   may be "added" to the set without fear of duplication.  However, it is important to then correctly create and connect
        #   all of the new S nodes as children of all the A nodes that could produce them, and likewise add the A nodes to the
        #   parent sets of the S nodes

        # s_levels is a list with each element being a set of state literals. Add another element to the list and make
        # it contain an empty set
        self.s_levels.append(set())

        #Read actions at previous level and for each action read through its effects creating a state literal at this
        #level for each effect. Next link the state literal to the action.
        # i) the action should have the new state literal added as a child
        #ii) the state literal should have the action as a parent
        for action_node in self.a_levels[level -1]:
            # print('Action node',action_node)
            for state_node in action_node.effnodes: #effnodes is a set of nodes which are the states resultign from actions
                # print('Effect node',state_node)
                self.s_levels[level].add(state_node) #Add each action effect node as state node at this level
                action_node.children.add(state_node) #Set the state node as a child of the action node
                state_node.parents.add(action_node) #Set the action node as the parent of the state node



    def update_a_mutex(self, nodeset):
        """ Determine and update sibling mutual exclusion for A-level nodes

        Mutex action tests section from 3rd Ed. 10.3 or 2nd Ed. 11.4
        A mutex relation holds between two actions a given level
        if the planning graph is a serial planning graph and the pair are non-persistence actions
        or if any of the three conditions hold between the pair:
           Inconsistent Effects
           Interference
           Competing needs

        :param nodeset: set of PgNode_a nodes(action siblings in the same level)
        :return:
            mutex set in each PgNode_a in the set is appropriately updated
        """
        nodelist = list(nodeset)
        for i, n1 in enumerate(nodelist[:-1]):
            for n2 in nodelist[i + 1:]:
                if (self.serialize_actions(n1, n2) or
                        self.inconsistent_effects_mutex(n1, n2) or
                        self.interference_mutex(n1, n2) or
                        self.competing_needs_mutex(n1, n2)):
                    mutexify(n1, n2)

    def serialize_actions(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
        """
        Test a pair of actions for mutual exclusion, returning True if the
        planning graph is serial, and if either action is persistent; otherwise
        return False.  Two serial actions are mutually exclusive if they are
        both non-persistent.

        :param node_a1: PgNode_a
        :param node_a2: PgNode_a
        :return: bool
        """
        #
        if not self.serial:
            return False
        if node_a1.is_persistent or node_a2.is_persistent:
            return False
        return True

    def inconsistent_effects_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
        """
        Test a pair of actions for inconsistent effects, returning True if
        one action negates an effect of the other, and False otherwise.

        HINT: The Action instance associated with an action node is accessible
        through the PgNode_a.action attribute. See the Action class
        documentation for details on accessing the effects and preconditions of
        an action.

        :param node_a1: PgNode_a
        :param node_a2: PgNode_a
        :return: bool
        """
        # TODO test for Inconsistent Effects between nodes

        #Read through the effect states of action node n1 and for each check if it negates an effect state listed in action
        #node n2
        #Note - I don't think I need to do this the other way round too i.e. n2 effect to n1 effect as I think its the
        #same thing?

        #First make the effect sets for action nodes n1 and n2 into lists
        nodea1_effect_list = list(node_a1.effnodes)
        nodea2_effect_list = list(node_a2.effnodes)

        #NOTE - enumurate function returns a tuple (counter, value)
        for i, nodea1_effect in enumerate(nodea1_effect_list):
            #print('Processing effect',i,'from node1',node_a1.action ,'effects=', nodea1_effect.symbol,'IsPos=',nodea1_effect.is_pos)
            #Now lookup the a2 effects list to see if we can find the same effect an dif we do then check if it has
            #the same sign (pos or neg). If the signs are opposite then we have effects which are inconsistent. Return
            #True
            for j, nodea2_effect in enumerate(nodea2_effect_list):
                # print('Processing effect', j, 'from node2', node_a2.action, 'effects=', nodea2_effect.symbol, 'IsPos=',
                #       nodea2_effect.is_pos)
                if nodea2_effect.symbol == nodea1_effect.symbol and nodea2_effect.is_pos!=nodea1_effect.is_pos:
                    # print('These actions are mutually exclusive')
                    return True


        return False

    def interference_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
        """
        Test a pair of actions for mutual exclusion, returning True if the 
        effect of one action is the negation of a precondition of the other.

        HINT: The Action instance associated with an action node is accessible
        through the PgNode_a.action attribute. See the Action class
        documentation for details on accessing the effects and preconditions of
        an action.

        :param node_a1: PgNode_a
        :param node_a2: PgNode_a
        :return: bool
        """
        # TODO test for Interference between nodes

        # Read through the effect states of action node n1 and for each check if it negates a precondition state of action
        # node n2

        # First make the effect sets for action nodes n1 and n2 into lists
        nodea1_effect_list = list(node_a1.effnodes)
        nodea2_precond_list = list(node_a2.prenodes)

        # print('Checking node1',node_a1.action,'against node2',node_a2.action,
        #       'for inconsistency i.e. there exists a node1 effect state that negates a node 2 precondition state')

        # NOTE - enumurate function returns a tuple (counter, value)
        for i, nodea1_effect in enumerate(nodea1_effect_list):
            # print('Processing effect', i, 'from node1', node_a1.action, 'effects=', nodea1_effect.symbol, 'IsPos=',
            #       nodea1_effect.is_pos)
            # Now lookup the a2 effects list to see if we can find the same effect an dif we do then check if it has
            # the same sign (pos or neg). If the signs are opposite then we have effects which are inconsistent. Return
            # True
            for j, nodea2_precond in enumerate(nodea2_precond_list):
                # print('Processing precond', j, 'from node2', node_a2.action, 'precond=', nodea2_precond.symbol, 'IsPos=',
                #       nodea2_precond.is_pos)
                if nodea2_precond.symbol == nodea1_effect.symbol and nodea2_precond.is_pos != nodea1_effect.is_pos:
                    # print('These actions are mutually exclusive due to inconsistency between effects and preconditions')
                    return True

        # Read through the effect states of action node n2 and for each check if it negates precondition state of action
        # node n1

        # print('Checking node2', node_a2.action, 'against node1', node_a1.action,
        #       'for inconsistency i.e. there exists a node2 effect state that negates a node 1 precondition state')

        # First make the effect sets for action nodes n1 and n2 into lists
        nodea1_precond_list = list(node_a1.prenodes)
        nodea2_effect_list = list(node_a2.effnodes)

        # NOTE - enumurate function returns a tuple (counter, value)
        for i, nodea2_effect in enumerate(nodea2_effect_list):
            # print('Processing effect', i, 'from node2', node_a2.action, 'effects=', nodea2_effect.symbol, 'IsPos=',
            #       nodea2_effect.is_pos)
            # Now lookup the a2 effects list to see if we can find the same effect an dif we do then check if it has
            # the same sign (pos or neg). If the signs are opposite then we have effects which are inconsistent. Return
            # True
            for j, nodea1_precond in enumerate(nodea1_precond_list):
                # print('Processing precond', j, 'from node1', node_a1.action, 'precond=', nodea1_precond.symbol, 'IsPos=',
                #       nodea1_precond.is_pos)
                if nodea1_precond.symbol == nodea2_effect.symbol and nodea1_precond.is_pos != nodea2_effect.is_pos:
                    # print('These actions are mutually exclusive due to inconsistency between effects and preconditions')
                    return True

        return False

    def competing_needs_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
        """
        Test a pair of actions for mutual exclusion, returning True if one of
        the precondition of one action is mutex with a precondition of the
        other action.

        :param node_a1: PgNode_a
        :param node_a2: PgNode_a
        :return: bool
        """

        # TODO test for Competing Needs between nodes

        # For a disussion of this mutex condition and why we use parents and not the precons please see..
        #  https://discussions.udacity.com/t/problem-with-test-competing-needs-mutex/227344/17
        #Basically this says that its not enough to test states in the precondition lists against each other as some
        #possible types of mutex are not recorded that way e.g. inconsistent support between literals. It tells us
        # to check the parents using the mutex() function.

        node1_parents = list(node_a1.parents)
        node2_parents = list(node_a2.parents)

        # print('Running competing needs mutex...')

        for parent1 in node1_parents:
            for parent2 in node2_parents:
                if parent1.is_mutex(parent2): #This returns true if parent2 is found in the mutex list of parent1
                    return True

        return False

    def update_s_mutex(self, nodeset: set):
        """ Determine and update sibling mutual exclusion for S-level nodes

        Mutex action tests section from 3rd Ed. 10.3 or 2nd Ed. 11.4
        A mutex relation holds between literals at a given level
        if either of the two conditions hold between the pair:
           Negation
           Inconsistent support

        :param nodeset: set of PgNode_a (siblings in the same level)
        :return:
            mutex set in each PgNode_a in the set is appropriately updated
        """
        nodelist = list(nodeset)
        for i, n1 in enumerate(nodelist[:-1]):
            for n2 in nodelist[i + 1:]:
                if self.negation_mutex(n1, n2) or self.inconsistent_support_mutex(n1, n2):
                    mutexify(n1, n2)

    def negation_mutex(self, node_s1: PgNode_s, node_s2: PgNode_s) -> bool:
        """
        Test a pair of state literals for mutual exclusion, returning True if
        one node is the negation of the other, and False otherwise.

        HINT: Look at the PgNode_s.__eq__ defines the notion of equivalence for
        literal expression nodes, and the class tracks whether the literal is
        positive or negative.

        :param node_s1: PgNode_s
        :param node_s2: PgNode_s
        :return: bool
        """
        # TODO test for negation between nodes


        # print('Now running negation_Mutex()....')

        #Check if the s1 node is the negation of the s2 node
        if (node_s1.symbol == node_s2.symbol) and (node_s1.is_pos != node_s2.is_pos):
            return True

        return False

    def inconsistent_support_mutex(self, node_s1: PgNode_s, node_s2: PgNode_s):
        """
        Test a pair of state literals for mutual exclusion, returning True if
        there are no actions that could achieve the two literals at the same
        time, and False otherwise.

        In other words, the two literal nodes are mutex if ALL of the actions that could achieve the first literal node
        are pairwise mutually exclusive with ALL of the actions that could achieve the second literal node.

        From the book.."each possible pair of actions that could achieve the two literal are mutually exclusive."

        HINT: The PgNode.is_mutex method can be used to test whether two nodes
        are mutually exclusive.

        :param node_s1: PgNode_s
        :param node_s2: PgNode_s
        :return: bool
        """
        # TODO test for Inconsistent Support between nodes
        node1_parents = list(node_s1.parents)
        node2_parents = list(node_s2.parents)

        # print('Running inconsistent support mutex...')

        #Loop round node1's parent actions and test if these are mutex with node2's parent actions
        all_parentactions_mutex = True
        for node1_parent in  node1_parents:
            for node2_parent in node2_parents:
                if not(node1_parent.is_mutex(node2_parent)):  # This returns true if parent2 is found in the mutex list of parent1
                    all_parentactions_mutex = False

        #If all state 1 parent actions are mutex with state2 parent action then we have inconsistent support mutex..return True
        if all_parentactions_mutex == True:
            return True

        return False

    def h_levelsum(self) -> int:
        """The sum of the level costs of the individual goals (admissible if goals independent)
        e.g. For the Have Cake and Eat it problem our goal state Have Cake first appears at level 0 and our other
             goal state Eaten Cake first appears at level 1 therefore this heuristic would return 1 (0 +1)

        Note - I'm assuming that goal states can only be written in positive terms as the goals don't have any flags
               indicating + or - by which I mean we can have Eaten(cake) but never ¬Eaten(cake) as a goal
        :return: int
        """
        print('Running h_levelsum().....')

        #Read round the problem's goal states
        level_sum = 0
        for gs, goal_state in enumerate(self.problem.goal):
            print('Printing goal',gs,goal_state)
            #Find the first level the goal state appears at - start by reading through the array of state levels
            found = False
            for lvl, state_set in enumerate(self.s_levels):
                print('Looking in level',lvl)
                state_list = list(state_set)
                for state in state_list:
                    if state.symbol == goal_state and state.is_pos == True: #Assume goals are always +ve
                        print('Found goal state in level',lvl)
                        level_sum = level_sum + lvl
                        found = True
                        break
                if found == True: break

        return level_sum
