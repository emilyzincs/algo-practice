import sys
import os
import argparse
import unittest
from util.file_paths import get_abstract_test_dir, PROJECT_ROOT
from user_testing.test_commands.java import path_to_package

TEST_PREFIX = "test_"

# Parses command‑line arguments to set environment variables and decide whether to run all tests
# or a specific test. Arguments: --lang, --test, --num, --alg, --debug.
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


# Discovers and runs all test files starting with 'TEST_PREFIX' inside the "app_tests" directory.
# Exits with code 1 if any test fails.
def run_all_tests() -> None:
  loader = unittest.TestLoader()
  suite = loader.discover(start_dir="app_tests", pattern=f"{TEST_PREFIX}*.py")
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(suite)
  if not result.wasSuccessful():
    sys.exit(1)


# Runs a single test specified by test_name (without the "test_" prefix or .py extension).
# Raises ValueError if the test file does not exist. Exits with code 1 if the test fails.
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


if __name__ == "__main__":
  main()