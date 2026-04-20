class Solution:
  def solve(self, nums: list[int]) -> list[int]:
    if not nums:
      return nums
    
    min_num = min(nums)
    nums = [num - min_num for num in nums]

    max_num = max(nums)
    exp = 1
    while max_num // exp > 0:
      self._counting_sort(nums, exp)
      exp *= 10
      
    nums = [num + min_num for num in nums]
    return nums

  def _counting_sort(self, nums: list[int], exp: int) -> None:
    n = len(nums)
    output = [0] * n
    count = [0] * 10

    for num in nums:
      digit = (num // exp) % 10
      count[digit] += 1

    for i in range(1, 10):
      count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
      digit = (nums[i] // exp) % 10
      output[count[digit] - 1] = nums[i]
      count[digit] -= 1

    for i in range(n):
      nums[i] = output[i]