#include <vector>
#include <algorithm>

using std::vector;

// Algorithm: Bucket Sort.
class Solution {
 public:
  static vector<double> solve(vector<double>& nums) {
    int n = nums.size();
    if (n == 0) {
      return nums;
    }
    double min = nums[0], max = nums[0];
    for (int i = 1; i < n; i++) {
      min = std::min(min, nums[i]);
      max = std::max(max, nums[i]);
    }

    vector<vector<double>> buckets(n);
    for (double num : nums) {
      int idx = int((num - min) / (max - min) * (n - 1));
      buckets[idx].push_back(num);
    }

    vector<double> ret;
    for (auto& buck : buckets) {
      std::sort(buck.begin(), buck.end());
      ret.insert(ret.end(), buck.begin(), buck.end());
    }
    return ret;
  }
};
