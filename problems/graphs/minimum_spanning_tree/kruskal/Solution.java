package problems.graphs.minimum_spanning_tree.kruskal;

import java.util.*;

public class Solution {
  public int solve(List<List<int[]>> graph) {
    int numVertices = graph.size();
    if (numVertices <= 1) {
      return 0;
    }

    List<int[]> edges = new ArrayList<>();
    for (int vertex = 0; vertex < numVertices; vertex++) {
      for (int[] neighborWeight : graph.get(vertex)) {
        int neighbor = neighborWeight[0];
        int weight = neighborWeight[1];
        if (neighbor < vertex) {
          edges.add(new int[] {weight, vertex, neighbor});
        }
      }
    }

    Collections.sort(edges, Comparator.comparingInt(a -> a[0]));

    int[] parent = new int[numVertices];
    int[] rank = new int[numVertices];
    for (int i = 0; i < numVertices; i++) {
      parent[i] = i;
    }

    return kruskal(numVertices, edges, parent, rank);
  }

  private int kruskal(int numVertices, List<int[]> edges, int[] parent, int[] rank) {
    int totalWeight = 0;
    for (int[] edge : edges) {
      int weight = edge[0];
      int vertex = edge[1];
      int neighbor = edge[2];
      if (union(vertex, neighbor, parent, rank)) {
        totalWeight += weight;
      }
    }
    return totalWeight;
  }

  private int find(int element, int[] parent) {
    if (parent[element] != element) {
      parent[element] = find(parent[element], parent);
    }
    return parent[element];
  }

  private boolean union(int firstMember, int secondMember, int[] parent, int[] rank) {
    int first = find(firstMember, parent);
    int second = find(secondMember, parent);
    if (first == second) {
      return false;
    }
    if (rank[first] < rank[second]) {
      parent[first] = second;
    } else if (rank[first] > rank[second]) {
      parent[second] = first;
    } else {
      parent[second] = first;
      rank[first]++;
    }
    return true;
  }
}