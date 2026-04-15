from user_testing.test_generation import generation_util as util
import random

def get_weighted_graphs(directed: bool, connected: bool, lo: float, hi: float):
  weighted_graphs: list[tuple[tuple[tuple[int, float], ...], ...]]

  unweighted_graphs: list[list[list[int]]] = (
    get_unweighted_graphs(directed, connected)
  )
  for unweighted_graph in unweighted_graphs:
    weighted_graph: list[list[list[tuple[int, float]]]]
    
      


      


def get_unweighted_graphs(directed: bool, connected: bool) -> list[list[list[int]]]:
  graphs: list[list[list[int]]] = []
  for i in range(3, 8):
    add_random_variety(graphs, directed, connected, i, 2)
  for i in range(15, 18):
    add_random_variety(graphs, directed, connected, i, 2)
  for i in range(49, 52):
    add_random_variety(graphs, directed, connected, i, 3)
  for i in range(99, 102):
    add_random_variety(graphs, directed, connected, i, 3)
  add_random_variety(graphs, directed, connected, 250, 3)
  return graphs


def add_random_case(
  graphs: list[list[list[int]]], 
  num_vertices: int, 
  directed: bool,
  connected: bool, 
  edge_prob: float,
) -> None:
  graphs.append(util.rand_graph(num_vertices, directed, connected, edge_prob))


def add_random_cases(
    graphs: list[list[list[int]]], 
    num_vertices: int, 
    directed: bool,
    connected: bool, 
    edge_prob: float,
    num_cases: int
) -> None:
  for _ in range(num_cases):
    add_random_case(graphs, num_vertices, directed, connected, edge_prob)
    

# Adds graphs generated with varying edge probabilities
def add_random_variety(
    graphs: list[list[list[int]]], 
    directed: bool,
    connected: bool,
    num_vertices: int, 
    num_cases_per: int
) -> None:
  edge_probs = None
  if num_vertices < 20:
    edge_probs = [0, 0.3, 0.5, 0.7, 1]
  elif num_vertices < 50:
    edge_probs = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
  else:
    edge_probs = [0, 0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95, 1]

  for i, edge_prob in enumerate(edge_probs):
    add_random_cases(graphs, num_vertices, 
                     directed, connected, edge_prob, num_cases_per)
    if util.rand_bool(0.9):
      continue
    
    if directed and not connected:
      add_random_case(graphs, num_vertices, 
                      directed=False, connected=True, edge_prob=edge_prob)
    if not connected and i < 3:
      add_random_case(graphs, num_vertices, 
                      directed=directed, connected=True, edge_prob=edge_prob)
    if directed and i < 3:
      add_random_case(graphs, num_vertices, 
                      directed=False, connected=connected, edge_prob=edge_prob)
