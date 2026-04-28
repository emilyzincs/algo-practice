#include <vector>
#include <queue>
#include <stdexcept>

using std::vector;
using std::priority_queue;
using std::pair;

// Algorithm: Prim.
// Returns the minimum cost of a spanning forest for the given
// undirected weighted graph.
class Solution {
 public:
  int solve(vector<vector<vector<int>>>& graph) {
    int num_vertices = graph.size();
    if (num_vertices == 0) {
      return 0;
    }

    int total_mst_weight = 0;

    vector<bool> processed(num_vertices, false);
    for (int vertex = 0; vertex < num_vertices; vertex++) {
      total_mst_weight += prim(graph, vertex, processed);
    }

    for (bool p : processed) {
      if (!p) {
        throw std::runtime_error("Did not process all vertices!");
      }
    }

    return total_mst_weight;
  }

 private:
  int prim(const vector<vector<vector<int>>>& graph, int vertex,
           vector<bool>& processed) {
    if (processed[vertex]) {
      return 0;
    }

    long long component_mst_weight = 0;  // Use long long to prevent overflow
    std::priority_queue<std::pair<int, int>, vector<std::pair<int, int>>,
                         std::greater<std::pair<int, int>>> pq;
    pq.emplace(0, vertex);
    while (!pq.empty()) {
      int weight = pq.top().first;
      int curr_vertex = pq.top().second;
      pq.pop();
      if (processed[curr_vertex]) {
        continue;
      }

      for (const auto& neighbor : graph[curr_vertex]) {
        if (curr_vertex != neighbor[0] && !processed[neighbor[0]]) {
          pq.emplace(neighbor[1], neighbor[0]);
        }
      }
      processed[curr_vertex] = true;
      component_mst_weight += weight;
    }
    return static_cast<int>(component_mst_weight);
  }
};