package problems.graphs.reachable.depth_first_search;

import java.util.List;
import java.util.Set;
import java.util.HashSet;

public class Solution {
  public static Set<Integer> solve(List<List<Integer>> graph, int root) {
    int n = graph.size();
    Set<Integer> reachable = new HashSet<Integer>();
    boolean[] seen = new boolean[n];
    dfs(graph, root, reachable, seen);
    return reachable;
  }
  
  private static void dfs(List<List<Integer>> graph, int root, Set<Integer> reachable, boolean[] seen) {
    int n = graph.size();
    if (root < 0 || n <= root) throw new IllegalArgumentException("Invalid root vertex: " + root);
    reachable.add(root);
    for (int neighbor : graph.get(root)) {
      if (!seen[neighbor]) {
        seen[neighbor] = true;
        dfs(graph, neighbor, reachable, seen);
      }
    }
  }
}
