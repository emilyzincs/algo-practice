import practice_run_tests.abstract_test_run_tests as parent
import os.path
from util.get_file_paths import PROJECT_ROOT

class TestPythonRunTest(parent.AbstractTestRunTests):
  def test_python_run_test(self):
    super().abstract_test_run_tests("java", ".java", self.get_practice_file_dir(), "Sol", "Sol")

  def test_python_solutions(self):
    super().abstract_test_solutions("java", ".java")
         
  def get_practice_file_dir(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "practice_run_tests", "java", "solution_files")