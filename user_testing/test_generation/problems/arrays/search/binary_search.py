import user_testing.test_generation.util.array_util as util
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import SpecificAlgorithm
from typing import override


# Generator for binary search algorithm tests.
class BinarySearchGenerator(BaseGenerator):

  # Builds the complete list of test cases for binary search.
  #
  # Returns:
  #   A list of (array, target) tuples covering edge cases, random inputs,
  #   boundary conditions, and large arrays.
  @override
  def get_all_test_cases(self) -> list[tuple[tuple[int, ...], int]]:
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

    arr = tuple(sorted(util.rand_int_array(255, -1000, 1000)))
    self.add_boundary_cases(test_cases, arr)

    arr = tuple(sorted(util.rand_int_array(256, -1000, 1000)))
    self.add_boundary_cases(test_cases, arr)

    arr = tuple(sorted(util.rand_int_array(257, -1000, 1000)))
    self.add_boundary_cases(test_cases, arr)

    for _ in range(4):
      big_arr = tuple(sorted(list((util.rand_int_big_arry()))))
      target = util.pick_target(big_arr)
      test_cases.append((big_arr, target))

    arr = tuple(sorted(list((util.rand_int_big_arry()))))
    self.add_boundary_cases(test_cases, arr)

    test_cases.append((util.all_same_big_arr(value=0), 0))
    test_cases.append((util.all_same_big_arr(value=-100), -99))

    test_cases = self.remove_duplicate_cases(test_cases)
    return test_cases

  # Returns the list of indices where target appears in arr, or [-1] if not found.
  #
  # Parameters:
  # - arr: List of integers to search.
  # - target: Integer to find.
  #
  # Returns:
  #   List of indices (sorted) or [-1].
  @override
  def oracle(self, arr: tuple[int, ...], target: int) -> list[int]:
    inds = [i for i, num in enumerate(arr) if num == target]
    if not inds:
      inds.append(-1)
    return inds
  
  @override
  def get_algorithm(self) -> SpecificAlgorithm:
    return SpecificAlgorithm.BINARY_SEARCH

  # Returns a list of edge case test inputs for binary search.
  #
  # Returns:
  #   List of (array, target) tuples covering empty array, single element,
  #   missing values, and boundaries.
  def get_edge_cases(self) -> list[tuple[tuple[int, ...], int]]:
    return [
      ((1,), 0),
      ((1,), 1),
      ((1,), 2),
      ((1,3), 1),
      ((1,3), 3),
      ((1,3), 2),
      ((-1,5), -2),
      ((-1,5), 6),
      (tuple(), -1),
      (tuple(), 5)
    ]

  # Generates a random sorted array and a target that may or may not be present.
  #
  # Parameters:
  # - n: Length of the array.
  # - lo: Minimum value for array elements.
  # - hi: Maximum value for array elements.
  #
  # Returns:
  #   A tuple (sorted list, target).
  def get_random_case(self, n: int, lo: int, 
                      hi: int) -> tuple[tuple[int, ...], int]:
    arr = tuple(sorted(util.rand_int_array(n, lo, hi)))
    target = util.pick_target(arr)
    return tuple(arr), target

  # Appends a specified number of random test cases to the given list.
  #
  # Parameters:
  # - test_cases: List to extend.
  # - n: Length of each random array.
  # - lo: Minimum value for array elements.
  # - hi: Maximum value for array elements.
  # - num_cases: Number of test cases to add.
  def add_random_cases(self, test_cases, n: int, lo: int, hi: int, num_cases: int) -> None:
    for _ in range(num_cases):
      test_cases.append(self.get_random_case(n, lo, hi))

  # Adds boundary test cases for a given sorted array (min, min-1, max, max+1).
  #
  # Parameters:
  # - test_cases: List to extend.
  # - arr: Sorted list of integers.
  def add_boundary_cases(self, test_cases, arr) -> None:
    arr = tuple(arr)
    target = min(arr)
    test_cases.append((arr, target))

    target = min(arr) - 1
    test_cases.append((arr, target))

    target = max(arr)
    test_cases.append((arr, target))

    target = max(arr) + 1
    test_cases.append((arr, target)) 

  def remove_duplicate_cases(self, test_cases: list[tuple[tuple[int, ...], int]]
                             ) -> list[tuple[tuple[int, ...], int]]:
    test_cases = list(set(test_cases))
    test_cases.sort(key=lambda x: len(x[0]))
    return test_cases
