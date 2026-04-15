import random
from typing import Any


def get_null() -> None:
  return None


def get_empty_list() -> list[Any]:
  return []


def rand_array(size: int, lo: int, hi: int) -> tuple[int, ...]:
  return tuple([random.randint(lo, hi) for _ in range(size)])


def rand_big_arr() -> tuple[int, ...]:
  ret = []
  for i in range(-(10**4), 10**4):
    if rand_bool():
      ret.append(i)
      while rand_bool(0.2):
        ret.append(i)
  random.shuffle(ret)
  return tuple(ret)


def rand_sorted_big_arr() -> tuple[int, ...]:
  ret = []
  for i in range(-(10**4), 10**4):
    if rand_bool():
      ret.append(i)
      while rand_bool(0.2):
        ret.append(i)
  return tuple(ret)


def all_same_big_arr(value: int, size: int = 10**4) -> tuple[int, ...]:
  return tuple([value for _ in range(size)])


def rand_choice(arr: tuple[int, ...]):
  return random.choice(arr)


def rand_bool(probability_true: float = 0.5):
  return random.random() < probability_true


# Picks a target value that may or may not be present in the array.
def pick_target(arr: tuple[int, ...]) -> int:
  if len(arr) == 0:
    return 0
  if rand_bool():
    return rand_choice(arr)  # present
  else:
    return random.randint(min(arr)-1, max(arr)+1)  # maybe absent


# Generates a level‑order list for a random binary tree, with some None placeholders.
#
# Parameters:
# - n: Desired length of the list (may include trailing None values).
# - null_prob: Probability that a non‑root node is None (default 0.2).
#
# Returns:
#   A list of length n containing integers or None.
def rand_tree_array(n: int, null_prob: float = 0.2) -> list[int|None]:
  if n == 0:
    return []

  arr: list[int|None] = []
  for i in range(n):
    if i == 0 or not rand_bool(null_prob):
      arr.append(random.randint(-100, 100))
    else:
      arr.append(None)
  return arr


# Removes trailing None values from the given level‑order tree list 'arr'.
def trim_tree(arr: list[int]) -> list[int]:
  while arr and arr[-1] is None:
    arr.pop()
  return arr


def rand_graph(
    num_vertices: int, 
    directed: bool, 
    connected: bool, 
    edge_prob: float = 0.2
) -> list[list[int]]:
  
  graph: list[list[int]] = [[] for _ in range(num_vertices)]
  for i in range(num_vertices):
    for j in range(i+1, num_vertices):
      if rand_bool(edge_prob):
        graph[i].append(j)
        if directed and rand_bool(edge_prob):
          graph[j].append(i)
        elif not directed:
          graph[j].append(i)
  if connected:
    connect_graph(graph, directed) 
      
  return graph


def graph_list_to_tuple(graph: list[list[int]]) -> tuple[tuple[int, ...], ...]:
  return tuple(tuple(adj_list) for adj_list in graph)


def rand_vertex(graph: list[list[int]]) -> int:
  n = len(graph)
  if n == 0:
    raise ValueError("Cannot pick random vertex since graph has no vertices")
  return random.randint(0, n-1)


def rand_graph_and_root(num_vertices: int, directed: bool, connected: bool, 
                       edge_prob: float) -> tuple[list[list[int]], int]: 
  graph = rand_graph(num_vertices, directed, connected,  edge_prob)
  root = rand_vertex(graph)
  return graph, root


def connect_graph(graph: list[list[int]], directed: bool) -> None:
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


def weight_graph(unweighted_graph: list[list[int]], lo: int, hi: int
                 ) -> list[list[tuple[int, float]]]:
  weighted_graph: list[list[tuple[int, float]]] = []
  for unweighted_neighbor_list in unweighted_graph:
      weighted_neighbor_list = [(neighbor, random.uniform(lo, hi)) 
                                  for neighbor in unweighted_neighbor_list]
      weighted_graph.append(weighted_neighbor_list)
  return weighted_graph
      

