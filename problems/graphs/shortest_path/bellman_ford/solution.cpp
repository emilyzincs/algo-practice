#include <vector>
#include <deque>
#include <limits>

using std::vector;
using std::deque;

// Algorithm: Bellman Ford.
// Given a weighted digraph, returns the minimum cost of a path
// from the start vertex to the target vertex.
// (The minimum distance from one vertex to another is defined to be
// infinity (represented by the provided sentinel) if there is no path
// between them, and negative infinity (represented by the provided sentinel)
// if a path between them goes through a negative cycle).
class Solution {
 public:
  long solve(vector<vector<vector<int>>>& graph, int start, int target, long NEG_INF_SENTINEL, long INF_SENTINEL) {
    int num_vertices = (int)graph.size();
    if (num_vertices == 0) return INF_SENTINEL;

    const long INF = std::numeric_limits<long>::max();
    vector<long> dist(num_vertices, INF);
    dist[start] = 0;

    vector<bool> in_queue(num_vertices, false);
    vector<int> relaxation_count(num_vertices, 0);

    deque<int> queue;
    queue.push_back(start);
    in_queue[start] = true;

    while (!queue.empty()) {
      int u = queue.front();
      queue.pop_front();
      in_queue[u] = false;

      for (const auto& edge : graph[u]) {
        int v = edge[0];
        int weight = edge[1];

        if (dist[u] != INF && dist[u] + (long)weight < dist[v]) {
          dist[v] = dist[u] + (long)weight;

          if (!in_queue[v]) {
            relaxation_count[v] += 1;

            // Negative cycle detected
            if (relaxation_count[v] >= num_vertices) {
              // Check if this cycle can actually reach the target
              if (reaches_target(graph, v, target)) {
                return NEG_INF_SENTINEL;
              } else {
                // If it doesn't reach target, we continue but stop 
                // exploring this specific path to avoid infinite loops
                continue;
              }
            }

            // Small SPFA optimization (SLF - Small Label First)
            if (!queue.empty() && dist[v] < dist[queue.front()]) {
              queue.push_front(v);
            } else {
              queue.push_back(v);
            }
            in_queue[v] = true;
          }
        }
      }
    }

    if (dist[target] == INF) {
      return INF_SENTINEL;
    }
    return dist[target];
  }

 private:
  bool reaches_target(const vector<vector<vector<int>>>& graph, int start_node, int target) {
    int num_vertices = (int)graph.size();
    deque<int> q;
    q.push_back(start_node);
    vector<bool> visited(num_vertices, false);
    visited[start_node] = true;

    while (!q.empty()) {
      int u = q.front();
      q.pop_front();

      if (u == target) return true;

      for (const auto& edge : graph[u]) {
        int v = edge[0];
        if (!visited[v]) {
          visited[v] = true;
          q.push_back(v);
        }
      }
    }
    return false;
  }
};