from heuristic_search.pqueue import PriorityQueue
from heuristic_search.node import Node
import sys
import time




def astar(problem):

    # initialization of timer (used to measure the time
    # taken in the computation)
    start_time = time.time()

    branches_taken = 0

    closed = PriorityQueue()

    front = PriorityQueue()

    start_node = Node(problem.start_state)
    #start_node = DCStarNode(problem.start_state)

    #estimated_node = (problem.estimate_cost(start_node.path()), start_node)
    #estimated_node = (problem.estimate_cost(start_node), start_node)
    estimated_node = ((0, 0, 0), start_node)

    front.put(estimated_node)

    while not front.empty():

        branches_taken = branches_taken + 1

        # depending if the verbose mode is chosen, the correct
        # on-screen printing is shown
        if problem.verbose:
            sys.stdout.write('\r' + "Evaluating node #" + str(branches_taken))
        else:
            sys.stdout.write('\r' + "Evaluating" + str('.' * (branches_taken % 25)))

        #(path_estimated_cost, current_node) = front.get()
        (estimated_cost, current_node) = front.get()

        current_state = current_node.state

        #if not problem.unique_successors:
        if closed.find(current_state) is None:
            #closed.put((path_estimated_cost, current_node))
            closed.put((estimated_cost, current_node))

        if problem.goal(current_state):
            #return (current_node.path(), branches_taken)
            return current_node.state, branches_taken, time.time() - start_time

        else:

            successors = problem.successors(current_state)

            for successor_state in successors:

                successor_node = Node(successor_state, parent_node = current_node)

                #path_estimated_cost = problem.estimate_cost(successor_node.path())
                estimated_cost = problem.estimate_cost(successor_node)

                #if not problem.unique_successors:
                if closed.find(current_state) is not None:

                    estimated_node = front.find(successor_state)

                    if estimated_node is not None:

                        #if path_estimated_cost < estimated_node[0]:
                        if estimated_cost < estimated_node[0]:

                            front.remove(estimated_node)

                            #front.put((path_estimated_cost, successor_node))
                            front.put((estimated_cost, successor_node))

                    else:

                        estimated_node = closed.find(successor_state)

                        if estimated_node is not None:

                            #if path_estimated_cost < estimated_node[0]:
                            if estimated_cost < estimated_node[0]:

                                #front.put((path_estimated_cost, successor_node))
                                front.put((estimated_cost, successor_node))

                                closed.remove(estimated_node)

                        else:
                            #front.put((path_estimated_cost, successor_node))
                            front.put((estimated_cost, successor_node))

                else:
                    #front.put((path_estimated_cost, successor_node))
                    front.put((estimated_cost, successor_node))

    return None, branches_taken, time.time() - start_time
