import user_testing.test_generation.util.array_util as util
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import SpecificAlgorithm
from typing import override


class Generator(BaseGenerator):

  @override
  def get_all_test_cases(self) -> list[tuple[tuple[int, ...], ...]]:
    test_cases = self.get_edge_cases()
    self.add_random_cases(test_cases, 3, -100, 100, 4)
    self.add_random_cases(test_cases, 4, -100, 100, 4)
    self.add_random_cases(test_cases, 5, -100, 100, 4)
    self.add_random_cases(test_cases, 7, -100, 100, 3)
    self.add_random_cases(test_cases, 8, -100, 100, 3)
    self.add_random_cases(test_cases, 9, -100, 100, 3)
    self.add_random_cases(test_cases, 15, -100, 100, 2)
    self.add_random_cases(test_cases, 16, -100, 100, 2)
    self.add_random_cases(test_cases, 17, -100, 100, 2)
    self.add_random_cases(test_cases, 30, -100, 100, 2)
    self.add_random_cases(test_cases, 31, -100, 100, 2)
    self.add_random_cases(test_cases, 31, -100, -100, 1) 
    self.add_random_cases(test_cases, 32, -100, 100, 2)
    self.add_random_cases(test_cases, 32, -100, -100, 1)
    self.add_random_cases(test_cases, 33, -100, 100, 2)
    self.add_random_cases(test_cases, 33, -100, -100, 1)
    self.add_random_cases(test_cases, 34, -100, 100, 2)
    self.add_random_cases(test_cases, 250, -10, 10, 2)
    self.add_random_cases(test_cases, 255, -100, 100, 2)
    self.add_random_cases(test_cases, 256, -100, 100, 2)
    self.add_random_cases(test_cases, 257, -100, 100, 2)
    self.add_random_cases(test_cases, 255, -1000, 1000, 2)
    self.add_random_cases(test_cases, 256, -1000, 1000, 2)
    self.add_random_cases(test_cases, 257, -1000, 1000, 2)

    for _ in range(4):
      big_arr = self.rand_big_arr()
      test_cases.append((big_arr,))
    
    sorted_big_arr = self.rand_sorted_big_arr()
    test_cases.append((sorted_big_arr,))
    reverse_sorted_big_arr = tuple(list(big_arr)[::-1])
    test_cases.append((reverse_sorted_big_arr,))

    test_cases.append(self.get_all_same_case())

    test_cases = self.remove_duplicate_cases(test_cases)
    return test_cases
  
  # Returns the sorted version of the input array.
  @override
  def oracle(self, arr: list[int]) -> list[int]:
    return sorted(arr)
  
  @override
  def get_algorithm(self) -> SpecificAlgorithm:
    return SpecificAlgorithm.MERGE_SORT  # multiple work here

  # Returns a list of edge-case test inputs for sorting.
  def get_edge_cases(self) -> list[tuple[tuple[int, ...], ...]]:
    return [
      (tuple([]),),
      (tuple([1]),),
      (tuple([1,1]),),
      (tuple([-1, -2]),),
      (tuple([-2, -1]),),
      (tuple([-1,5]),),
    ]

  # Generates a random array and returns it as a single‑element tuple.
  #
  # Parameters:
  # - n: Length of the array.
  # - lo: Minimum value for array elements.
  # - hi: Maximum value for array elements.
  def get_random_case(self, n: int, lo: int, hi: int
                      ) -> tuple[tuple[int, ...], ...]:
    arr = util.rand_int_array(n, lo, hi)
    return (tuple(arr),)

  # Appends a specified number of random test cases to the given list.
  #
  # Parameters:
  # - test_cases: List to extend.
  # - n: Length of each random array.
  # - lo: Minimum value for array elements.
  # - hi: Maximum value for array elements.
  # - num_cases: Number of test cases to add.
  def add_random_cases(self, test_cases, n: int, lo: int, hi: int, 
                       num_cases: int) -> None:
    for _ in range(num_cases):
      test_cases.append(self.get_random_case(n, lo, hi))

  def remove_duplicate_cases(self, test_cases) -> list[tuple[tuple[int, ...], ...]]:
    test_cases = list(set(test_cases))
    test_cases.sort(key=lambda x: len(x[0]))
    return test_cases
  
  def rand_big_arr(self) -> tuple[int, ...]:
    return util.rand_int_big_arry()

  def rand_sorted_big_arr(self) -> tuple[int, ...]:
    return tuple(sorted(list((self.rand_big_arr()))))
  
  def get_all_same_case(self) -> tuple[tuple[int, ...]]:
    return (util.all_same_big_arr(0),)