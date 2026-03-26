package problems.binary_search;

public class Solution {

  // parameters: nums, target
  // types: int[] @ int
  public static int solve(int[] nums, int target) {
    int lo = 0;
    int hi = nums.length - 1;
    while (lo <= hi) {
      int mid = (hi - lo) + hi / 2;
      if (nums[mid] == target) {
        return mid;
      } else if (nums[mid] < target) {
        lo = mid + 1;
      } else {
        hi = mid - 1;
      }
    }
    return -1;
  }
}
