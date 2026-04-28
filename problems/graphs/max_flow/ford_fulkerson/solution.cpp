#include <vector>
#include <algorithm>
#include <functional>
#include <climits>

using std::vector;

// Algorithm: Ford Fulkerson.
// Returns the maximum flow on the given network.
class Solution {
 public:
  int solve(vector<vector<vector<int>>>& graph, int s, int t) {
    if (s == t) {
      return 0;
    }

    int n = (int)graph.size();
    vector<vector<vector<int>>> adj(n);

    for (int u = 0; u < n; ++u) {
      for (const auto& edge : graph[u]) {
        int v = edge[0];
        int cap = edge[1];
        
        int forward_idx = (int)adj[u].size();
        int backward_idx = (int)adj[v].size();
        
        adj[u].push_back({v, cap, backward_idx});
        adj[v].push_back({u, 0, forward_idx});
      }
    }

    std::function<int(int, int, vector<bool>&)> dfs = [&](int u, int flow, vector<bool>& visited) -> int {
      if (u == t) {
        return flow;
      }
      
      visited[u] = true;
      
      for (auto& edge : adj[u]) {
        int v = edge[0];
        int& cap = edge[1];
        int rev_idx = edge[2];
        
        if (!visited[v] && cap > 0) {
          int bottleneck = dfs(v, std::min(flow, cap), visited);
          
          if (bottleneck > 0) {
            cap -= bottleneck;
            adj[v][rev_idx][1] += bottleneck;
            return bottleneck;
          }
        }
      }
      
      return 0;
    };

    int max_flow = 0;
    int INF = INT_MAX;
    
    while (true) {
      vector<bool> visited(n, false);
      int path_flow = dfs(s, INF, visited);
      if (path_flow == 0) {
        break;
      }
      max_flow += path_flow;
    }
    
    return max_flow;
  }
};