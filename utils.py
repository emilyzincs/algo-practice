import sys
import json
from importlib import util as lib_util
from shutil import copyfile as shutil_copy_file
from typing import List
from io import IOBase
from tempfile import NamedTemporaryFile as TempFile
from os import path as os_path, replace as os_replace

def read_json(path: str):
  try:
    if not path.endswith(".json"):
      raise json.JSONDecodeError
    with open(path, "r", encoding="utf-8") as f:
      return json.load(f)
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
    dir = os_path.dirname(path)
    with TempFile(mode="w", dir=dir, delete=False, encoding="utf-8") as temp:
      json.dump(data, temp, indent=2)
    os_replace(temp.name, path)
  except FileNotFoundError as e:
    print(f"Path must be a (existing) json file. Was {path}", file=sys.stderr)
    raise e
  except TypeError as e:
    print(f"Data cannot be converted to valid json: {data}.", file=sys.stderr)
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

def match_json_keys(to_match_path: str, to_edit_path: str):
  to_match, to_edit = read_json(to_match_path), read_json(to_edit_path)
  for key in to_match.keys():
    if key not in to_edit:
      to_edit[key] = to_match[key]
  if len(to_edit) > len(to_match):
    to_edit = {key: val for key, val in to_edit.items() if key in to_match}
  dump_json(to_edit_path, to_edit)

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

def is_type(str: str, type_constructor) -> bool:
  try:
    type_constructor(str)
    return True
  except ValueError:
    return False

def string_to_bool(str: str) -> bool:
  str = str.strip().lower()
  if str == "true":
    return True
  elif str == "false":
    return False
  else:
    raise ValueError(f"Str must be either 'true' or 'false'. Was {str}")

def no_op() -> None:
  pass