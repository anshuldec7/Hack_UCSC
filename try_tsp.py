##############################################################
#
# File :- try_tsp.py
#
#Description :- This file implements the TSp logic
#
#Author :- Team Fantastic4
#
###############################################################

import random
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def Distance(i, j):
  """will us for final amount calculation after optimal path"""

  return i + j


class RandomMatrix(object):
  """Random matrix."""

  def __init__(self, size, seed,list):
    """Initialize random matrix."""

    List1=list
    rand = random.Random()
    rand.seed(seed)

    self.matrix = {}
    for from_node in range(size):
      self.matrix[from_node] = {}
      for to_node in range(size):
        if from_node == to_node:
          self.matrix[from_node][to_node] = 0
        else:
          self.matrix[from_node][to_node] = List1[from_node][to_node]       #rand.randrange(distance_max)

  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]


def tsp(args,list):
  if args.Destination > 0:

    routing = pywrapcp.RoutingModel(args.Destination, 1, 0)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)


    matrix = RandomMatrix(args.Destination, args.tsp_random_seed,list)

    for k,v in  matrix.matrix.iteritems():
      print k, v


    matrix_callback = matrix.Distance



    if args.tsp_use_random_matrix:
      routing.SetArcCostEvaluatorOfAllVehicles(matrix_callback)
    else:
      routing.SetArcCostEvaluatorOfAllVehicles(Distance)

    rand = random.Random()
    rand.seed(args.tsp_random_seed)
    forbidden_connections = 0
    while forbidden_connections < args.tsp_random_forbidden_connections:
      from_node = rand.randrange(args.Destination - 1)
      to_node = rand.randrange(args.Destination - 1) + 1
      if routing.NextVar(from_node).Contains(to_node):
        print('Forbidding connection ' + str(from_node) + ' -> ' + str(to_node))
        routing.NextVar(from_node).RemoveValue(to_node)
        forbidden_connections += 1

    assignment = routing.Solve()
    if assignment:
      print(assignment.ObjectiveValue())


      Tsp_cor=[]
      route_number = 0
      node = routing.Start(route_number)
      route = ''
      while not routing.IsEnd(node):
        route += str(node) + ' -> '
        Tsp_cor.append(str(node))

        node = assignment.Value(routing.NextVar(node))
      route += '0'
      print(route)
      return Tsp_cor


    else:
      print('No solution found.')
  else:
    print('Specify an instance greater than 0.')
