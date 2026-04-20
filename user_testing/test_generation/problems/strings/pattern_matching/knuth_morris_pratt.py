from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import SpecificAlgorithm
from user_testing.test_generation.util.string_util import get_random_string
import random


class Generator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[str, str]]:
    test_cases: list[tuple[str, str]] = self.get_edge_cases()
    for text_size in [5, 10, 20, 50, 100, 500, 1000, 10000, 100000]:
      for num_allowed_chars in [5, 10, 50, 100, 500, 1000, 10000]:
        self.add_random_cases(test_cases, 5, text_size, num_allowed_chars)
    return test_cases
  
  @override
  def oracle(self, text: str, pattern: str) -> list[int]:
    if not pattern: 
      return []
    indices = []
    idx = text.find(pattern)
    while idx != -1:
      indices.append(idx)
      idx = text.find(pattern, idx + 1)
    return indices

  @override
  def get_algorithm(self) -> SpecificAlgorithm:
    return SpecificAlgorithm.KNUTH_MORRIS_PRATT
  
  def get_edge_cases(self) -> list[tuple[str, str]]:
    return [
      ("", ""),
      ("", "a"),
      ("a", ""),
      ("a", "a"),
      ("a", "b"),
      ("abc", "abc"),
      ("abc", "ab"),
      ("abc", "bc"),
      ("abc", "c"),
      ("abc", "d"),
      ("aaa", "aa"),
      ("aaaaa", "aa"),
      ("ababab", "abab"),
      ("abababa", "aba"),
      ("abcabcabc", "abc"),
      ("mississippi", "issi"),
      ("mississippi", "issip"),
      ("abc", "abcd"),
      ("a" * 1000, "a" * 10),
      ("a" * 1000, "b"),
      ("ab" * 500, "abab"),
      ("a" * 100 + "b", "a" * 50),
      ("abcde", ""),
    ]

  def add_random_cases(self, test_cases: list[tuple[str, str]], 
                       num_cases: int, text_size: int, num_allowed_chars: int):
    for _ in range(num_cases):
      test_cases.append(self.get_random_case(text_size, num_allowed_chars))

  def get_random_case(self, text_size: int, num_allowed_chars: int
                      ) -> tuple[str, str]:
    text = get_random_string(text_size, num_allowed_chars)
    return (text, self.get_pattern_from_text(text))

  def get_pattern_from_text(self, text: str) -> str:
    n = len(text)
    length = random.randint(0, n)
    start = random.randint(0, n - length)
    return text[start:start+length]