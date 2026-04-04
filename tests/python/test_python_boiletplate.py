import practice_run_tests.abstract_test_run_tests as parent
import os.path
from util.get_file_paths import PROJECT_ROOT

class TestPythonRunTest(parent.AbstractTestBoilerplate):
  def test_python_run_test(self):
    super().abstract_test_run_tests("python", ".py", 
                                    self.get_boilerplate_dir(), "bp")
  
  def get_boilerplate_dir(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "practice_run_tests", "python", "boilerplate_files")