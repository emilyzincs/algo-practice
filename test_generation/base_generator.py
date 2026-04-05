import test_generation.generation_util as util
from util.get_file_paths import get_test_file_path
from util.utils import dump_json

class BaseGenerator:
  @staticmethod
  def generate_tests(alg: str, oracle_func):
    test_cases = BaseGenerator.get_all_test_cases()
    tests = util.make_tests(test_cases, oracle_func)
    test_file_path = get_test_file_path(alg)
    dump_json(test_file_path, tests)
  
  @staticmethod
  def get_all_test_cases():
    raise NotImplementedError("Children must implement this method.")