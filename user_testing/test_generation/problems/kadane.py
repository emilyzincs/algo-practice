import user_testing.test_generation.util.array_util as util
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import GeneralAlgorithm
from typing import override
from problems.Arrays.Subarray.kadane.solution import Solution

sol = Solution()


# Generator for binary search algorithm tests.
class KadaneGenerator(BaseGenerator):

  # Builds the complete list of test cases for binary search.
  #
  # Returns:
  #   A list of (array, target) tuples covering edge cases, random inputs,
  #   boundary conditions, and large arrays.
  @override
  def get_all_test_cases(self) -> list[tuple[tuple[int, ...]]]:
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
      big_arr = tuple(util.rand_int_big_arry())
      test_cases.append((big_arr,))

    test_cases.append((util.all_same_big_arr(value=0),))
    test_cases.append((util.all_same_big_arr(value=-100),))

    test_cases = self.remove_duplicate_cases(test_cases)
    return test_cases

  @override
  def oracle(self, arr: tuple[int, ...]) -> int:
    n = len(arr)
    if n < 1000:
      best = 0
      for i in range(n):
          cur = 0
          for j in range(i, n):
              cur += arr[j]
              best = max(best, cur)
      return best
    else:
      return sol.solve(list(arr))
  
  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.KADANE

  def get_edge_cases(self) -> list[tuple[tuple[int, ...]]]:
    return [
      ((),),
      ((5,),),
      ((-3,),),
      ((0,),),
      ((-1, -2, -3),),
      ((-5,),),
      ((-10, -20, -30, -1),),
      ((1, 2, 3, 4),),
      ((10,),),
      ((5, -1, -2, 3),),
      ((10, -5, -20, 1),),
      ((-2, -3, 4, 5),),
      ((-1, -2, 3),),
      ((-2, 1, -3, 4, -1, 2, 1, -5, 4),),
      ((3, -4, 5, -2, 7, -1),),
      ((0, -1, 2, -1, 0, 3),),
      ((-2, 0, -1),),
      ((1, -2, 3, -4, 5, -6, 7),),
      ((2, -1, 2, -1, 2),),
      ((1000000, -1, 1000000),),
      ((-1000000, -2000000, -3000000),),
      ((1, -2, 3, -1, 2),),
      ((-1, 2, -3, 4, -5, 6),),
      ((2, -3, 4, -1, -2, 1, 5, -3),),
      ((0, 0, 0),),
      ((0, 5, 0, -10, 0, 6, 0),),
      ((0, 0, 0, 0),),
    ]
   

  # Generates a random sorted array.
  #
  # Parameters:
  # - n: Length of the array.
  # - lo: Minimum value for array elements.
  # - hi: Maximum value for array elements.
  #
  # Returns:
  #   A tuple (list).
  def get_random_case(self, n: int, lo: int, 
                      hi: int) -> tuple[tuple[int, ...]]:
    arr = util.rand_int_array(n, lo, hi)
    return (arr,)

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
  
  def remove_duplicate_cases(self, cases: list[tuple[tuple[int, ...]]]
                                  ) -> list[tuple[tuple[int, ...]]]:
    return sorted(list(set(cases)), key=lambda x: len(x[0]))
  
