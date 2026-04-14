class Solution:
  def solve(self, nums: list[int]) -> list[int]:
    self.quick_sort(nums, 0, len(nums)-1)
    return nums

  def quick_sort(self, nums: list[int], lo: int, hi: int) -> None:
    pivot = self.partition(nums, lo, hi)
    self.quick_sort(nums, lo, pivot - 1)
    self.quick_sort(nums, pivot + 1, hi)

  def partition(self, nums: list[int], lo: int, hi: int) -> int:
    pivot = nums[hi]
    i = lo - 1
    for j in range(lo, hi):
      if nums[j] <= pivot:
        i += 1
        nums[i], nums[j] = nums[j], nums[i]
    i += 1
    nums[i], nums[hi] = nums[hi], nums[i]
    return i
