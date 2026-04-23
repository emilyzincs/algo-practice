#include <vector>
#include <algorithm>

using std::vector;

// Algorithm: Kruskal.
class Solution {
 public:
  int solve(vector<vector<vector<int>>>& graph) {
    const int n = graph.size();
    vector<vector<int>> edges;
    for (int i = 0; i < n; i++) {
      const auto& neighbors = graph[i];
      for (const auto& tup : neighbors) {
        edges.push_back({tup[1], i, tup[0]});
      }
    }
    std::sort(edges.begin(), edges.end(), [](const auto& a, const auto& b) {
      return a[0] < b[0];
    });

    parent.clear();
    rank.clear();
    for (int i = 0; i < n; i++) {
      parent.push_back(i);
      rank.push_back(0);
    }

    int cost = 0;
    for (const auto& edge : edges) {
      if (join(edge[1], edge[2])) {
        cost += edge[0];
      }
    }
    return cost;
  }

 private:
  vector<int> parent;
  vector<int> rank;
  int find(int elem) {
    while (parent[elem] != elem) {
      parent[elem] = parent[parent[elem]];
      elem = parent[elem];
    }
    return elem;
  }

  bool join(int first_el, int second_el) {
    int first = find(first_el), second = find(second_el);
    if (first == second) return false;

    if (rank[first] < rank[second]) {
      parent[first] = second;
    } else if (rank[first] > rank[second]) {
      parent[second] = first;
    } else {
      parent[first] = second;
      rank[second]++;
    }
    return true;
  }
};
