#include <vector>

using std::vector;

// Algorithm: Heap Sort.
// Returns the sorted version of the input array.
class Solution {
 public:
  vector<int> solve(vector<int>& nums) {
    buildHeap(nums);
    vector<int> sorted;
    while (!nums.empty()) {
      sorted.push_back(nums[0]);
      nums[0] = nums.back();
      nums.pop_back();
      heapify(nums, 0);
    }
    return sorted;
  }

 private:
  void buildHeap(vector<int>& nums) {
    for (int i = nums.size() / 2 - 1; i >= 0; --i) {
      heapify(nums, i);
    }
  }

  void heapify(vector<int>& nums, int i) {
    int smallest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < nums.size() && nums[left] < nums[smallest]) {
      smallest = left;
    }

    if (right < nums.size() && nums[right] < nums[smallest]) {
      smallest = right;
    }

    if (smallest != i) {
      std::swap(nums[i], nums[smallest]);
      heapify(nums, smallest);
    }
  }
};