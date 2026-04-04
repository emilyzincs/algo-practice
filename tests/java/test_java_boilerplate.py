import tests.abstract_test_boilerplate as parent
import os.path
from util.get_file_paths import PROJECT_ROOT

class TestPythonRunTest(parent.AbstractTestBoilerplate):
  def test_python_run_test(self):
    super().abstract_test_boilerplate("java", self.get_boilerplate_dir(), "Bp", "Bp")
  
  def get_boilerplate_dir(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "java", "boilerplate_files")