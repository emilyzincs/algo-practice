class Solution:
  def solve(self, nums: list[int]) -> list[int]:
    self.quick_sort(nums, 0, len(nums)-1)
    return nums

  def quick_sort(self, nums: list[int], lo: int, hi: int) -> None:
    if lo >= hi:
      return
    lt, gt = self.partition(nums, lo, hi)
    self.quick_sort(nums, lo, lt - 1)
    self.quick_sort(nums, gt + 1, hi)

  def partition(self, nums: list[int], lo: int, hi: int) -> tuple[int, int]:
    pivot_idx = self.median_of_three(nums, lo, hi)
    pivot = nums[pivot_idx]
    nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]

    lt = lo
    i = lo
    gt = hi

    while i <= gt:
      if nums[i] < pivot:
        nums[lt], nums[i] = nums[i], nums[lt]
        lt += 1
        i += 1
      elif nums[i] > pivot:
        nums[gt], nums[i] = nums[i], nums[gt]
        gt -= 1
      else:
        i += 1
    return lt, gt
  
  def median_of_three(self, nums: list[int], lo: int, hi: int) -> int:
    mid = (lo + hi) // 2
    a, b, c = nums[lo], nums[mid], nums[hi]
    if (b - a) * (c - b) >= 0:
      return mid
    elif (a - b) * (c - a) >= 0:
      return lo
    else:
      return hi
