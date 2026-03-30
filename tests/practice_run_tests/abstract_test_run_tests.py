import unittest
from unittest.mock import patch
import os
from utils import read_json
from commands.practice.practice import run_tests
from get_file_paths import PROJECT_ROOT

class AbstractTestRunTests(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.gfp_base = "commands.practice.practice.gfp."
    self.debug = False

  def abstract_test_run_tests(self, language, extension, 
                              practice_file_dir, practice_file_name_prefix):
    expected_values = [
      True,
      False,
      False,
      True,
      True, # 5
      True,
      True,
      False,
      True,
      False, # 10
      False,
      True,
      True,
      True, # 15
    ]
    json_path_prefix = self.get_json_path_prefix()
    practice_file_prefix = os.path.join(practice_file_dir, practice_file_name_prefix)
    i = 1
    with patch(self.gfp_base + "get_practice_file_dir", return_value=practice_file_dir):
      while True:
        if self.debug:
          print(f"\nRunning test {i}:")
        json_path = json_path_prefix + f"{i}.json"
        practice_file_path = practice_file_prefix + f"{i}{extension}"
        if os.path.exists(json_path) != os.path.exists(practice_file_path):
          raise RuntimeError("Json path must exist iff practice file exists." +
                            " Violated for paths:\n" +
                            f"json_path: {json_path},\n" +
                            f"practice_file_path: {practice_file_path}")
        if not os.path.exists(json_path):
          print(f"Breaking at i={i}.")
          break
        with (
          patch(self.gfp_base + "get_test_file_path", return_value=json_path),
          patch(self.gfp_base + "get_practice_file_path", return_value=practice_file_path)
        ):
          result = run_tests("", language, extension, self.debug)
        expected = expected_values[i-1]
        error_msg = (f"Expected test {i} to succeed but it failed." 
                    if expected
                    else f"Expected test {i} to fail but it succeeded.")
        self.assertEqual(expected, result, error_msg)      
        i += 1

  def get_json_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "practice_run_tests", "json_files", "test")
