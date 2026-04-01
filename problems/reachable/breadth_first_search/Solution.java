package problems.reachable.breadth_first_search;

import java.util.List;
import java.util.Queue;
import java.util.Set;
import java.util.HashSet;
import java.util.LinkedList;

public class Solution {
  public static Set<Integer> solve(List<List<Integer>> graph, int root) {
    int n = graph.size();
    Queue<Integer> q = new LinkedList<Integer>();
    boolean[] seen = new boolean[n];
    Set<Integer> reachable = new HashSet<Integer>();
    if (root < 0 || root >= n) throw new IllegalArgumentException();
    q.add(root);
    seen[root] = true;
    while (!q.isEmpty()) {
      int curr = q.poll();
      reachable.add(curr);
      for (int neighbor : graph.get(curr)) {
        if (!seen[neighbor]) {
          q.add(neighbor);
          seen[neighbor] = true;
        }
      }
    }
    return reachable;
  }  
}
