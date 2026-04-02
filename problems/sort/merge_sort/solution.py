class Solution:
  def solve(self, nums: tuple[int]) -> tuple[int]:
    nums = list(nums)
    aux = nums.copy()
    self.merge_sort(nums, aux, 0, len(nums))
    return tuple(nums)

  def merge_sort(self, nums: list[int], aux: list[int], lo: int, hi: int):
    if hi <= lo + 1:
      return
    mid = (lo + hi) // 2
    self.merge_sort(nums, aux, lo, mid)
    self.merge_sort(nums, aux, mid, hi)
    left = lo
    right = mid
    p = left
    while left < mid and right < hi:
      if nums[left] <= nums[right]:
        aux[p] = nums[left]
        left += 1
      else:
        aux[p] = nums[right]
        right += 1
      p += 1
    while left < mid:
      aux[p] = nums[left]
      left += 1
      p += 1
    while right < hi:
      aux[p] = nums[right]
      right += 1
      p += 1
    for i in range(lo, hi):
      nums[i] = aux[i]
