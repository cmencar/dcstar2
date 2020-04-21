from heuristic_search.pqueue import PriorityQueue
from heuristic_search.node import Node
import sys
import time


# Method for the execution of A* algorithm for the clustering problem
def astar(problem):

    # initialization of timer (used to measure the time taken in the computation) and number of branches taken
    start_time = time.time()
    branches_taken = 0

    # initialization of priority queues
    closed = PriorityQueue()
    front = PriorityQueue()

    # definition of the starting node for the evaluation and its starting cost. The starting node is now defined
    # as the first estimated node to be evaluated in problem computation
    start_node = Node(problem.start_state)
    estimated_node = ((0, 0, 0), start_node)
    front.put(estimated_node)

    # if the front priority queue is not empty means that are more nodes to be evaluated
    while not front.empty():

        # incrementing the branches taken counter
        branches_taken = branches_taken + 1

        # depending if the verbose mode is chosen, the correct on-screen printing is shown
        if problem.verbose:
            sys.stdout.write('\r' + "Evaluating node #" + str(branches_taken))
        else:
            sys.stdout.write('\r' + "Evaluating" + str('.' * (branches_taken % 5)))

        # acquiring the most promising node from front priority queue, i.e. the node with the best estimated_cost,
        # and initialize the current_state variable with the most promising node state (a DimensionalSequenceBinary object)
        (estimated_cost, current_node) = front.get()
        current_state = current_node.state

        # if it is not a unique successor then insert the current_node in closed queue. unique_successor means that
        # is impossible to find cycles in the evaluated path: consequently, the paths taken by the A* algorithm
        # are simple paths and, therefore, the macrostructure can be related back to a tree
        if not problem.unique_successors:
            closed.put((estimated_cost, current_node))

        # if the evaluated current_state is a possible result then return it and finish the execution early.
        # The information on current_State as a possible result is given by the goal function, which returns True
        # if the cut sequence defined by the state generates a set of hyperboxes all pure
        if problem.goal(current_state):
            return current_node.state, branches_taken, time.time() - start_time

        # if the evaluated current_State is not a possible result then define the list of successors of the
        # evaluated current_state. Those successors will be evaluated in the next steps.
        else:

            # define a list of successors taking the current_state and evaluate them one-by-one. The successors
            # are DimensionalSequenceBinary objects created by successors() method
            successors = problem.successors(current_state)
            for successor_state in successors:

                # create a Node object using the successor_state evaluated, i.e. a DimensionalSequenceBinary, and
                # estimate a cost using the three-levels priority values
                successor_node = Node(successor_state, parent_node = current_node)
                estimated_cost = problem.estimate_cost(successor_node)

                # if it is not a unique successor then there could be a duplicate node, i.e. a front priority
                # queue's node that has the same state as one of the newly created successors
                if not problem.unique_successors:

                    # Search if the evaluated successor state, i.e. a certain cut configuration defined by
                    # DimensionalSequenceBinary, is already present in a node in the front priority queue.
                    # If so (and, therefore, the value defined by estimated_node is different from None) then
                    # compare the cost value associated to this node with the cost value of the successor state,
                    # i.e. the amount defined by estimated_cost. If the cost value associated to the successor_state
                    # is lower than the value of the node already present, then the second is removed and the node
                    # of the evaluated successor_state replace it
                    estimated_node = front.find(successor_state)
                    if estimated_node is not None:
                        if estimated_cost < estimated_node[0]:
                            front.remove(estimated_node)
                            front.put((estimated_cost, successor_node))

                    # if the evaluated successor state is not present in a node in the front priority queue then
                    # search that node in the closed priority queue. If the evaluated successor_state is present in
                    # closed priority queue (and, therefore, the value defined by estimated_node is different from None)
                    # then compare the cost value associated to this node with the cost value of the successor state,
                    # i.e. the amount defined by estimated_cost. If the cost value associated to the successor_state
                    # is lower than the value of the node already present, then the second is inserted in front
                    # priority queue (with the already defined estimated_cost) and it is removed from closed priority queue.
                    # If the evaluated successor_state is not present in closed priority queue is a is a node that
                    # has not yet been evaluated (and consequently inserted in closed). So it is inserted in the front
                    # priority queue with the already defined estimated_cost and it could be evaluated in the next steps.
                    else:
                        estimated_node = closed.find(successor_state)
                        if estimated_node is not None:
                            if estimated_cost < estimated_node[0]:
                                front.put((estimated_cost, successor_node))
                                closed.remove(estimated_node)
                        else:
                            front.put((estimated_cost, successor_node))

                # if unique_successor is equal to false then the node is simply inserted in the front priority queue
                # with the estimated_cost value previously calculated
                else:
                    front.put((estimated_cost, successor_node))

    # if there are no possible results then it must return a None value for the result field
    return None, branches_taken, time.time() - start_time
