import sys
from importlib import util as lib_util
from types import ModuleType


# Loads a Python module dynamically from a given file path.
# Registers the module in sys.modules and returns the loaded module.
# Raises ImportError if the spec or loader cannot be obtained.
def load_module_from_path(module_name, file_path) -> ModuleType:
  spec = lib_util.spec_from_file_location(module_name, file_path)
  if spec is None or spec.loader is None:
    raise ImportError(f"Could not load spec for {file_path}")
  module: ModuleType = lib_util.module_from_spec(spec)
  sys.modules[module_name] = module
  spec.loader.exec_module(module)
  return module


# Placeholder function that performs no operation and returns None.
def no_op() -> None:
  pass
