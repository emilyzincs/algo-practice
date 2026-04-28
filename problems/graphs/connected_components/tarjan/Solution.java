package problems.graphs.connected_components.tarjan;

import java.util.ArrayList;
import java.util.List;

// Algorithm: Tarjan.
// Returns the strongly connected components of the given digraph
// in any order.
public class Solution {
  private int index;
  private int[] indices;
  private int[] lowlink;
  private boolean[] on_stack;
  private List<Integer> stack;
  private List<List<Integer>> sccs;

  public List<List<Integer>> solve(List<List<Integer>> graph) {
    int n = graph.size();
    index = 0;
    indices = new int[n];
    for (int i = 0; i < n; i++) {
      indices[i] = -1;
    }
    lowlink = new int[n];
    on_stack = new boolean[n];
    stack = new ArrayList<>();
    sccs = new ArrayList<>();

    for (int v = 0; v < n; v++) {
      if (indices[v] == -1) {
        strongconnect(v, graph);
      }
    }

    return sccs;
  }

  private void strongconnect(int v, List<List<Integer>> graph) {
    indices[v] = index;
    lowlink[v] = index;
    index += 1;
    stack.add(v);
    on_stack[v] = true;

    for (int w : graph.get(v)) {
      if (indices[w] == -1) {
        strongconnect(w, graph);
        lowlink[v] = Math.min(lowlink[v], lowlink[w]);
      } else if (on_stack[w]) {
        lowlink[v] = Math.min(lowlink[v], indices[w]);
      }
    }

    if (lowlink[v] == indices[v]) {
      List<Integer> scc = new ArrayList<>();
      while (true) {
        int w = stack.remove(stack.size() - 1);
        on_stack[w] = false;
        scc.add(w);
        if (w == v) {
          break;
        }
      }
      sccs.add(scc);
    }
  }
}