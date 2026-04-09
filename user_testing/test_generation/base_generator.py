import user_testing.test_generation.generation_util as util
from util.file_paths import get_test_file_path
from util.file_io import dump_json
from util.enums import SpecificAlgorithm
from abc import ABC, abstractmethod


# A class which factors out the logic for generating tests into
#   the appropriate file.
# Meant to be extended by all test generators.
class BaseGenerator(ABC):

  # Generates test cases, runs them through the oracle to get the expected outputs, 
  # and writes the results to the appropriate JSON file, as determined by 'alg'.
  #
  # Parameters:
  # - alg: The SpecificAlgorithm to generate tests for.
  # - oracle_func: A callable that takes test inputs and returns the expected output.
  def generate_tests(self, alg: SpecificAlgorithm, oracle_func) -> None:
    test_cases = self.get_all_test_cases()
    tests = util.make_tests(test_cases, oracle_func)
    test_file_path = get_test_file_path(alg)
    dump_json(test_file_path, tests)
  

  # Returns a list of all test case inputs for the algorithm.
  # Must be implemented by subclasses.
  @abstractmethod
  def get_all_test_cases(self):
    pass
