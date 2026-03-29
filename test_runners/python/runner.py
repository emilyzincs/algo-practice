import json
import sys

if len(sys.argv) != 4:
  print("Must have exactly three command line arguments, was "
          + str(len(sys.argv) - 1), file=sys.stderr)
  sys.exit(1)
PROJECT_ROOT = sys.argv[3]
sys.path.insert(0, PROJECT_ROOT) 

from utils import load_module_from_path

def main():
  
  practice_file_path = sys.argv[1]
  practice_module = load_module_from_path("practice_module", practice_file_path)
  Attempt = practice_module.Solution
  test_file_path = sys.argv[2]
  if (not run_test(Attempt(), test_file_path)):
    sys.exit(1)

def standardize(output):
  return output

def run_test(solution_instance, test_file_path: str) -> bool:
  with open(test_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  if (data['answer_amount'] != "single" and data['answer_amount'] != "multiple"):
    raise AttributeError("Invalid answer_amount field in json test file")
  unique_answer = (data['answer_amount'] == "single")
  tests = data['tests']
  for i, test in enumerate(tests):
    inputs = test['inputs']
    expected = test['expected']
    actual = standardize(solution_instance.solve(*inputs))
      
    if (unique_answer and actual != expected) or (not unique_answer and actual not in expected):
      actual_as_string = str(actual)
      optional_part = " Output: " + actual_as_string if len(actual_as_string) <= 100 else ""
      optional_part = actual if len(str(actual)) <= 100 else ""
      print(f"Test {i + 1} failed.{optional_part}", file=sys.stderr)
      return False
  return True

if __name__ == "__main__":
  main()