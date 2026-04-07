import os, sys, subprocess
from util.file_paths import PROJECT_ROOT
from pathlib import Path

def get_test_cmd(
    practice_file_dir: str,
    practice_file: str,
    test_runner_dir: str,
    test_runner_file: str,
    info_file: str,
    test_file: str,
    debug: str
) -> list[str]|None:
  try:
    compile_if_necessary(practice_file, practice_file_dir)
  except RuntimeError as e:
    print(f"User code compilation failed:\n{e}", file=sys.stderr)
    return None
  additional_dependencies = [practice_file_dir]
  try:
    compile_if_necessary(test_runner_file, test_runner_dir, additional_dependencies) 
  except RuntimeError as e:
    print(f"Failed to compile java test runner:\n")
    raise e
  runtime_cp_entries =[
    PROJECT_ROOT,
    practice_file_dir,
    test_runner_dir,
  ]
  add_jars(runtime_cp_entries, test_runner_dir)
  additional_args = [path_to_package(practice_file_dir, PROJECT_ROOT), info_file, test_file, debug]
  class_path = os.path.join(test_runner_dir, "Runner")
  class_path_for_cmd = path_to_package(class_path, PROJECT_ROOT)
  return ["java", "-cp", os.pathsep.join(runtime_cp_entries), 
          class_path_for_cmd] + additional_args

def file_to_class_path(file: str) -> str:
  if not file.endswith(".java"):
    raise ValueError("file path must end in .java! given:", file)
  return file[:-len(".java")] + ".class"

def compile_if_necessary(java_file: str, cwd: str, 
                         additional_dependencies: list[str] = []) -> None:
  if not os.path.exists(java_file):
    raise ValueError(f"Could not find {java_file}")

  class_path = file_to_class_path(java_file)
  if os.path.exists(class_path) and os.path.getmtime(java_file) > os.path.getmtime(class_path):
    os.remove(class_path)
  if not os.path.exists(class_path): 
    cp_entries = [cwd]
    add_jars(cp_entries, cwd)
    for d in additional_dependencies:
      cp_entries.append(d)
    cp = os.pathsep.join(cp_entries)
    compile_cmd = ["javac", "-cp", cp, java_file]
    result = subprocess.run(compile_cmd, cwd=cwd, capture_output=True, text=True) 
    if result.returncode == 0 and not os.path.exists(class_path):
      raise RuntimeError(f"Failed to compile into file {class_path}." +
                         " ensure the .java file contains a public class with the same name as the file")
    if result.returncode != 0:
      raise RuntimeError(f"Compilation failed:\n{result.stderr}")
  
def add_jars(cp_entries: list[str], dir: str) -> None:
  lib_dir = os.path.join(dir, "jarlib")
  if os.path.exists(lib_dir):
    for f in Path(lib_dir).iterdir(): 
      if f.name.endswith(".jar"):
        cp_entries.append(os.path.join(lib_dir, f.name))

def path_to_package(path: str, project_root_path: str) -> str:
  path = path.replace(project_root_path, "")
  path = path.replace(os.sep, "", 1)
  path = path.replace(os.sep, ".")
  return path
      