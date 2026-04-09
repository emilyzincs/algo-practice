import random


# Returns None.
def get_null():
  return None


# Returns an empty list.
def get_empty_list():
  return []


# Generates a random tuple of integers.
#
# Parameters:
# - n: Number of elements.
# - lo: Minimum value (inclusive).
# - hi: Maximum value (inclusive).
#
# Returns:
#   A tuple of n random integers.
def rand_array(n: int, lo: int, hi: int) -> tuple[int, ...]:
  return tuple([random.randint(lo, hi) for _ in range(n)])


# Returns a random element from 'arr'.
def rand_choice(arr):
  return random.choice(arr)


# Returns True with probability p, False otherwise.
def rand_bool(p=0.5):
  return random.random() < p


# Picks a target value that may or may not be present in the array.
#
# Parameters:
# - arr: A list of integers.
#
# Returns:
#   An integer that is either an element of arr (with 50% probability)
#   or a random integer between min(arr)-1 and max(arr)+1.
def pick_target(arr) -> int:
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
def rand_tree_array(n, null_prob=0.2):
  if n == 0:
    return []

  arr = []
  for i in range(n):
    if i == 0 or not rand_bool(null_prob):
      arr.append(random.randint(-100, 100))
    else:
      arr.append(None)
  return arr


# Removes trailing None values from the given level‑order tree list 'arr'.
def trim_tree(arr):
  while arr and arr[-1] is None:
    arr.pop()
  return arr


# Generates a random graph as an adjacency list.
#
# Parameters:
# - n: Number of vertices.
# - directed: True for directed edges, False for undirected.
# - edge_prob: Probability of an edge existing between two vertices (default 0.2).
#
# Returns:
#   An adjacency list where graph[i] contains the neighbors of vertex i.
def rand_graph(n: int, directed: bool, edge_prob: float = 0.2) -> list[list[int]]:
  graph: list[list[int]] = [[] for _ in range(n)]
  for i in range(n):
    for j in range(i+1, n):
      if rand_bool(edge_prob):
        graph[i].append(j)
        if directed and rand_bool(edge_prob):
          graph[j].append(i)
        elif not directed:
          graph[j].append(i)
  return graph


# Returns a random vertex index from the given 'graph' (adjacency list).
def rand_vertex(graph: list[list[int]]) -> int:
  n = len(graph)
  if n == 0:
    raise ValueError("Cannot pick random vertex since graph has no vertices")
  return random.randint(0, n-1)


# Modifies the given 'graph' to ensure it is connected by 
# adding edges between consecutive vertices.
def connect_graph(graph: list[list[int]]) -> None:
  n = len(graph)
  if n == 0:
    return
  for i in range(1, n):
    if i not in graph[i-1]:
      graph[i-1].append(i)
  if 0 not in graph[n-1]:
    graph[n-1].append(0)


# Creates a test dictionary from inputs and expected output.
#
# Parameters:
# - inputs: The test case inputs (any type).
# - expected: The expected output.
#
# Returns:
#   A dictionary with keys "inputs" and "expected".
def make_test(inputs, expected):
  return {
      "inputs": inputs,
      "expected": expected
  }


# Builds a list of tests by applying the oracle to each input case.
#
# Parameters:
# - cases: A list of test case inputs.
# - oracle: A function that takes the inputs and returns the expected output.
#
# Returns:
#   A list of test dictionaries (as created by make_test).
def make_tests(cases, oracle):
  tests = []
  for inputs in cases:
    expected = oracle(*inputs)
    tests.append(make_test(inputs, expected))
  return tests
