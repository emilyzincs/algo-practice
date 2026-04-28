#include <vector>

using std::vector;

// Algorithm: Radix Sort.
// Returns the sorted version of the input array.
class Solution {
 public:
  vector<int> solve(vector<int>& nums) {
    if (nums.empty()) {
      return nums;
    }
    
    int min_num = *std::min_element(nums.begin(), nums.end());
    for (auto& num : nums) {
      num -= min_num;
    }

    int max_num = *std::max_element(nums.begin(), nums.end());
    int exp = 1;
    while (max_num / exp > 0) {
      _counting_sort(nums, exp);
      exp *= 10;
    }
      
    for (auto& num : nums) {
      num += min_num;
    }
    return nums;
  }

 private:
  void _counting_sort(vector<int>& nums, int exp) {
    int n = nums.size();
    vector<int> output(n);
    vector<int> count(10, 0);

    for (const auto& num : nums) {
      int digit = (num / exp) % 10;
      count[digit] += 1;
    }

    for (int i = 1; i < 10; i++) {
      count[i] += count[i - 1];
    }

    for (int i = n - 1; i >= 0; i--) {
      int digit = (nums[i] / exp) % 10;
      output[count[digit] - 1] = nums[i];
      count[digit] -= 1;
    }

    for (int i = 0; i < n; i++) {
      nums[i] = output[i];
    }
  }
};