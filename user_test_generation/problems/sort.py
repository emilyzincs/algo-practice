import user_test_generation.generation_util as util
from user_test_generation.base_generator import BaseGenerator as parent
from util.enums import SpecificAlgorithm

def oracle(arr):
  return sorted(arr)

def get_edge_cases():
  return [
    (tuple([]),),
    (tuple([1]),),
    (tuple([1,1]),),
    (tuple([-1, -2]),),
    (tuple([-2, -1]),),
    (tuple([-1,5]),),
  ]

def get_random_case(n: int, lo: int, hi: int) -> tuple[tuple[int, ...], ...]:
  arr = util.rand_array(n, lo, hi)
  return (tuple(arr),)

def add_random_cases(test_cases, n: int, lo: int, hi: int, num_cases: int) -> None:
  for _ in range(num_cases):
    test_cases.append(get_random_case(n, lo, hi))

def get_big_arr() -> tuple[int, ...]:
  ret = []
  for i in range(-(10**4), 10**4):
    if util.rand_bool():
      ret.append(i)
      while util.rand_bool(0.2):
        ret.append(i)
  return tuple(ret)

def remove_redundant_cases(test_cases):
  test_cases = list(set(test_cases))
  test_cases.sort(key=lambda x: len(x))
  return test_cases

class SortGenerator(parent):
  def get_all_test_cases(self):
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

    for _ in range(4):
      big_arr = get_big_arr()
      test_cases.append((big_arr,))

    test_cases = remove_redundant_cases(test_cases)
    return test_cases

def generate():
  SortGenerator().generate_tests(SpecificAlgorithm.MERGE_SORT, oracle)

if __name__ == "__main__":
  generate()