#include <vector>

using std::vector;

// Algorithm: Depth First Search.
// Returns the reachable vertices from the given vertex
// in the given digraph, in any order.
class Solution {
 public:
  vector<int> solve(vector<vector<int>>& graph, int root) {
    vector<int> reachable;
    vector<bool> seen(graph.size(), false);
    seen[root] = true;
    dfs(graph, root, reachable, seen);
    return reachable;
  }
  
 private:
  void dfs(const vector<vector<int>>& graph, int root, vector<int>& reachable, vector<bool>& seen) {
    reachable.push_back(root);
    for (int neighbor : graph[root]) {
      if (!seen[neighbor]) {
        seen[neighbor] = true;
        dfs(graph, neighbor, reachable, seen);
      }
    }
  }
};