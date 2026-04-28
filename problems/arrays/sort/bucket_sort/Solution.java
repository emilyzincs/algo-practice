package problems.arrays.sort.bucket_sort;

import java.util.Arrays;

// Algorithm: Bucket Sort.
// Returns the sorted version of the input array.
public class Solution {
  public double[] solve(double[] nums) {
    int n = nums.length;
    if (n <= 1) {
      return nums;
    }

    double minVal = Double.MAX_VALUE;
    double maxVal = Double.MIN_VALUE;
    for (double x : nums) {
      if (x < minVal) {
        minVal = x;
      }
      if (x > maxVal) {
        maxVal = x;
      }
    }

    double diff = maxVal - minVal;
    if (diff == 0) {
      return nums;
    }

    double[][] buckets = new double[n][];
    int[] bucketCounts = new int[n];

    for (double num : nums) {
      int idx = (int) ((num - minVal) / diff * (n - 1));
      if (bucketCounts[idx] == 0) {
        buckets[idx] = new double[n];
      }
      buckets[idx][bucketCounts[idx]++] = num;
    }

    double[] sortedList = new double[n];
    int index = 0;
    for (int i = 0; i < n; i++) {
      if (bucketCounts[i] > 0) {
        Arrays.sort(buckets[i], 0, bucketCounts[i]);
        System.arraycopy(buckets[i], 0, sortedList, index, bucketCounts[i]);
        index += bucketCounts[i];
      }
    }

    return sortedList;
  }
}