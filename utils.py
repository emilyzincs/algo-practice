import sys
import json
from importlib import util as lib_util
from shutil import copyfile as shutil_copy_file
from typing import List

def read_json(path: str):
  try:
    if not path.endswith(".json"):
      raise json.JSONDecodeError
    with open(path, "r", encoding="utf-8") as f:
      return json.load(f), f
  except FileNotFoundError as e:
    print(f"Path must be a (existing) json file. Was {path}.", file=sys.stderr)
    raise e
  except json.JSONDecodeError as e:
    print(f"File is not valid json: {path}.", file=sys.stderr)
    raise e
   
def dump_json(path: str, data) -> None:
  try:
    if not path.endswith(".json"):
      raise FileNotFoundError
    with open(path, "w", encoding="utf-8") as f:
      json.dump(data, path, indent=2)
  except FileNotFoundError as e:
    print(f"Path must be a (existing) json file. Was {path}", file=sys.stderr)
    raise e
  except TypeError as e:
    print(f"File does not contain valid json: {path}.", file=sys.stderr)
    raise e

def copy_file(src: str, dest: str) -> None:
    try:
      shutil_copy_file(src, dest)
    except PermissionError as e:
      print(f"Error: do not have permission to copy {src} to {dest}.", file=sys.stderr)
      raise e
    except FileNotFoundError as e:
      print(f"File does not exist: {src}.", file=sys.stderr)
      raise e

def in_either(str: str, first: set, second: set) -> bool:
  return str in first or str in second

def print_desc(descs: List[str]) -> None:
  for i, desc in enumerate(descs):
    print(f"{i+1}. {desc}.")

def load_module_from_path(module_name, file_path):
    spec = lib_util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load spec for {file_path}")
    module = lib_util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def is_int(str: str) -> bool:
  try:
    int(str)
    return True
  except ValueError:
    return False
