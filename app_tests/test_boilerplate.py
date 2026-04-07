import os
from typing import Optional, assert_never
from app_tests.base_test import BaseTest as parent
from unittest.mock import patch
from app import settings

from boilerplate.boilerplate import get_boilerplate_text
from util.file_paths import PROJECT_ROOT, to_language_file_case
from util.file_io import read_json
from util.enums import Language, member_to_string
from util.constants import SOLUTION_CLASS_NAME, SOLUTION_FUNCTION_NAME

class TestBoilerplate(parent):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def setUp(self) -> None:
    super().setUp()
    if self.alg is not None:
      raise ValueError("Alg arguments are not applicable to boilerplate tests.")
    self.fp_base = "boilerplate.boilerplate."

  def test_main(self) -> None:
    if self.language is not None:
      self.run_language_tests(self.language)
    else:
      for language in Language:
        self.run_language_tests(language)

  def run_language_tests(self, language: Language):
    boilerplate_file_name_prefix = to_language_file_case("bp", language)
    required_class_name_prefix = None
    boilerplate_file_dir = os.path.join(PROJECT_ROOT, "app_tests", 
                                        member_to_string(language), "boilerplate_files")
    match language:
      case Language.PYTHON:
        pass
      case Language.JAVA:
        required_class_name_prefix = "Bp"
      case _:
        assert_never()
    self.abstract_test_boilerplate(
      language,
      boilerplate_file_dir,
      boilerplate_file_name_prefix,
      required_class_name_prefix
    )

  def specific_test_boilerplate(
      self,
      test_number: int,
      language: Language,
      info_path_prefix: str,
      test_path_prefix: str,
      boilerplate_file_path_prefix: str,
      required_class_name_prefix: Optional[str]
  ) -> bool:
    res = self.get_paths(
      info_path_prefix,
      test_path_prefix,
      boilerplate_file_path_prefix,
      test_number,
      extension=".txt",
    )
    if res is None:
      return False
    info_path, test_path, boilerplate_file_path = res
    print(f"\nRunning {member_to_string(language)} boilerplate test {test_number}:")
    info = read_json(info_path)
    boilerplate = get_boilerplate_text(
      info["parameter_names"],
      info["input_types"],
      info["expected_type_wrapper"],
      " " * settings["tab_size"],
      (
        SOLUTION_CLASS_NAME if not required_class_name_prefix 
        else f"{required_class_name_prefix}{test_number}"
      ),
      SOLUTION_FUNCTION_NAME,
      language
    )
    with open(boilerplate_file_path, "r", encoding="utf-8") as f:
      expected = f.read()
    error_msg = (f"Test {test_number} failed.")
    self.assertEqual(expected, boilerplate, error_msg)
    print("Test passed.")
    return True

  def abstract_test_boilerplate(
      self,
      language: Language,
      boilerplate_file_dir: str,
      boilerplate_file_name_prefix: str,
      required_class_name_prefix: Optional[str] = None,
  ):
    info_path_prefix = self.get_info_path_prefix()
    test_path_prefix = self.get_test_path_prefix()
    boilerplate_file_prefix = os.path.join(boilerplate_file_dir, boilerplate_file_name_prefix)
    with patch(self.fp_base + "get_practice_file_dir", return_value=boilerplate_file_dir):
      if self.num is not None:
        res =self.specific_test_boilerplate(
          self.num,
          language,
          info_path_prefix,
          test_path_prefix,
          boilerplate_file_prefix,
          required_class_name_prefix
        )
        if not res:
          raise RuntimeError(f"Invalid test number: {self.num}.")
      else:
        print("\n\nRUNNING " + member_to_string(language).upper() + " boilerplate TESTS.")
        i = 1
        while True:
          res = self.specific_test_boilerplate(
            i,
            language,
            info_path_prefix,
            test_path_prefix,
            boilerplate_file_prefix,
            required_class_name_prefix
          )
          if not res:
            break
          i += 1
        print("Done.")
  
  def get_paths(
    self,
    info_path_prefix: str, 
    test_path_prefix: str, 
    boilerplate_file_prefix: str, 
    i: int, 
    extension: str,
  ) -> tuple[str, str, str]|None:
    info_path = info_path_prefix + f"{i}.json"
    test_path = test_path_prefix + f"{i}.json"
    boilerplate_file_path = boilerplate_file_prefix + f"{i}{extension}"
    if not (os.path.exists(test_path) == 
            os.path.exists(info_path) == os.path.exists(boilerplate_file_path)):
      raise RuntimeError("Test file must exist iff info file exists iff boilerplate file exists." +
                        " Violated for paths:\n" +
                        f"test_path: {test_path},\n" +
                        f"info_path: {info_path},\n" +
                        f"boilerplate_file_path: {boilerplate_file_path}")
    if not os.path.exists(test_path): 
      return None
    return info_path, test_path, boilerplate_file_path

  def get_test_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "app_tests", "json_files", "test")
  
  def get_info_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "app_tests", "json_files", "info")
