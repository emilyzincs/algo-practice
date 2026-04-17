import user_testing.test_generation.generation_util as util
from user_testing.test_generation.problems.sort import SortGenerator
from util.enums import GeneralAlgorithm
from typing import override


# Generator for sorting algorithm tests.
class BucketSortGenerator(SortGenerator):
  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.BUCKET_SORT
  
  @override
  def get_random_case(self, n: int, lo: int, hi: int
                      ) -> tuple[tuple[int, ...], ...]:
    arr = util.rand_array(n, lo, hi)
    return (tuple(arr),)

  