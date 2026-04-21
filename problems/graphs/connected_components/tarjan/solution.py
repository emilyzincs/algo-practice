class Solution:
  def solve(self, graph: list[list[int]]) -> list[list[int]]:
    n = len(graph)
    index = 0
    indices = [-1] * n
    lowlink = [0] * n
    on_stack = [False] * n
    stack = []
    sccs: list[list[int]] = []

    def strongconnect(v: int) -> None:
      nonlocal index
      indices[v] = index
      lowlink[v] = index
      index += 1
      stack.append(v)
      on_stack[v] = True

      for w in graph[v]:
        if indices[w] == -1:
          strongconnect(w)
          lowlink[v] = min(lowlink[v], lowlink[w])
        elif on_stack[w]:
          lowlink[v] = min(lowlink[v], indices[w])

      if lowlink[v] == indices[v]:
        scc = []
        while True:
          w = stack.pop()
          on_stack[w] = False
          scc.append(w)
          if w == v:
            break
        sccs.append(scc)

    for v in range(n):
      if indices[v] == -1:
        strongconnect(v)

    return sccs
