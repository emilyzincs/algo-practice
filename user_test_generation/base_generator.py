import user_test_generation.generation_util as util
from util.file_paths import get_test_file_path
from util.file_io import dump_json
from util.enums import SpecificAlgorithm

class BaseGenerator:
  def generate_tests(self, alg: SpecificAlgorithm, oracle_func):
    test_cases = self.get_all_test_cases()
    tests = util.make_tests(test_cases, oracle_func)
    test_file_path = get_test_file_path(alg)
    dump_json(test_file_path, tests)
  
  def get_all_test_cases(self):
    raise NotImplementedError("Children must implement this method.")