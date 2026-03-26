import json
import importlib.util
import sys

def main():
  if len(sys.argv) != 3:
    print("Must have exactly two command line arguments, was " + str(len(sys.argv) - 1), file=sys.stderr)
    sys.exit(1)
  practice_file_path = sys.argv[1]
  practice_module = load_module_from_path("practice_module", practice_file_path)
  Attempt = practice_module.Attempt
  test_file_path = sys.argv[2]
  if (not run_test(Attempt(), test_file_path)):
    sys.exit(1)

def standardize(output):
  return output

def run_test(solution_instance, test_file_path: str) -> bool:
  with open(test_file_path) as f:
    data = json.load(f)
  
  tests = data['tests']
  for test in tests:
    number = test['number']
    inputs = test['inputs']
    expected = test['expected']
    actual = standardize(solution_instance.solve(**inputs))
    if actual != expected:
      print(f"TEST FAILED: Actual value of {actual} does not match expected value of {expected} for test {number}.", file=sys.stderr)
      return False
  return True

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
  main()