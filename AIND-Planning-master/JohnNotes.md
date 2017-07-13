#AIND Project 4 Planning - John's Notes




Running the Planning Search
---------------------------

To obtain help =>

python run_search.py -h


To run manually, selecting the problem and search algorithm by hand =>

python run_search.py -m

To run without manual selection use the numbers provided on manual secltion 

python run_search.py -p 1 -s 1 

runs for problem 1 and search 1 (BFS)

Unit Test
---------

Note - To run the local unit test script I needed to move the test script up to the main folder from the tests folder as it
could not resolve aimacode folder (it seemed to have the correct logic to do so but didn't work, dont know why). Anyways
after I moved it up I run as follows from main folder

python test_my_air_cargo_problems.py

I should have fixed this by setting the python path

1 Navigate to main project folder
2 set PYTHONPATH=.

The dot means "current working directory". So do this from within the directory where the aimacode subdirectory lives.

Now from the main project folder execute the uni test script with

python tests/test_my_air_cargo_problems.py

Note about the bit of code that says
if __name__ == '__main__':
    unittest.main()
    
is present for cases such as this when code is executed directly rather thna via an import into another module that is
executed. The code in this block runs only when the file is executed in this way.


What Happens when I Execute Run_Search.py?
------------------------------------------
main () receives the index number of the problem and search from the command line.
  - it looks these up in table of problem functions and table of search functions and gets a pointer to each 
     e.g. function air_cargo_p1 at 0x00000268FBAB8268 or function breadth_first_search at 0x00000268FBAB68C8
  - It does some sort of looping, perhaps you can provide multiple problems and search algos on the command?
  - at the heart of this loop it
      - creates a new instance of the problem by calling the problem function which is defined
        in file my_air_cargo_problems.py 
        
        e.g. There is a function air_cargo_p1 which defines a set of list variables to represent the problem
        in PDL
        
        *** I NEED TO DEFINE air_cargo_p2 and air_cargo_p3 BASED ON air_cargo_p1 PROVIDED ***
        
        These functions do their unique problem defintion set up by impementing the PDDL defintion of the problem 
        in python lists and then they call the cosntructor function for the AirCargoProblem class passing in the lists 
        of cargos, planes, airports (Syntax used for this is... def air_cargo_p1() -> AirCargoProblem:) and then 
        they call the getActions() function
       
        *** I NEED TO DEFINE getActions() INCLUDING ITS SUBFUNCTIONS load_actions() AND unload_actions() - BASE ***
        *** THIS ON THE fly_actions() FUNCTION PROVIDED                                                         ***

        get_actions() returns a list of action objects - unload action objects + load action objects + fly action objects.

        The loop then then executes method run_search() passing problem and  search_function.
        
        run_search executes the search function (selected by user and passed in as arg in the search_function variable 
        e.g. breadth_first_search at 0x00000268FBAB68C8. The search functions are defined in aimacode/search.py with 
        supporting data structures in aimacode/utils.py. The search functions seem to mainly execute the same 
        function using the different data structures according to the type of search. They all execute tree_search() 
        which is the generic tree graph search algo. They pass in a different data structure such as stack or prioritised 
        queue depending on search algo but they all call a function to expand the current node from the frontier and this 
        function is a method of the node class and is called expand(). 
        
        expand() returns the child nodes reachable in 1 step from the frontier node under exploration and in doing so 
        calls problem.actions() and problem.result() 
       
        *** the aircargo paroblem has an actions() method amd a result() method and I NEED TO CMPLETE THESE !!!
        
        - I DON'T KNOW HOW RESULT() IS CALLED BUT IT MUST BE IN ORDER TO
        APPLY THE ACTION TO THE CURRENT STATE TO GENERATE A CHILD TO BE ADDED TO THE FRONTIER!!!!!
        
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]
        
        ****** I NEED TO DO DEFINE ACTIONS())*****
        ****** problem.actions is back in my_air_cargo_problems.py and we must define this such that it accepts ***
        *****  a state and returns a list of action objects which are valid in that state                        ***
        
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
        
        ****** I NEED TO DO DEFINE RESULT()*****
        ****** Accept state and action to return new state *******
        
         def result(self, state: str, action: Action):
        """ Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        :param state: state entering node
        :param action: Action applied
        :return: resulting state after action
        """
        # TODO implement
        new_state = FluentState([], [])      ***** USES SUPPLIED FluentState() from lp_utils.py
        return encode_state(new_state, self.state_map)
        
        **********************************
        
        MY PLAN OF ATTACK................
        
       1. Get it working for air_cargo_problem1..so need to complete the following methods
            - AirCargoProblem.get_actions method including 
                - load_actions
                - unload_actions sub-functions 
            - AirCargoProblem.actions method 
            - AirCargoProblem.result method 
        
        2.  Define air_cargo_problem2 and air_cargo_problem3
        
        3. Conduct tests and gather performance data as required
        
        
        
        The search function returns a node (nodes consist of pointer to parent, action that got to 
        the node and the path cost to reach the node from the initial node)

        A printable version of the problem is created by the PrintableProblem() function and this is what gets passed to the
        search function.

        The search functions are all coded up in search.py under the aimacode folder and have been provided by Udacity.
        They look to be standard algorithms for things like BFS, DFS, UCS and A*. Data structures required to support these
        such as stacks and priority queues are coded in accompanying utils.py file.
        
        
        
        
        

Part 1 - To Do
---------------
In my_air_cargo_problems.py 
 - define the functions air_cargo_p2 and air_cargo_p3 (base these on air_cargo_p1 provided)

 - AirCargoProblem.get_actions method including load_actions and unload_actions sub-functions 
 - AirCargoProblem.actions method 
 - AirCargoProblem.result method 






