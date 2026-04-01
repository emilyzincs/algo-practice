import sys
if len(sys.argv) < 2:
  raise ValueError("Must include project root as first CLI")
PROJECT_ROOT = sys.argv[1].strip()
print("ROOT", PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import test_generation.generation_util as util
import get_file_paths as gfp
from utils import read_json, dump_json

def oracle(arr, target):
  inds = [i for i, num in enumerate(arr) if num == target]
  if not inds:
    inds.append(-1)
  return inds

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

def get_random_case(n: int, lo: int, hi: int) -> tuple[list[int], int]:
  arr = sorted(util.rand_array(n, lo, hi))
  target = util.pick_target(arr)
  return arr, target

def add_random_cases(test_cases, n: int, lo: int, hi: int, num_cases: int) -> None:
  for _ in range(num_cases):
    test_cases.append(get_random_case(n, lo, hi))

def add_boundary_cases(test_cases, arr) -> None:
  target = min(arr)
  test_cases.append((arr, target))

  target = min(arr) - 1
  test_cases.append((arr, target))

  target = max(arr)
  test_cases.append((arr, target))

  target = max(arr) + 1
  test_cases.append((arr, target))

def get_big_arr():
  ret = []
  for i in range(-(10**4), 10**4):
    if util.rand_bool():
      ret.append(i)
      while util.rand_bool(0.2):
        ret.append(i)
  return ret

def get_all_test_cases():
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

def main():
  test_cases = get_all_test_cases()
  tests = util.make_tests(test_cases, oracle)
  test_file_path = gfp.get_test_file_path("binary_search")
  json = read_json(test_file_path)
  json["tests"] = tests
  dump_json(test_file_path, json)

if __name__ == "__main__":
  main()