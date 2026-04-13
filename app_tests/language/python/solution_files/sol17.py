class Solution:
  def solve(self, input: set[tuple[str, ...]]) -> set[str]:
    ret: list[str] = []
    for tup in input:
      ret.extend(tup)
    return set(ret)