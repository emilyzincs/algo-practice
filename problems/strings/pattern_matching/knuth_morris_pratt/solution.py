class Solution:
  def solve(self, text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m == 0: return []

    def compute_lps(pattern: str) -> list[int]:
      lps = [0] * m
      length = 0 
      i = 1

      while i < m:
        if pattern[i] == pattern[length]:
          length += 1
          lps[i] = length
          i += 1
        else:
          if length != 0:
            length = lps[length - 1]
          else:
            lps[i] = 0
            i += 1
      return lps
    
    lps = compute_lps(pattern)
    indices = []
    i = 0
    j = 0

    while i < n:
      if pattern[j] == text[i]:
        i += 1
        j += 1

      if j == m:
        indices.append(i - j)
        j = lps[j - 1]
      elif i < n and pattern[j] != text[i]:
        if j != 0:
          j = lps[j - 1]
        else:
          i += 1
    return indices
  