import importlib
import sys
from typing import List

def print_desc(descs: List[str]) -> None:
  for i, desc in enumerate(descs):
    print(f"{i+1}. {desc}.")
  print()

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
