import json
import os
import sys
from typing import Any
from tempfile import NamedTemporaryFile as TempFile
from shutil import copyfile as shutil_copy_file


# Copies a file from source to destination, handling common errors.
#
# Parameters:
# - src: Path to the source file.
# - dest: Path to the destination file.
#
# Raises:
#   PermissionError if the operation lacks permission.
#   FileNotFoundError if the source file does not exist.
def copy_file(src: str, dest: str) -> None:
  try:
    shutil_copy_file(src, dest)
  except PermissionError as e:
    print(f"Error: do not have permission to copy {src} to {dest}.", file=sys.stderr)
    raise e
  except FileNotFoundError as e:
    print(f"File does not exist: {src}.", file=sys.stderr)
    raise e


# Reads the JSON data in the given path, then returns the parsed data.
#
# Raises:
#   Exception if 'path' does not end in ".json"
#   FileNotFoundError if the file does not exist.
#   json.JSONDecodeError if the file contains invalid JSON.
def read_json(path: str) -> Any:
  try:
    if not path.endswith(".json"):
      raise Exception(f"File name must end json: {path}.")
    with open(path, "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError as e:
    print(f"Path must be a (existing) json file. Was {path}.", file=sys.stderr)
    raise e
  except json.JSONDecodeError as e:
    print(f"File is not valid json: {path}.", file=sys.stderr)
    raise e


# Writes data to a JSON file atomically using a temporary file.
#
# Parameters:
# - path: Path to the target .json file.
# - data: Python object that can be serialized to JSON.
#
# Raises:
#   FileNotFoundError if the directory does not exist 
#                     or 'path' does not end in ".json".
#   TypeError if data cannot be serialized to JSON.
def dump_json(path: str, data) -> None:
  try:
    if not path.endswith(".json"):
      raise FileNotFoundError
    dir = os.path.dirname(path)
    with TempFile(mode="w", dir=dir, delete=False, encoding="utf-8") as temp:
      json.dump(data, temp, indent=2)
    os.replace(temp.name, path)
  except FileNotFoundError as e:
    print(f"Path must be a (existing) json file. Was {path}", file=sys.stderr)
    raise e
  except TypeError as e:
    print(f"Data cannot be converted to valid json: {data}.", file=sys.stderr)
    raise e


# Ensures that the JSON file at to_edit_path contains all keys present in the
#   reference file at to_match_path. Keys present only in to_edit are removed.
# If a key is present in to_match_path but not to_edit_path, it is added to to_edit_path
#   with the same value as in to_match_path.
#
# Parameters:
# - to_match_path: Path to the reference JSON file (dictionary).
# - to_edit_path: Path to the JSON file to be updated in place.
def match_json_keys(to_match_path: str, to_edit_path: str):
  to_match, to_edit = read_json(to_match_path), read_json(to_edit_path)
  for key in to_match.keys():
    if key not in to_edit:
      to_edit[key] = to_match[key]
  if len(to_edit) > len(to_match):
    to_edit = {key: val for key, val in to_edit.items() if key in to_match}
  dump_json(to_edit_path, to_edit)
