from collections import deque

class Solution:
  def solve(
    self,
    graph: list[list[tuple[int, int]]],
    start: int,
    target: int,
    NEG_INF_SENTINEL: int,
    INF_SENTINEL: int
  ) -> int:
    num_vertices = len(graph)
    if num_vertices == 0: return INF_SENTINEL

    # Use a large integer or infinity
    dist = [float('inf')] * num_vertices
    dist[start] = 0

    in_queue = [False] * num_vertices
    relaxation_count = [0] * num_vertices
    has_negative_cycle_to_target = False

    queue: deque[int] = deque([start])
    in_queue[start] = True
    
    while queue:
      u = queue.popleft()
      in_queue[u] = False

      for v, weight in graph[u]:
        if dist[u] != float('inf') and dist[u] + weight < dist[v]:
          dist[v] = dist[u] + weight
          
          if not in_queue[v]:
            relaxation_count[v] += 1
            
            # Negative cycle detected
            if relaxation_count[v] >= num_vertices:
              # Check if this cycle can actually reach the target
              if self._reaches_target(graph, v, target):
                return NEG_INF_SENTINEL
              else:
                # If it doesn't reach target, we continue but stop 
                # exploring this specific path to avoid infinite loops
                continue 

            # Small SPFA optimization (SLF - Small Label First)
            if queue and dist[v] < dist[queue[0]]:
              queue.appendleft(v)
            else:
              queue.append(v)
            in_queue[v] = True

    return self._finalize_distance(dist, target, INF_SENTINEL)

  def _reaches_target(self, graph: list[list[tuple[int, int]]], start_node: int, target: int) -> bool:
    """Standard BFS to see if target is reachable from the cycle node."""
    q = deque([start_node])
    visited = {start_node}
    while q:
      u = q.popleft()
      if u == target: return True
      for v, _ in graph[u]:
        if v not in visited:
          visited.add(v)
          q.append(v)
    return False

  def _finalize_distance(self, distance: list[float], target: int, INF_SENTINEL: int) -> int:
    d = distance[target]
    if d == float('inf'):
      return INF_SENTINEL
    # Cast to int for the final return
    return int(d)