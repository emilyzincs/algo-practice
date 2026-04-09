from util.file_paths import get_practice_file_dir, PROJECT_ROOT, get_boilerplate_language_file_path
from user_testing.test_commands.java import path_to_package
from typing import assert_never, Any
from util.enums import Language, ParseType, member_from_string, member_to_string
from util.general import load_module_from_path
from boilerplate.util import validate_type
from boilerplate.interface import BpInterface
from boilerplate.language import java

BP_LANG_CLASS: type[BpInterface]

def get_boilerplate_text(
  parameter_names: list[str],
  input_types,
  expected_type,
  one_indent: str,
  solution_class_name: str,
  solution_function_name: str,
  language: Language
):
  set_bp_lang_class(language)

  parameter_type_strings = [BP_LANG_CLASS.parse_type_string(input_type) for input_type in input_types]
  return_type_string = BP_LANG_CLASS.parse_type_string(expected_type)
  included_types: set[ParseType] = recursively_get_included_types(input_types, expected_type)

  start = BP_LANG_CLASS.get_start()

  class_declaration = BP_LANG_CLASS.get_class_declaration(solution_class_name, one_indent)
  method_declaration = BP_LANG_CLASS.get_method_declaration(
    solution_function_name,
    parameter_names, 
    parameter_type_strings, 
    return_type_string, 
    one_indent
  )

  list_node = ""
  tree_node = ""

  if ParseType.LISTNODE in included_types:
    val_type_string = get_nested_type_string(ParseType.LISTNODE, "val",
                                            input_types, expected_type)
    list_node = BP_LANG_CLASS.list_node(val_type_string, one_indent, one_indent * 1) 

  if ParseType.TREENODE in included_types:
    val_type_string = get_nested_type_string(ParseType.TREENODE, "val",
                                             input_types, expected_type)
    tree_node = BP_LANG_CLASS.tree_node(val_type_string, one_indent, one_indent * 1)

  end = get_ending(one_indent, language)

  ret = "".join([
    start,
    class_declaration, 
    method_declaration, 
    list_node, 
    tree_node, 
    end
  ])

  return ret

def set_bp_lang_class(lang: Language) -> None:
  lang_class_name: str
  path = get_boilerplate_language_file_path(lang)

  # This match logic is not strictly necessary, but it is a useful
  # static flag that a new class needs to be implemented when 
  # a new language is added
  match lang:
    case Language.PYTHON:
      lang_class_name = "PythonBp"
    case Language.JAVA:
      lang_class_name = "JavaBp"
    case _:
      assert_never(lang)
  global BP_LANG_CLASS
  module = load_module_from_path(lang_class_name, path)
  BP_LANG_CLASS = getattr(module, lang_class_name)
  if not issubclass(BP_LANG_CLASS, BpInterface):
    raise TypeError(f"{lang_class_name} must inherit from BpInterface.")

def get_beginning(language: Language) -> str:
  match language:
    case Language.PYTHON:
      return ""
    case Language.JAVA:
      return "package " + path_to_package(get_practice_file_dir(), PROJECT_ROOT) + ";\n\n"
    case _:
      assert_never(language)

def add_nested_included_types(typ: dict[str, Any], s: set[ParseType]) -> None:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])
  s.add(curr_type)
  match curr_type:
    case ParseType.INT | ParseType.LONG | ParseType.FLOAT | ParseType.BOOLEAN | ParseType.STRING:
      pass
    case ParseType.ARRAY | ParseType.LIST | ParseType.IMMUTABLE_LIST | ParseType.SET:
      add_nested_included_types(typ["items"], s)
    case ParseType.MAP:
      add_nested_included_types(typ["keys"], s)
      add_nested_included_types(typ["values"], s)
    case ParseType.LISTNODE | ParseType.TREENODE:
      add_nested_included_types(typ["val"], s)
    case _:
      assert_never(curr_type)

def recursively_get_included_types(input_types, expected_type) -> set[ParseType]:
  ret: set[ParseType] = set()
  for input_type in input_types:
    add_nested_included_types(input_type, ret)
  add_nested_included_types(expected_type, ret)
  return ret

def get_required_imports(included_types: set[ParseType], language: Language) -> str:
  match language:
    case Language.PYTHON:
      return ("from __future__ import annotations\n" + "from typing import Optional\n\n"
              if ParseType.LISTNODE in included_types or ParseType.TREENODE in included_types
              else "")
    case Language.JAVA:
      imports = ""
      for t in [ParseType.LIST, ParseType.SET, ParseType.MAP]:
        if t in included_types:
          imports += f"import java.util.{member_to_string(t).capitalize()};\n"
      if imports:
        imports += "\n"
      return imports 
    case _:
      assert_never(language)

def get_required_class_line(solution_class_name: str, one_indent, language: Language) -> str:
  match language:
    case Language.PYTHON:
      return f"class {solution_class_name}:\n"
    case Language.JAVA:
      return f"public class {solution_class_name}" + " {\n"
    case _:
      assert_never(language)
    
def get_ending(one_indent, language: Language) -> str:
  match language:
    case Language.PYTHON:
      return ""
    case Language.JAVA:
      return "}\n"
    case _:
      assert_never(language)

def find_type(typ: dict[str, Any], to_find: ParseType) -> dict[str, Any] | None:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])
  if curr_type == to_find:
    return typ
  match curr_type:
    case ParseType.INT | ParseType.LONG | ParseType.FLOAT | ParseType.BOOLEAN | ParseType.STRING:
      return None
    case ParseType.ARRAY | ParseType.LIST | ParseType.IMMUTABLE_LIST | ParseType.SET:
      return find_type(typ["items"], to_find)
    case ParseType.MAP:
      key_typ = find_type(typ["keys"], to_find)
      return key_typ if key_typ is not None else find_type(typ["values"], to_find)
    case ParseType.LISTNODE | ParseType.TREENODE:
      return find_type(typ["val"], to_find)
    case _:
      assert_never(curr_type)

def get_nested_type_string(to_find: ParseType, field: str, 
                           input_types, expected_type):
  typ: dict[str, Any] | None = None
  for input_type in input_types:
    curr = find_type(input_type, to_find)
    if curr is not None:
      typ = curr
      break
  if typ is None:
    typ = find_type(expected_type, to_find)
  if typ is None:
    raise RuntimeError(f"Type not found: {to_find}")
  return BP_LANG_CLASS.parse_type_string(typ[field])
