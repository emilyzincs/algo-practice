package problems.arrays.sort.quick_sort;

// Algorithm: Quick Sort.
// Returns the sorted version of the input array.
public class Solution {
  public int[] solve(int[] nums) {
    quickSort(nums, 0, nums.length - 1);
    return nums;
  }

  private void quickSort(int[] nums, int lo, int hi) {
    if (lo >= hi) {
      return;
    }
    int[] ltGt = partition(nums, lo, hi);
    quickSort(nums, lo, ltGt[0] - 1);
    quickSort(nums, ltGt[1] + 1, hi);
  }

  private int[] partition(int[] nums, int lo, int hi) {
    int pivotIdx = medianOfThree(nums, lo, hi);
    int pivot = nums[pivotIdx];
    swap(nums, pivotIdx, hi);

    int lt = lo;
    int i = lo;
    int gt = hi;

    while (i <= gt) {
      if (nums[i] < pivot) {
        swap(nums, lt, i);
        lt++;
        i++;
      } else if (nums[i] > pivot) {
        swap(nums, gt, i);
        gt--;
      } else {
        i++;
      }
    }
    return new int[]{lt, gt};
  }

  private int medianOfThree(int[] nums, int lo, int hi) {
    int mid = (lo + hi) / 2;
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

  private void swap(int[] nums, int i, int j) {
    int temp = nums[i];
    nums[i] = nums[j];
    nums[j] = temp;
  }
}