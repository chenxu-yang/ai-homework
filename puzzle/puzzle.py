
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import resource
import psutil
import queue as Q


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index<3:
            return None
        config=self.config[:]
        n=self.n
        blank_index=self.blank_index
        cost=self.cost+1
        action='Up'
        config[blank_index],config[blank_index-3]=config[blank_index-3],config[blank_index]
        return PuzzleState(config,n,self,action,cost)

      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index > 5:
            return None
        config = self.config[:]
        n = self.n
        blank_index = self.blank_index
        cost = self.cost + 1
        action = 'Down'
        config[blank_index], config[blank_index + 3] = config[blank_index + 3], config[blank_index]
        return PuzzleState(config, n, self, action, cost)
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index in [0,3,6]:
            return None
        config = self.config[:]
        n = self.n
        blank_index = self.blank_index
        cost = self.cost + 1
        action = 'Left'
        config[blank_index], config[blank_index - 1] = config[blank_index - 1], config[blank_index]
        return PuzzleState(config, n, self, action, cost)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index in [2, 5, 8]:
            return None
        config = self.config[:]
        n = self.n
        blank_index = self.blank_index
        cost = self.cost + 1
        action = 'Right'
        config[blank_index], config[blank_index + 1] = config[blank_index + 1], config[blank_index]
        return PuzzleState(config, n, self, action, cost)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
class solver(object):
    def __init__(self,initial_state):
        self.initial_state=initial_state
        self.path_to_goal=[]
        self.cost=0
        self.nodes_expanded=0
        self.search_depth=0
        self.max_search_depth=0
        self.running_time=0
        self.max_ram_usage=0
    def writeOutput(self):
        file = open('output.txt', 'w')
        file.write("path_to_goal: [" + str(self.path_to_goal) + "]")
        file.write("\ncost_of_path:")
        file.write(str(self.cost))
        file.write("\nnodes_expanded:")
        file.write(str(self.nodes_expanded))
        file.write("\nsearch_depth:")
        file.write(str(self.search_depth))
        file.write("\nmax_search_depth:")
        file.write(str(self.max_search_depth))
        file.write("\nrunning_time: %.8f" % (self.running_time))
        file.write("\nmax_ram_usage: %.8f" % (self.max_ram_usage))

    def bfs_search(self,initial_state):
        """BFS search"""
        ### STUDENT CODE GOES HERE ###
        start_time=time.time()
        queue=[initial_state]
        visited=set()
        visited.add(tuple(initial_state.config))
        while queue:
            cur_state=queue.pop(0)
            flag=0
            if self.test_goal(cur_state):
                level=0
                path=[]
                while cur_state.parent:
                    path.append(cur_state.action)
                    level+=1
                    cur_state=cur_state.parent
                self.search_depth=level
                self.cost=len(path)
                self.path_to_goal=path[::-1]
                end_time=time.time()
                self.running_time=end_time-start_time
                self.max_ram_usage = max(self.max_ram_usage,resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024)
                return self.writeOutput()
            self.nodes_expanded += 1

            for neighbor in cur_state.expand():
                if tuple(neighbor.config) not in visited:
                    queue.append(neighbor)
                    visited.add(tuple(neighbor.config))
                    flag=1
            if flag:
                self.max_search_depth=max(self.max_search_depth,cur_state.cost+1)




    def dfs_search(self,initial_state):
        """DFS search"""
        start_time=time.time()
        stack=[initial_state]
        visited=set()
        visited.add(tuple(initial_state.config))
        while stack:
            cur_state=stack.pop()
            flag=0
            if self.test_goal(cur_state):
                level = 0
                path = []
                while cur_state.parent:
                    path.append(cur_state.action)
                    level += 1
                    cur_state = cur_state.parent
                self.search_depth = level
                self.cost = len(path)
                self.path_to_goal = path[::-1]
                end_time = time.time()
                self.running_time = end_time - start_time
                self.max_ram_usage = max(self.max_ram_usage,resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024)
                return self.writeOutput()
            self.nodes_expanded+=1

            for neighbor in cur_state.expand()[::-1]:
                if tuple(neighbor.config) not in visited:
                    stack.append(neighbor)
                    visited.add(tuple(neighbor.config))
                    flag=1
            if flag:
                self.max_search_depth = max(self.max_search_depth, cur_state.cost+1)


    def A_star_search(self,initial_state):
        """A * search"""
        ### STUDENT CODE GOES HERE ###
        start_time = time.time()
        queue = Q.PriorityQueue()
        order=0
        queue.put([self.calculate_total_cost(initial_state),0,initial_state])
        visited = set()
        visited.add(tuple(initial_state.config))
        while queue:
            cur_state = queue.get()[2]
            flag = 0
            if self.test_goal(cur_state):
                level = 0
                path = []
                while cur_state.parent:
                    path.append(cur_state.action)
                    level += 1
                    cur_state = cur_state.parent
                self.search_depth = level
                self.cost = len(path)
                self.path_to_goal = path[::-1]
                end_time = time.time()
                self.running_time = end_time - start_time
                self.max_ram_usage = max(self.max_ram_usage,resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024)
                return self.writeOutput()
            self.nodes_expanded += 1
            for neighbor in cur_state.expand():
                if tuple(neighbor.config) not in visited:
                    order+=1
                    queue.put([self.calculate_total_cost(neighbor),order,neighbor])
                    visited.add(tuple(neighbor.config))
                    flag = 1
            if flag:
                self.max_search_depth = max(self.max_search_depth, cur_state.cost + 1)

    def calculate_total_cost(self,state):
        """calculate the total estimated cost of a state"""
        ### STUDENT CODE GOES HERE ###
        return state.cost+self.calculate_manhattan_dist(state)

    def calculate_manhattan_dist(self,state):
        """calculate the manhattan distance of a tile"""
        ### STUDENT CODE GOES HERE ###
        dis=0
        for i in range(state.n**2):
            num=state.config[i]
            if num!=0:
                dis+=abs(i%state.n-num%state.n)+abs(i//state.n-num//state.n)
        return dis

    def test_goal(self,puzzle_state):
        """test the state is the goal state or not"""
        ### STUDENT CODE GOES HERE ###
        return puzzle_state.config==[0,1,2,3,4,5,6,7,8]

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    my_solver=solver(hard_state)
    if   search_mode == "bfs": my_solver.bfs_search(hard_state)
    elif search_mode == "dfs": my_solver.dfs_search(hard_state)
    elif search_mode == "ast": my_solver.A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()