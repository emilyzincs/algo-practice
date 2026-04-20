import heapq

class Solution:
  def solve(self, nums: list[int]) -> list[int]:
    heapq.heapify(nums)
    return [heapq.heappop(nums) for _ in range(len(nums))]