#include <vector>

using std::vector;

// Algorithm: Merge Sort.
// Returns the sorted version of the input array.
class Solution {
 public:
  vector<int> solve(vector<int>& nums) {
    vector<int> aux = nums;
    merge_sort(nums, aux, 0, static_cast<int>(nums.size()));
    return nums;
  }

 private:
  void merge_sort(vector<int>& nums, vector<int>& aux, int lo, int hi) {
    if (hi <= lo + 1) {
      return;
    }
    int mid = lo + (hi - lo) / 2;
    merge_sort(nums, aux, lo, mid);
    merge_sort(nums, aux, mid, hi);
    int left = lo;
    int right = mid;
    int p = left;
    while (left < mid && right < hi) {
      if (nums[left] <= nums[right]) {
        aux[p] = nums[left];
        left += 1;
      } else {
        aux[p] = nums[right];
        right += 1;
      }
      p += 1;
    }
    while (left < mid) {
      aux[p] = nums[left];
      left += 1;
      p += 1;
    }
    while (right < hi) {
      aux[p] = nums[right];
      right += 1;
      p += 1;
    }
    for (int i = lo; i < hi; i++) {
      nums[i] = aux[i];
    }
  }
};