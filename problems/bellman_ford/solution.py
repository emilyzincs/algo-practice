from collections import deque
from typing import List, Tuple

class Solution:
  def solve(
    self,
    graph: List[List[Tuple[int, int]]],
    start: int,
    target: int,
    NEG_INF_SENTINAL: int,
    INF_SENTINAL: int
  ) -> int:
    num_vertices = len(graph)

    INF = float('inf')
    distance = [INF] * num_vertices
    distance[start] = 0

    in_queue = [False] * num_vertices
    relaxation_count = [0] * num_vertices

    queue: deque[int] = deque()
    queue.append(start)
    in_queue[start] = True
    relaxation_count[start] = 1

    while queue:
      current = queue.popleft()
      in_queue[current] = False

      for neighbor, weight in graph[current]:
        if distance[current] != INF and distance[current] + weight < distance[neighbor]:
          distance[neighbor] = distance[current] + weight

          if not in_queue[neighbor]:
            relaxation_count[neighbor] += 1
            if relaxation_count[neighbor] >= num_vertices:

              unbounded = self._find_unbounded_vertices(graph, neighbor)
              if unbounded[target]:
                return NEG_INF_SENTINAL
              
              return self._finalize_distance(distance, target, INF_SENTINAL)

            if queue and distance[neighbor] < distance[queue[0]]:
              queue.appendleft(neighbor)
            else:
              queue.append(neighbor)
            in_queue[neighbor] = True

    return self._finalize_distance(distance, target, INF_SENTINAL)

  def _find_unbounded_vertices(self, graph: List[List[Tuple[int, int]]],
                               start_from: int) -> List[bool]:
    num_vertices = len(graph)
    unbounded = [False] * num_vertices
    q = deque([start_from])
    unbounded[start_from] = True
    while q:
      u = q.popleft()
      for v, _ in graph[u]:
        if not unbounded[v]:
          unbounded[v] = True
          q.append(v)
    return unbounded

  def _finalize_distance(self, distance: List[float], target: int, INF_SENTINAL: int) -> int:
    ret = distance[target]
    if ret == float('inf'):
      return INF_SENTINAL
    if type(ret) != int:
      raise RuntimeError(f"Returned value must be an integer. Value: {ret}")
    return int(ret)