import user_testing.test_generation.util.array_util as util
from user_testing.test_generation.problems.sort import SortGenerator
from util.enums import GeneralAlgorithm
from typing import override


class BucketSortGenerator(SortGenerator):

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.BUCKET_SORT

  @override
  def get_edge_cases(self) -> list[tuple[tuple[float, ...], ...]]:  # type: ignore
    return [
      (tuple([]),),
      (tuple([0.5]),),
      (tuple([0.0, 0.0]),),
      (tuple([0.1, 0.2]),),
      (tuple([0.2, 0.1]),),
      (tuple([0.0, 0.0, 0.0]),),
      (tuple([1.0, 1.0, 1.0]),),
      (tuple([-0.5, -0.3, -0.1]),),
      (tuple([-0.1, -0.3, -0.5]),),
      (tuple([-0.5, 0.1, -0.2, 0.3]),),
      (tuple([0.1, 0.2, 0.3, 0.4]),),
      (tuple([0.4, 0.3, 0.2, 0.1]),),
      (tuple([0.0001, 0.0002, 0.0003]),),
      (tuple([-1000.0, 0.0, 1000.0]),),
      (tuple([0.5, 0.5, 0.5, 0.5, 0.5]),),
      (tuple([0.0, 1.0, 0.0, 1.0]),),
      (tuple([0.1, 0.2, 0.30000000000000004, 0.4]),),
      (tuple([-0.001]),),
      (tuple([0.9999999999, 1.0]),),
    ]

  @override
  def get_random_case(self, n: int, lo: int, hi: int # type: ignore 
                      ) -> tuple[tuple[float, ...], ...]: 
    arr = util.rand_float_array(n, lo, hi)   
    return (tuple(arr),)
  
  @override
  def rand_big_arr(self) -> tuple[float, ...]: # type: ignore
    return util.rand_float_big_arry()
