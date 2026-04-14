class Solution:
  def solve(self, nums: list[int]) -> list[int]:
    self.quick_sort(nums, 0, len(nums)-1)
    return nums

  def quick_sort(self, nums: list[int], lo: int, hi: int) -> None:
    if lo >= hi:
      return
    pivot_idx = self.partition(nums, lo, hi)
    self.quick_sort(nums, lo, pivot_idx - 1)
    self.quick_sort(nums, pivot_idx + 1, hi)

  def partition(self, nums: list[int], lo: int, hi: int) -> int:
    pivot_idx = self.median_of_three(nums, lo, hi)
    pivot = nums[pivot_idx]
    nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]

    i = lo - 1
    for j in range(lo, hi):
      if nums[j] <= pivot:
        i += 1
        nums[i], nums[j] = nums[j], nums[i]
    i += 1
    nums[i], nums[hi] = nums[hi], nums[i]
    return i
  
  def median_of_three(self, nums: list[int], lo: int, hi: int) -> int:
    mid = (lo + hi) // 2
    a, b, c = nums[lo], nums[mid], nums[hi]
    if (a - b) * (c - a) >= 0:
      return lo
    elif (b - a) * (c - b) >= 0:
      return mid
    else:
      return hi
