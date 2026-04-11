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
  def generate_tests(self, alg: SpecificAlgorithm) -> None:
    test_cases = self.get_all_test_cases()
    tests = self.make_tests(test_cases, self.oracle)
    test_file_path = get_test_file_path(alg)
    dump_json(test_file_path, tests)
  
  # Builds a list of tests by applying the oracle to each input case.
  #
  # Parameters:
  # - cases: A list of test case inputs.
  # - oracle: A function that takes the inputs and returns the expected output.
  #
  # Returns:
  #   A list of test dictionaries (as created by make_test).
  def make_tests(self, cases, oracle):
    tests = []
    for inputs in cases:
      expected = oracle(*inputs)
      tests.append(self.make_test(inputs, expected))
    return tests

  # Creates a test dictionary from inputs and expected output.
  #
  # Parameters:
  # - inputs: The test case inputs (any type).
  # - expected: The expected output.
  #
  # Returns:
  #   A dictionary with keys "inputs" and "expected".
  def make_test(self, inputs, expected):
    return {
        "inputs": inputs,
        "expected": expected
    }
  
  # Returns a list of all test case inputs for the algorithm.
  # Must be implemented by subclasses.
  @abstractmethod
  def get_all_test_cases(self):
    pass
  
  # Takes in inputs for a test and returns either
  # the unique solution, if the algorithm always has a unique solution,
  # or a list of all solutions for the test.
  @abstractmethod
  def oracle(self, *args, **kwargs):
    pass
