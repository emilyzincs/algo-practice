package problems.arrays.subarray.kadane;

// Algorithm: Kadane.
// Returns the maximum subarray sum of the given array.
// (The empty subarray is valid and has sum zero).
public class Solution {
  public int solve(int[] nums) {
    int maxCurrent = 0;
    int maxGlobal = 0;

    for (int num : nums) {
      maxCurrent = Math.max(num, maxCurrent + num);
      maxGlobal = Math.max(maxGlobal, maxCurrent);
    }

    return maxGlobal;
  }
}