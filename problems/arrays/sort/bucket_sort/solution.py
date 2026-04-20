class Solution:
  def solve(self, nums: list[float]) -> list[float]:
    n = len(nums)
    if n <= 1:
      return nums

    min_val = max_val = nums[0]
    for x in nums[1:]:
      if x < min_val: min_val = x
      if x > max_val: max_val = x

    diff = max_val - min_val
    if diff == 0:
      return nums

    buckets: list[list[float]] = [[] for _ in range(n)]
    
    for num in nums:
      idx = int((num - min_val) / diff * (n - 1))
      buckets[idx].append(num)

    sorted_list = []
    for bucket in buckets:
      if bucket:
        sorted_list.extend(sorted(bucket))
        
    return sorted_list
