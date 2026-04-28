#include <vector>

using std::vector;

// Algorithm: Quick Sort.
// Returns the sorted version of the input array.
class Solution {
 public:
  vector<int> solve(vector<int>& nums) {
    quick_sort(nums, 0, nums.size() - 1);
    return nums;
  }

 private:
  void quick_sort(vector<int>& nums, int lo, int hi) {
    if (lo >= hi) {
      return;
    }
    int lt, gt;
    std::tie(lt, gt) = partition(nums, lo, hi);
    quick_sort(nums, lo, lt - 1);
    quick_sort(nums, gt + 1, hi);
  }

  std::pair<int, int> partition(vector<int>& nums, int lo, int hi) {
    int pivot_idx = median_of_three(nums, lo, hi);
    int pivot = nums[pivot_idx];
    std::swap(nums[pivot_idx], nums[hi]);

    int lt = lo;
    int i = lo;
    int gt = hi;

    while (i <= gt) {
      if (nums[i] < pivot) {
        std::swap(nums[lt], nums[i]);
        lt += 1;
        i += 1;
      } else if (nums[i] > pivot) {
        std::swap(nums[gt], nums[i]);
        gt -= 1;
      } else {
        i += 1;
      }
    }
    return std::make_pair(lt, gt);
  }

  int median_of_three(vector<int>& nums, int lo, int hi) {
    int mid = lo + (hi - lo) / 2;
    int a = nums[lo];
    int b = nums[mid];
    int c = nums[hi];
    if ((b - a) * (c - b) >= 0) {
      return mid;
    } else if ((a - b) * (c - a) >= 0) {
      return lo;
    } else {
      return hi;
    }
  }
};