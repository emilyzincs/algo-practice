package problems.arrays.sort.merge_sort;
import java.util.Arrays;

public class Solution {
  public static int[] solve(int[] nums) {
    int[] aux = Arrays.copyOf(nums, nums.length);
    mergeSort(nums, aux, 0, nums.length);
    return nums;
  }

  private static void mergeSort(int[] nums, int[] aux, int lo, int hi) {
    if (hi <= lo + 1) return;
    int mid = lo + (hi - lo) / 2;
    mergeSort(nums, aux, lo, mid);
    mergeSort(nums, aux, mid, hi);
    int left = lo;
    int right = mid;
    int ptr = lo;
    while (left < mid && right < hi) {
      if (nums[left] <= nums[right]) aux[ptr++] = nums[left++];
      else aux[ptr++] = nums[right++];
    }
    while (left < mid) aux[ptr++] = nums[left++];
    while (right < hi) aux[ptr++] = nums[right++];
    for (int i = lo; i < hi; i++) {
      nums[i] = aux[i];
    }
  }
}
