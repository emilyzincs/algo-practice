from user_testing.test_generation import generation_util as util
from typing import TypeVar, Callable, cast
import random

WeightedGraph = list[list[tuple[int, int]]]
UnweightedGraph = list[list[int]]
Graph = TypeVar('Graph', UnweightedGraph, WeightedGraph)


def get_graphs_with_rand_vertices(graphs: list[Graph], num_rand_vertices: int):
  graphs_with_rand_vertices = []
  for graph in graphs:
    rand_vertices: list[int] = [rand_vertex(graph) for _ in range(num_rand_vertices)]
    graph_with_rand_vertices = (graph, *rand_vertices)
    graphs_with_rand_vertices.append(graph_with_rand_vertices)
  return graphs_with_rand_vertices


def get_weighted_graphs(directed: bool, connected: bool, lo: int, hi: int):
  weighted_graphs: list[WeightedGraph]

  unweighted_graphs: list[UnweightedGraph] = (
    get_unweighted_graphs(directed, connected)
  )

  for unweighted_graph in unweighted_graphs:
    weighted_graph: WeightedGraph = (
      weight_graph_random(unweighted_graph, directed, lo, hi)
    )
    weighted_graphs.append(weighted_graph)
  return weighted_graphs
    

def get_unweighted_graphs(directed: bool, connected: bool) -> list[UnweightedGraph]:
  graphs: list[UnweightedGraph] = []
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
  graphs: list[UnweightedGraph], 
  num_vertices: int, 
  directed: bool,
  connected: bool, 
  edge_prob: float,
) -> None:
  graphs.append(rand_graph(num_vertices, directed, connected, edge_prob))


def add_random_cases(
    graphs: list[UnweightedGraph], 
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
    graphs: list[UnweightedGraph], 
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


def graph_list_to_tuple(graph: UnweightedGraph) -> tuple[tuple[int, ...], ...]:
  return tuple(tuple(adj_list) for adj_list in graph)


def rand_vertex(graph: Graph) -> int:
  n = len(graph)
  if n == 0:
    raise ValueError("Cannot pick random vertex since graph has no vertices")
  return random.randint(0, n-1)


def rand_graph_and_root(
    num_vertices: int, 
    directed: bool, 
    connected: bool, 
    edge_prob: float
) -> tuple[UnweightedGraph, int]: 
  graph = rand_graph(num_vertices, directed, connected,  edge_prob)
  root = rand_vertex(graph)
  return graph, root


def connect_graph(graph: UnweightedGraph, directed: bool) -> None:
  n = len(graph)
  if n == 0:
    return
  for i in range(1, n):
    if i not in graph[i-1]:
      graph[i-1].append(i)
    if not directed and i-1 not in graph[i]:
      graph[i].append(i-1)
  if 0 not in graph[n-1]:
    graph[n-1].append(0)
  if not directed and n-1 not in graph[0]:
    graph[0].append(n-1)


def weight_graph_random(
    unweighted_graph: UnweightedGraph, 
    directed: bool, 
    lo: int, 
    hi: int
) -> WeightedGraph:
  return weight_graph_custom(
    unweighted_graph,
    directed,
    random.randint,
    *[lo, hi]
  )


def weight_graph_custom(
    unweighted_graph: UnweightedGraph, 
    directed: bool,
    get_weight_func: Callable[..., int], 
    *weight_func_args, 
    **weight_func_kwargs
) -> WeightedGraph:
  weighted_graph: WeightedGraph = []
  for curr_vertex, unweighted_neighbor_list in enumerate(unweighted_graph):
    weighted_neighbor_list: list[tuple[int, int]] = []

    for neighbor in unweighted_neighbor_list:
      weight: int = _get_weight(
        weighted_graph, 
        directed, 
        curr_vertex, 
        neighbor, 
        get_weight_func, 
        *weight_func_args, 
        **weight_func_kwargs
      )

      weighted_neighbor_list.append((neighbor, weight))  
    weighted_graph.append(weighted_neighbor_list)
  return weighted_graph


def _get_weight(
  weighted_graph: WeightedGraph, 
  directed: bool,
  curr_vertex: int,
  neighbor: int,
  get_weight_func: Callable[..., int], 
  *weight_func_args, 
  **weight_func_kwargs 
) -> int:
  if directed or curr_vertex <= neighbor:
    return get_weight_func(*weight_func_args, **weight_func_kwargs)
  else:
    for vertex, other_weight in weighted_graph[neighbor]:
      if vertex == curr_vertex:
        return other_weight
    raise ValueError(
      f"Missing reverse edge {neighbor} -> {curr_vertex} in undirected graph.")


def rand_graph(
    num_vertices: int, 
    directed: bool, 
    connected: bool, 
    edge_prob: float = 0.2
) -> UnweightedGraph:
  
  graph: UnweightedGraph = [[] for _ in range(num_vertices)]
  for i in range(num_vertices):
    for j in range(i+1, num_vertices):
      if util.rand_bool(edge_prob):
        graph[i].append(j)
        if directed and util.rand_bool(edge_prob):
          graph[j].append(i)
        elif not directed:
          graph[j].append(i)
  if connected:
    connect_graph(graph, directed) 
      
  return graph
