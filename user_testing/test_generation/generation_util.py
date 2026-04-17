import random
from typing import Any, Callable


def get_null() -> None:
  return None


def get_empty_list() -> list[Any]:
  return []


def rand_int_array(size: int, lo: int, hi: int) -> tuple[int, ...]:
  return _rand_array(size, random.randint, lo, hi)


def rand_float_array(size: int, lo: int, hi: int) -> tuple[float, ...]:
  return _rand_array(size, random.uniform, lo, hi)


def _rand_array(size: int, element_creator_func: Callable, *args, **kwargs):
  return tuple([element_creator_func(*args, **kwargs) for _ in range(size)])


def rand_int_big_arry(lo: int = 10**4, hi: int = 10**4) -> tuple[int, ...]:
  return _rand_big_arr(random.randint, lo, hi)

def rand_float_big_arry(lo: int = 10**4, hi: int = 10**4) -> tuple[float, ...]:
  return _rand_big_arr(random.uniform, lo, hi)

def _rand_big_arr(element_creator_func: Callable, *args, **kwargs):
  ret = []
  for _ in range(-(10**4), 10**4):
    if rand_bool():
      element = element_creator_func(*args, **kwargs)
      ret.append(element)
      while rand_bool(0.2):
        ret.append(element)
  return tuple(ret)


def all_same_big_arr(value: int, size: int = 10**4) -> tuple[int, ...]:
  return tuple([value for _ in range(size)])


def rand_choice(arr: tuple[int, ...]):
  return random.choice(arr)


def rand_bool(probability_true: float = 0.5):
  return random.random() < probability_true


# Picks a target value that may or may not be present in the array.
def pick_target(arr: tuple[int, ...]) -> int:
  if len(arr) == 0:
    return 0
  if rand_bool():
    return rand_choice(arr)  # present
  else:
    return random.randint(min(arr)-1, max(arr)+1)  # maybe absent


# Generates a level‑order list for a random binary tree, with some None placeholders.
#
# Parameters:
# - n: Desired length of the list (may include trailing None values).
# - null_prob: Probability that a non‑root node is None (default 0.2).
#
# Returns:
#   A list of length n containing integers or None.
def rand_tree_array(n: int, null_prob: float = 0.2) -> list[int|None]:
  if n == 0:
    return []

  arr: list[int|None] = []
  for i in range(n):
    if i == 0 or not rand_bool(null_prob):
      arr.append(random.randint(-100, 100))
    else:
      arr.append(None)
  return arr


# Removes trailing None values from the given level‑order tree list 'arr'.
def trim_tree(arr: list[int]) -> list[int]:
  while arr and arr[-1] is None:
    arr.pop()
  return arr
