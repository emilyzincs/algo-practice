#include <vector>
#include <algorithm>

using std::vector;

// Algorithm: Kadane.
// Returns the maximum subarray sum of the given array.
// (The empty subarray is valid and has sum zero).
class Solution {
 public:
  int solve(vector<int>& nums) {
    long long max_current = 0;
    long long max_global = 0;

    for (int num : nums) {
      max_current = std::max((long long)num, max_current + num);
      max_global = std::max(max_global, max_current);
    }

    return (int)max_global;
  }
};