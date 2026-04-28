package problems.arrays.sort.radix_sort;

// Algorithm: Radix Sort.
// Returns the sorted version of the input array.
public class Solution {
  public int[] solve(int[] nums) {
    if (nums.length == 0) {
      return nums;
    }
    
    int minNum = findMin(nums);
    nums = subtractMinFromAll(nums, minNum);

    int maxNum = findMax(nums);
    int exp = 1;
    while (maxNum / exp > 0) {
      countingSort(nums, exp);
      exp *= 10;
    }

    nums = addMinToAll(nums, minNum);
    return nums;
  }

  private int findMin(int[] nums) {
    int minNum = nums[0];
    for (int num : nums) {
      if (num < minNum) {
        minNum = num;
      }
    }
    return minNum;
  }

  private int findMax(int[] nums) {
    int maxNum = nums[0];
    for (int num : nums) {
      if (num > maxNum) {
        maxNum = num;
      }
    }
    return maxNum;
  }

  private int[] subtractMinFromAll(int[] nums, int minNum) {
    int[] result = new int[nums.length];
    for (int i = 0; i < nums.length; i++) {
      result[i] = nums[i] - minNum;
    }
    return result;
  }

  private int[] addMinToAll(int[] nums, int minNum) {
    int[] result = new int[nums.length];
    for (int i = 0; i < nums.length; i++) {
      result[i] = nums[i] + minNum;
    }
    return result;
  }

  private void countingSort(int[] nums, int exp) {
    int n = nums.length;
    int[] output = new int[n];
    int[] count = new int[10];

    for (int num : nums) {
      int digit = (num / exp) % 10;
      count[digit]++;
    }

    for (int i = 1; i < 10; i++) {
      count[i] += count[i - 1];
    }

    for (int i = n - 1; i >= 0; i--) {
      int digit = (nums[i] / exp) % 10;
      output[count[digit] - 1] = nums[i];
      count[digit]--;
    }

    for (int i = 0; i < n; i++) {
      nums[i] = output[i];
    }
  }
}