from util.file_paths import get_practice_file_dir, PROJECT_ROOT
from commands.practice.java import path_to_package
from typing import assert_never, Any
from util.enums import Language, ParseType, member_from_string, member_to_string
from boilerplate.util import validate_type
import boilerplate.language.java as java_bp
import boilerplate.language.python as python_bp

def get_boilerplate_text(
  parameter_names: list[str],
  input_types,
  expected_type,
  one_indent: str,
  solution_class_name: str,
  solution_function_name: str,
  language: Language
):
  parameter_type_strings = [parse_type_string(input_type, language) for input_type in input_types]
  return_type_string = parse_type_string(expected_type, language)
  included_types: set[ParseType] = recursively_get_included_types(input_types, expected_type)

  beginning = get_beginning(language)
  imports = get_required_imports(included_types, language)
  class_line = get_required_class_line(solution_class_name, one_indent, language)
  method_line = get_required_method_line(
    parameter_names, 
    parameter_type_strings, 
    return_type_string, 
    one_indent,
    solution_function_name,
    language
  )
  list_node_text = ""
  tree_node_text = ""
  if ParseType.LISTNODE in included_types:
    val_type_string = get_nested_type_string(ParseType.LISTNODE, "val",
                                            input_types, expected_type, language)
    list_node_text = get_list_node_text(val_type_string, one_indent, 1, language) 
  if ParseType.TREENODE in included_types:
    val_type_string = get_nested_type_string(ParseType.TREENODE, "val",
                                             input_types, expected_type, language)
    tree_node_text = get_tree_node_text(val_type_string, one_indent, 1, language)
  end = get_ending(one_indent, language)

  ret = "".join([
    beginning, 
    imports, 
    class_line, 
    method_line, 
    list_node_text, 
    tree_node_text, 
    end
  ])
  return ret

def parse_type_string(typ, language: Language) -> str:
  match language:
    case Language.PYTHON:
      return python_bp.parse_type_string(typ)
    case Language.JAVA:
      return java_bp.parse_type_string(typ)
    case _:
      assert_never()

def get_beginning(language: Language) -> str:
  match language:
    case Language.PYTHON:
      return ""
    case Language.JAVA:
      return "package " + path_to_package(get_practice_file_dir(), PROJECT_ROOT) + ";\n\n"
    case _:
      assert_never()

def get_required_method_line(
    parameter_names: list[str],
    parameter_types: list[str], 
    return_type: str, 
    one_indent: str, 
    required_method_name: str, 
    language: Language
) -> str:
  if len(parameter_names) != len(parameter_types):
    raise ValueError(f"Must have same number of parameter names and types." +
                     f" Names: {parameter_names}. Types: {parameter_types}.")
  match language:
    case Language.PYTHON:
      return python_bp.get_method_line(parameter_names, parameter_types, 
                                    return_type, one_indent, required_method_name)
    case Language.JAVA:
      return java_bp.get_method_line(parameter_names, parameter_types, 
                                  return_type, one_indent, required_method_name)
    case _:
      assert_never()

def get_list_node_text(val_type_string: str, one_indent: str, 
                       num_indents: int, language: Language) -> str:
  match language:
    case Language.PYTHON:
      return python_bp.list_node(val_type_string, one_indent, one_indent * num_indents)
    case Language.JAVA:
      return java_bp.list_node(val_type_string, one_indent, one_indent * num_indents)
    case _:
      assert_never()

def get_tree_node_text(val_type_string: str, one_indent: str,
                      num_indents: int, language: Language) -> str:
    match language:
      case Language.PYTHON:
        return python_bp.tree_node(val_type_string, one_indent, one_indent * num_indents)
      case Language.JAVA:
        return java_bp.tree_node(val_type_string, one_indent, one_indent * num_indents)
      case _:
        assert_never()

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
                           input_types, expected_type, language: Language):
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
  return parse_type_string(typ[field], language)




