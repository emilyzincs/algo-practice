class Solution:
  def solve(self, graph: list[list[tuple[int, int]]], source: int, sink: int) -> int:
    if source == sink:
      return 0
    
    n: int = len(graph)
    
    adj: list[list[list[int]]] = [[] for _ in range(n)]
    
    for u in range(n):
      for v, cap in graph[u]:
        forward_idx = len(adj[u])
        backward_idx = len(adj[v])
        
        adj[u].append([v, cap, backward_idx])
        adj[v].append([u, 0, forward_idx])

    def dfs(u: int, flow: int, visited: list[bool]) -> int:
      if u == sink:
        return flow
      
      visited[u] = True
      
      for edge in adj[u]:
        v, cap, rev_idx = edge
        if not visited[v] and cap > 0:
          bottleneck: int = dfs(v, min(flow, cap), visited)
          
          if bottleneck > 0:
            edge[1] -= bottleneck
            adj[v][rev_idx][1] += bottleneck
            return bottleneck
            
      return 0

    max_flow: int = 0
    INF: int = 10**18
    
    while True:
      visited: list[bool] = [False] * n
      path_flow: int = dfs(source, INF, visited)
      if path_flow == 0:
        break
      max_flow += path_flow
      
    return max_flow