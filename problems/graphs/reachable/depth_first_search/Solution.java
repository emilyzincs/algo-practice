package problems.graphs.reachable.depth_first_search;

import java.util.List;
import java.util.ArrayList;

public class Solution {
  public static List<Integer> solve(List<List<Integer>> graph, int root) {
    int n = graph.size();
    List<Integer> reachable = new ArrayList<Integer>();
    boolean[] seen = new boolean[n];
    seen[root] = true;
    dfs(graph, root, reachable, seen);
    return reachable;
  }
  
  private static void dfs(List<List<Integer>> graph, int root, 
                          List<Integer> reachable, boolean[] seen) {
    reachable.add(root);
    for (int neighbor : graph.get(root)) {
      if (!seen[neighbor]) {
        seen[neighbor] = true;
        dfs(graph, neighbor, reachable, seen);
      }
    }
  }
}
