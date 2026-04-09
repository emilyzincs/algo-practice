import user_testing.test_generation.generation_util as util
from user_testing.test_generation.base_generator import BaseGenerator as parent
from util.enums import SpecificAlgorithm


# Returns the list of indices where target appears in arr, or [-1] if not found.
#
# Parameters:
# - arr: List of integers to search.
# - target: Integer to find.
#
# Returns:
#   List of indices (sorted) or [-1].
def oracle(arr, target):
  inds = [i for i, num in enumerate(arr) if num == target]
  if not inds:
    inds.append(-1)
  return inds


# Returns a list of edge case test inputs for binary search.
#
# Returns:
#   List of (array, target) tuples covering empty array, single element,
#   missing values, and boundaries.
def get_edge_cases():
  return [
    ([1], 0),
    ([1], 1),
    ([1], 2),
    ([1,3], 1),
    ([1,3], 3),
    ([1,3], 2),
    ([-1,5], -2),
    ([-1,5], 6),
    ([], -1),
    ([], 5)
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
def get_random_case(n: int, lo: int, hi: int) -> tuple[list[int], int]:
  arr = sorted(util.rand_array(n, lo, hi))
  target = util.pick_target(arr)
  return arr, target


# Appends a specified number of random test cases to the given list.
#
# Parameters:
# - test_cases: List to extend.
# - n: Length of each random array.
# - lo: Minimum value for array elements.
# - hi: Maximum value for array elements.
# - num_cases: Number of test cases to add.
def add_random_cases(test_cases, n: int, lo: int, hi: int, num_cases: int) -> None:
  for _ in range(num_cases):
    test_cases.append(get_random_case(n, lo, hi))


# Adds boundary test cases for a given sorted array (min, min-1, max, max+1).
#
# Parameters:
# - test_cases: List to extend.
# - arr: Sorted list of integers.
def add_boundary_cases(test_cases, arr) -> None:
  target = min(arr)
  test_cases.append((arr, target))

  target = min(arr) - 1
  test_cases.append((arr, target))

  target = max(arr)
  test_cases.append((arr, target))

  target = max(arr) + 1
  test_cases.append((arr, target))


# Creates a large array with duplicates, ranging from -10^4 to 10^4.
#
# Returns:
#   A list of integers (unsorted).
def get_big_arr():
  ret = []
  for i in range(-(10**4), 10**4):
    if util.rand_bool():
      ret.append(i)
      while util.rand_bool(0.2):
        ret.append(i)
  return ret


# Generator for binary search algorithm tests.
class BinarySearchGenerator(parent):

  # Builds the complete list of test cases for binary search.
  #
  # Returns:
  #   A list of (array, target) tuples covering edge cases, random inputs,
  #   boundary conditions, and large arrays.
  def get_all_test_cases(self) -> list[tuple[list[int], int]]:
    test_cases = get_edge_cases()
    add_random_cases(test_cases, 3, -100, 100, 4)
    add_random_cases(test_cases, 4, -100, 100, 4)
    add_random_cases(test_cases, 5, -100, 100, 4)
    add_random_cases(test_cases, 7, -100, 100, 3)
    add_random_cases(test_cases, 8, -100, 100, 3)
    add_random_cases(test_cases, 9, -100, 100, 3)
    add_random_cases(test_cases, 15, -100, 100, 2)
    add_random_cases(test_cases, 16, -100, 100, 2)
    add_random_cases(test_cases, 17, -100, 100, 2)
    add_random_cases(test_cases, 30, -100, 100, 2)
    add_random_cases(test_cases, 31, -100, 100, 2)
    add_random_cases(test_cases, 31, -100, -100, 1) 
    add_random_cases(test_cases, 32, -100, 100, 2)
    add_random_cases(test_cases, 32, -100, -100, 1)
    add_random_cases(test_cases, 33, -100, 100, 2)
    add_random_cases(test_cases, 33, -100, -100, 1)
    add_random_cases(test_cases, 34, -100, 100, 2)
    add_random_cases(test_cases, 250, -10, 10, 2)
    add_random_cases(test_cases, 255, -100, 100, 2)
    add_random_cases(test_cases, 256, -100, 100, 2)
    add_random_cases(test_cases, 257, -100, 100, 2)
    add_random_cases(test_cases, 255, -1000, 1000, 2)
    add_random_cases(test_cases, 256, -1000, 1000, 2)
    add_random_cases(test_cases, 257, -1000, 1000, 2)

    arr = sorted(util.rand_array(255, -1000, 1000))
    add_boundary_cases(test_cases, arr)

    arr = sorted(util.rand_array(256, -1000, 1000))
    add_boundary_cases(test_cases, arr)

    arr = sorted(util.rand_array(257, -1000, 1000))
    add_boundary_cases(test_cases, arr)

    for _ in range(4):
      big_arr = get_big_arr()
      target = util.pick_target(big_arr)
      test_cases.append((big_arr, target))

    arr = get_big_arr()
    add_boundary_cases(test_cases, arr)

    return test_cases


# Generates test files for the binary search algorithm using this generator.
# Calls the parent method to write tests based on the oracle.
def generate():
  BinarySearchGenerator().generate_tests(SpecificAlgorithm.BINARY_SEARCH, oracle)


# Runs test generation when the script is executed directly.
if __name__ == "__main__":
  generate()
