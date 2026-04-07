import sys
import os
import argparse
import unittest
from util.file_paths import get_abstract_test_dir, PROJECT_ROOT
from commands.practice.java import path_to_package

TEST_PREFIX = "test_"

def run_all_tests() -> None:
  loader = unittest.TestLoader()
  suite = loader.discover(start_dir="tests", pattern="test_*.py")
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(suite)
  if not result.wasSuccessful():
    sys.exit(1)

def run_specific_test(test_name: str) -> None:
  test_dir = get_abstract_test_dir()
  test_path = os.path.join(test_dir, TEST_PREFIX + test_name)
  if not os.path.exists(test_path + ".py"):
    raise ValueError(f"Not a valid test: {test_name}. Path {test_path} does not exist.")
  full_test_name = path_to_package(test_path, PROJECT_ROOT)
  loader = unittest.TestLoader()
  suite = loader.loadTestsFromName(full_test_name)
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(suite)
  if not result.wasSuccessful():
    sys.exit(1)
  

def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument("--lang", help="Language (e.g., python, java).")
  parser.add_argument("--test", help="Specific test name")
  parser.add_argument("--num", help="Test number, if applicable.")
  parser.add_argument("--alg", help="Algorithm, if applicable")
  parser.add_argument("--debug", help="Whether to output test logs and stacktraces.")

  args = parser.parse_args()
  if args.lang:
    os.environ["TEST_LANGUAGE"] = args.lang
  if args.num:
    os.environ["TEST_NUM"] = args.num
  if args.alg:
    os.environ["TEST_ALG"] = args.alg
  if args.debug:
    os.environ["TEST_DEBUG"] = args.debug
  if not args.test:
    run_all_tests()
  else:
    run_specific_test(args.test)

if __name__ == "__main__":
  main()