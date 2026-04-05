import random

def get_null():
  return None

def get_empty_list():
  return []

def rand_array(n: int, lo: int, hi: int) -> list[int]:
  return [random.randint(lo, hi) for _ in range(n)]

def rand_choice(arr):
  return random.choice(arr)

def rand_bool(p=0.5):
  return random.random() < p

def pick_target(arr) -> int:
  if len(arr) == 0:
    return 0
  if rand_bool():
    return rand_choice(arr)  # present
  else:
    return random.randint(min(arr)-1, max(arr)+1)  # maybe absent

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

def trim_tree(arr):
  while arr and arr[-1] is None:
    arr.pop()
  return arr

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

def rand_vertex(graph: list[list[int]]) -> int:
  n = len(graph)
  if n == 0:
    raise ValueError("Cannot pick random vertex since graph has no vertices")
  return random.randint(0, n-1)

def connect_graph(graph: list[list[int]]) -> None:
  n = len(graph)
  if n == 0:
    return
  for i in range(1, n):
    if i not in graph[i-1]:
      graph[i-1].append(i)
  if 0 not in graph[n-1]:
    graph[n-1].append(0)

def make_test(inputs, expected):
  return {
      "inputs": inputs,
      "expected": expected
  }

def make_tests(cases, oracle):
  tests = []
  for inputs in cases:
    expected = oracle(*inputs)
    tests.append(make_test(inputs, expected))
  return tests
