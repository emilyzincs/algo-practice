package problems.graphs.shortest_path.floyd_warshall;

import java.util.List;

// Algorithm: Floyd Warshall.
// Given a weighted digraph with n vertices,
// returns an n by n matrix m where m[i][j]
// is the minimum cost of a path from vertex i to vertex j.
// (The minimum distance from one vertex to another is defined to be
// infinity (represented by the provided sentinel) if there is no path
// between them, and negative infinity (represented by the provided sentinel)
// if a path between them goes through a negative cycle).
public class Solution {
  public List<List<Integer>> solve(List<List<int[]>> graph, int NEG_INF_SENTINEL, int INF_SENTINEL) {
    int n = graph.size();
    
    List<List<Integer>> dist = new java.util.ArrayList<>();
    for (int i = 0; i < n; i++) {
      List<Integer> row = new java.util.ArrayList<>();
      for (int j = 0; j < n; j++) {
        row.add(INF_SENTINEL);
      }
      dist.add(row);
    }
    
    for (int i = 0; i < n; i++) {
      dist.get(i).set(i, 0);
      for (int[] neighbor : graph.get(i)) {
        dist.get(i).set(neighbor[0], Math.min(dist.get(i).get(neighbor[0]), neighbor[1]));
      }
    }

    for (int k = 0; k < n; k++) {
      for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
          if (dist.get(i).get(k) != INF_SENTINEL && dist.get(k).get(j) != INF_SENTINEL) {
            int newDist = dist.get(i).get(k) + dist.get(k).get(j);
            if (newDist < dist.get(i).get(j)) {
              dist.get(i).set(j, newDist);
            }
          }
        }
      }
    }

    for (int k = 0; k < n; k++) {
      if (dist.get(k).get(k) < 0) {
        for (int i = 0; i < n; i++) {
          for (int j = 0; j < n; j++) {
            if (dist.get(i).get(k) != INF_SENTINEL && dist.get(k).get(j) != INF_SENTINEL) {
              dist.get(i).set(j, NEG_INF_SENTINEL);
            }
          }
        }
      }
    }

    return dist;
  }
}