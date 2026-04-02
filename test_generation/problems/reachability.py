import sys
if len(sys.argv) < 2:
  raise ValueError("Must include project root as first CLI")
PROJECT_ROOT = sys.argv[1].strip()
print("ROOT", PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from problems.reachable.breadth_first_search.solution import Solution

import test_generation.generation_util as util
import get_file_paths as gfp
from utils import read_json, dump_json

sol = Solution()

def oracle(graph, root):
  return list(sol.solve(graph, root))

def get_edge_cases():
  return [
    ([[]], 0),
    ([[0]], 0),
    ([[1], []], 1),
    ([[1], [0]], 1),
    ([[0], [1]], 1),
    ([[0, 1], [0]], 1),
    ([[0, 1], [0, 1]], 1),
    ([[1], [0, 1]], 1),
    ([[0], [0, 1]], 1),
  ]

def get_random_case(n: int, directed: bool, edge_prob: float) -> tuple[list[list[int]], int]: 
  graph = util.rand_graph(n, directed, edge_prob)
  root = util.rand_vertex(graph)
  return graph, root

def add_random_cases(test_cases, n: int, directed: bool, edge_prob: float, num_cases: int) -> None:
  for _ in range(num_cases):
    test_cases.append(get_random_case(n, directed, edge_prob))

def add_random_variety(test_cases, n: int, num_cases: int):
  edge_probs = None
  if n < 20:
    edge_probs = [0, 0.3, 0.5, 0.7, 1]
  elif n < 50:
    edge_probs = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
  else:
    edge_probs = [0, 0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95, 1]
  for directed in [True, False]:
    for edge_prob in edge_probs:
      add_random_cases(test_cases, n, directed, edge_prob, num_cases)
      if edge_prob <= 0.3:
        graph, root = get_random_case(n, directed, edge_prob)
        util.connect_graph(graph)
        test_cases.append((graph, root))

def remove_redundant_test_cases(test_cases):
    print("length before:", len(test_cases))
    hashable_cases = []
    for graph, root in test_cases:
        graph_tuple = tuple(tuple(adj_list) for adj_list in graph)
        hashable_cases.append((graph_tuple, root))
    
    unique_cases = list(set(hashable_cases))
    unique_cases.sort(key=lambda x: len(x[0]))
    
    print("length after:", len(unique_cases))
    return unique_cases

def get_all_test_cases():
  test_cases = get_edge_cases()
  for i in range(3, 8):
    add_random_variety(test_cases, i, 2)
  print(1)
  for i in range(15, 18):
    add_random_variety(test_cases, i, 2)
  print(2)
  for i in range(49, 52):
    add_random_variety(test_cases, i, 3)
  print(3)
  for i in range(99, 102):
    add_random_variety(test_cases, i, 3)
  print(4)
  for i in range(249, 252):
    add_random_variety(test_cases, i, 3)
  print(5)
  # add_random_variety(test_cases, 10**3, 1)
  print(6)
  test_cases = remove_redundant_test_cases(test_cases)
  print(7)
  return test_cases

def main():
  test_cases = get_all_test_cases()
  tests = util.make_tests(test_cases, oracle)
  test_file_path = gfp.get_test_file_path("breadth_first_search")
  json = read_json(test_file_path)
  json["tests"] = tests
  dump_json(test_file_path, json)

if __name__ == "__main__":
  main()
