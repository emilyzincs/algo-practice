class Solution:
  def solve(self, nums: list[int]) -> int:
    max_current = max_global = 0

    for num in nums:
      max_current = max(num, max_current + num)
      max_global = max(max_global, max_current)

    return max_global