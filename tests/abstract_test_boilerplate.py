import unittest
from unittest.mock import patch
import os
from util.utils import read_json
from util.boilerplate import get_boilerplate_text
from util.get_file_paths import PROJECT_ROOT, to_language_file_case
from typing import Optional
from app import settings, LANGUAGE_LIST


UNIT_TESTS = {"run_tests", "solution"}

class AbstractTestBoilerplate(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.gfp_base = "util.boilerplate."
    self.debug = True

  def abstract_test_boilerplate(
      self,
      language: str,
      boilerplate_file_dir: str,
      boilerplate_file_name_prefix: str,
      required_class_name_prefix: Optional[str] = None,
  ):
    print("\n\nRUNNING " + language.upper() + " boilerplate TESTS.")
    
    test_path_prefix = self.get_test_path_prefix()
    info_path_prefix = self.get_info_path_prefix()
    boilerplate_file_prefix = os.path.join(boilerplate_file_dir, boilerplate_file_name_prefix)
    i = 1
    with patch(self.gfp_base + "get_practice_file_dir", return_value=boilerplate_file_dir):
      while True:
        test_path = test_path_prefix + f"{i}.json"
        info_path = info_path_prefix + f"{i}.json"
        boilerplate_file_path = boilerplate_file_prefix + f"{i}.txt"
        if not (os.path.exists(test_path) == 
                os.path.exists(info_path) == os.path.exists(boilerplate_file_path)):
          raise RuntimeError("Test file must exist iff info file exists iff boilerplate file exists." +
                            " Violated for paths:\n" +
                            f"test_path: {test_path},\n" +
                            f"info_path: {info_path},\n" +
                            f"boilerplate_file_path: {boilerplate_file_path}")
        if not os.path.exists(test_path): 
        # or test_number and i != test_number:
          print(f"Done.")
          break
        print(f"\nRunning {language} boilerplate test {i}:")
        
        info = read_json(info_path)
        boilerplate = get_boilerplate_text(
          info["parameter_names"],
          info["input_types"],
          info["expected_type_wrapper"],
          " " * settings["tab_size"],
          "Solution" if not required_class_name_prefix else f"{required_class_name_prefix}{i}",
          "solve",
          language
        )

        with open(boilerplate_file_path, "r", encoding="utf-8") as f:
          expected = f.read()

        error_msg = (f"Test {i} failed.")
        self.assertEqual(expected, boilerplate, error_msg)
        print("Test passed.")      
        i += 1
  

  def test_all(self) -> None:
    # if self.test_specifier != "all":
    #   return
    # self.test_specifier = ""
    for language in LANGUAGE_LIST:
      boilerplate_file_name_prefix = to_language_file_case("bp", language)
      required_class_name_prefix = None
      boilerplate_file_dir = os.path.join(PROJECT_ROOT, "tests", language, "boilerplate_files")
      if language == "java":
        required_class_name_prefix = "Bp"
      self.abstract_test_boilerplate(
        language,
        boilerplate_file_dir,
        boilerplate_file_name_prefix,
        required_class_name_prefix
      )

  def get_test_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "json_files", "test")
  
  def get_info_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "json_files", "info")
