class Solution:
  def solve(self, nums: list[float]) -> list[float]:
    n = len(nums)
    if n <= 1:
      return nums
    
    min_num = min(nums)
    max_num = max(nums)
    if max_num - min_num == 0:
      return nums
    
    buckets: list[list[float]] = [[] for _ in range(n)]
    for num in nums:
      idx = int((num - min_num) / (max_num - min_num) * (n - 1))
      buckets[idx].append(num)
    
    return [num for bucket in buckets for num in sorted(bucket)]
  