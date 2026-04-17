class Solution:
  def solve(self, nums: list[float]) -> list[float]:
    n = len(nums)

    shift = min(nums)
    if shift < 0:
      nums = [num + shift for num in nums]
    
    buckets: list[list[float]] = [[] for _ in range(n)]
    for num in nums:
      idx = int(num) % n
      buckets[idx].append(num)

    return [num for bucket in buckets for num in sorted(bucket)]

