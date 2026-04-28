package problems.arrays.sort.heap_sort;

// Algorithm: Heap Sort.
// Returns the sorted version of the input array.
public class Solution {
  public int[] solve(int[] nums) {
    if (nums == null || nums.length <= 1) {
      return nums;
    }

    int n = nums.length;

    // Build a max heap (rearrange the array)
    // We start from the last non-leaf node and heapify each subtree.
    for (int i = n / 2 - 1; i >= 0; i--) {
      heapify(nums, n, i);
    }

    // One by one extract elements from the heap
    for (int i = n - 1; i > 0; i--) {
      // Move current root (the maximum element) to the end of the array
      int temp = nums[0];
      nums[0] = nums[i];
      nums[i] = temp;

      // Call max heapify on the reduced heap
      heapify(nums, i, 0);
    }

    return nums;
  }

  // To heapify a subtree rooted with node i which is an index in nums[].
  // n is the size of the heap.
  private void heapify(int[] nums, int n, int i) {
    int largest = i; // Initialize largest as root
    int left = 2 * i + 1; // left child index
    int right = 2 * i + 2; // right child index

    // If left child is larger than root
    if (left < n && nums[left] > nums[largest]) {
      largest = left;
    }

    // If right child is larger than the largest so far
    if (right < n && nums[right] > nums[largest]) {
      largest = right;
    }

    // If largest is not root, swap and continue heapifying
    if (largest != i) {
      int swap = nums[i];
      nums[i] = nums[largest];
      nums[largest] = swap;

      // Recursively heapify the affected sub-tree
      heapify(nums, n, largest);
    }
  }
}