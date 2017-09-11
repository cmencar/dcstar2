from heuristic_search.pqueue import PriorityQueue
from heuristic_search.node import Node


def astar(problem):
    closed = PriorityQueue()
    front = PriorityQueue()  # unlimited priority queue

    start_node = Node(problem.start_state)

    estimated_node = (problem.estimate_cost(start_node.path()), problem.start_state)
    front.put(estimated_node)

    while not front.empty():
        (path_estimated_cost, current_node) = front.get()
        current_state = current_node.state
        if not problem.unique_successors:
            closed.put((path_estimated_cost, current_node))
        if problem.goal(current_state):
            return current_node.path()  # solution found!
        else:
            successors = problem.successors(current_state)
            for successor_state in successors:
                # improve
                successor_node = Node(successor_state, parent_node=current_node)
                path_estimated_cost = problem.estimate_cost(successor_node.path())
                if not problem.unique_successors:
                    estimated_node = front.find(successor_state)
                    if estimated_node is not None:
                        if path_estimated_cost < estimated_node[0]:
                            front.remove(estimated_node)
                            front.put((path_estimated_cost, successor_node))
                    else:
                        estimated_node = closed.find(successor_state)
                        if estimated_node is not None:
                            if path_estimated_cost < estimated_node[0]:
                                front.put((path_estimated_cost, successor_node))
                                closed.remove(estimated_node)
                        else:
                            front.put((path_estimated_cost, successor_node))
                else:
                    front.put((path_estimated_cost, successor_node))
    return None  # no solution found
