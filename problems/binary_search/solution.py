from typing import List

class Solution:
  def solve(self, nums: List[int], target: int) -> int:
    if nums is None:
      raise ValueError()
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
      mid = (lo + hi) // 2
      if nums[mid] == target:
        return mid
      elif nums[mid] < target:
        lo = mid + 1
      else:
        hi = mid - 1
    return -1
 