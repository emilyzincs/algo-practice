class Solution:
  def solve(self, nums: list[int]) -> list[int]:
    def merge_sort(nums: list[int], aux: list[int], lo: int, hi: int) -> None:
      if hi - lo <= 1:
        return
      mid = (lo + hi) // 2
      merge_sort(nums, aux, lo, mid)
      merge_sort(nums, aux, mid, hi)

      ptr = lo
      left = lo
      right = mid
      while left < mid and right < hi:
        if nums[left] <= nums[right]:
          aux[ptr] = nums[left]
          left += 1
        else:
          aux[ptr] = nums[right]
          right += 1
        ptr += 1
      while left < mid:
        aux[ptr] = nums[left]
        left += 1
        ptr += 1
      while right < hi:
        aux[ptr] = nums[right]
        right += 1
        ptr += 1
      for i in range(lo, hi):
        nums[i] = aux[i]

    merge_sort(nums, nums.copy(), 0, len(nums))
    return nums
