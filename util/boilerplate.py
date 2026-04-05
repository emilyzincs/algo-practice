from util.get_file_paths import get_practice_file_dir, PROJECT_ROOT
from util.exceptions import UnhandledCaseException
from commands.practice.java import path_to_package
COMPLEX_TYPES = {"array", "list", "immutable_list", "set", "map", "ListNode", "TreeNode"}

def get_boilerplate_text(
  parameter_names: list[str],
  input_types,
  expected_type,
  one_indent: str,
  solution_class_name: str,
  solution_function_name: str,
  language: str
):
  parameter_type_strings = [parse_type_string(input_type, language) for input_type in input_types]
  return_type_string = parse_type_string(expected_type, language)
  included_types = recursively_get_included_types(input_types, expected_type)

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
  if "ListNode" in included_types:
    val_type_string = get_nested_type_string("ListNode", "val", input_types, expected_type, language)
    list_node_text = get_list_node_text(val_type_string, one_indent, 1, language) 
  if "TreeNode" in included_types:
    val_type_string = get_nested_type_string("TreeNode", "val", input_types, expected_type, language)
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

def parse_type_string(typ, language: str) -> str:
  func_name = f"{language}_parse_type_string"
  func = globals().get(func_name)
  if func is None:
    raise UnhandledCaseException(language, "language")
  return func(typ)

def get_beginning(language: str) -> str:
  match language:
    case "python":
      return ""
    case "java":
      return "package " + path_to_package(get_practice_file_dir(), PROJECT_ROOT) + ";\n\n"
    case _:
      raise UnhandledCaseException(language, "language") 

def get_required_method_line(
    parameter_names: list[str],
    parameter_types: list[str], 
    return_type: str, 
    one_indent: str, 
    required_method_name: str, 
    language: str
) -> str:
  if len(parameter_names) != len(parameter_types):
    raise ValueError(f"Must have same number of parameter names and types." +
                     f" Names: {parameter_names}. Types: {parameter_types}.")
  func_name = f"{language}_get_method_line"
  func = globals().get(func_name)
  if func is None:
    raise UnhandledCaseException(language, "language")
  return func(parameter_names, parameter_types, return_type, one_indent, required_method_name)

def get_list_node_text(val_type_string: str, one_indent: str, 
                       num_indents: int, language: str) -> str:
  func_name = f"{language}_list_node"
  func = globals().get(func_name)
  if func is None:
    raise UnhandledCaseException(language, "language")
  return func(val_type_string, one_indent, one_indent * num_indents)

def get_tree_node_text(val_type_string: str, one_indent: str,
                      num_indents: int, language: str) -> str:
  func_name = f"{language}_tree_node"
  func = globals().get(func_name)
  if func is None:
    raise UnhandledCaseException(language, "language")
  return func(val_type_string, one_indent, one_indent * num_indents)

def get_nested_included_types(typ, s: set[str]):
  s.add(typ["type"])
  match typ["type"]:
    case "int" | "long" | "float" | "boolean" | "string":
      pass
    case "array" | "list" | "immutable_list" | "set":
      get_nested_included_types(typ["items"], s)
    case "map":
      get_nested_included_types(typ["keys"], s)
      get_nested_included_types(typ["values"], s)
    case "ListNode" | "TreeNode":
      get_nested_included_types(typ["val"], s)
    case _:
      raise UnhandledCaseException(typ["type"], "type")

def recursively_get_included_types(input_types, expected_type) -> set[str]:
  ret: set[str] = set()
  for input_type in input_types:
    get_nested_included_types(input_type, ret)
  get_nested_included_types(expected_type, ret)
  return ret

def get_required_imports(included_types: set[str], language: str) -> str:
  match language:
    case "python":
      return ("from __future__ import annotations\n" + "from typing import Optional\n\n"
              if "ListNode" in included_types or "TreeNode" in included_types
              else "")
    case "java":
      imports = ""
      for t in ["list", "set", "map"]:
        if t in included_types:
          imports += f"import java.util.{t.capitalize()};\n"
      if imports:
        imports += "\n"
      return imports 
    case _:
      raise UnhandledCaseException(language, "language")

def get_required_class_line(solution_class_name: str, one_indent, language: str) -> str:
  match language:
    case "python":
      return f"class {solution_class_name}:\n"
    case "java":
      return f"public class {solution_class_name}" + " {\n"
    case _:
      raise UnhandledCaseException(language, "language")
    
def get_ending(one_indent, language: str) -> str:
  match language:
    case "python":
      return ""
    case "java":
      return "}\n"
    case _:
      raise UnhandledCaseException(language, "language")

def python_parse_type_string(typ) -> str:  
  match typ["type"]:
    case "int":
      return "int"
    case "long":
      return "int"
    case "float":
      return "float"
    case "boolean":
      return "bool"
    case "string":
      return "str"
    case "array":
      return f"list[{python_parse_type_string(typ["items"])}]"
    case "list":
      return f"list[{python_parse_type_string(typ["items"])}]"
    case "immutable_list":
      return f"tuple[{python_parse_type_string(typ["items"])}]"
    case "set":
      return f"set[{python_parse_type_string(typ["items"])}]"
    case "map":
      return (f"dict[{python_parse_type_string(typ["keys"])}," + 
             f" {python_parse_type_string(typ["values"])}]")
    case "ListNode":
      return "Optional[ListNode]"
    case "TreeNode":
      return "Optional[TreeNode]"
    case _:
      raise UnhandledCaseException(typ["type"], "type")

def java_parse_type_string(typ, should_box_if_primitive: bool = False) -> str:
  match typ["type"]:
    case "int":
      return "int" if not should_box_if_primitive else "Integer"
    case "long":
      return "long" if not should_box_if_primitive else "Long"
    case "float":
      return "double" if not should_box_if_primitive else "Double"
    case "boolean":
      return "boolean" if not should_box_if_primitive else "Boolean"
    case "string":
      return "String"
    case "array":
      return f"{java_parse_type_string(typ["items"], False)}[]"
    case "list":
      return f"List<{java_parse_type_string(typ["items"], True)}>"
    case "immutable_list":
      return f"{java_parse_type_string(typ["items"], False)}[]"
    case "set":
      return f"Set<{java_parse_type_string(typ["items"], True)}>"
    case "map":
      return (f"Map<{java_parse_type_string(typ["keys"], True)}," + 
             f" {java_parse_type_string(typ["values"], True)}>")
    case "ListNode":
      return "ListNode"
    case "TreeNode":
      return "TreeNode"
    case _:
      raise UnhandledCaseException(typ["type"], "type")
    
def python_get_method_line(parameter_names: list[str], parameter_types: list[str], 
                          return_type: str, one_indent: str, require_method_name: str) -> str:
  in_parentheses = None
  n = len(parameter_names)
  in_parentheses = "self"
  for i in range(n):
    in_parentheses += f", {parameter_names[i]}: {parameter_types[i]}"
  return (f"{one_indent}def {require_method_name}({in_parentheses})" + 
          f" -> {return_type}:\n{one_indent * 2}")

def java_get_method_line(parameter_names: list[str], parameter_types: list[str], 
                          return_type: str, one_indent: str, require_method_name: str) -> str:
  in_parentheses = None
  n = len(parameter_names)
  if n == 0:
    in_parentheses = ""
  else:
    in_parentheses = f"{parameter_types[0]} {parameter_names[0]}"
    for i in range(1, n):
      in_parentheses += f", {parameter_types[i]} {parameter_names[i]}"
  return (f"{one_indent}public static {return_type} {require_method_name}({in_parentheses})" +
          " {\n" + (one_indent * 2) + f"\n{one_indent}" + "}\n")

def find_type(typ, to_find):
  if typ["type"] == to_find:
    return typ
  match typ["type"]:
    case "int" | "long" | "float" | "bool" | "string":
      return None
    case "array" | "list" | "immutable_list" | "set":
      return find_type(typ["items"], to_find)
    case "map":
      key_typ = find_type(typ["keys"], to_find)
      return key_typ if key_typ is not None else find_type(typ["values"], to_find)
    case "ListNode" | "TreeNode":
      return find_type(typ["val"], to_find)
    case _:
      raise UnhandledCaseException(typ["type"], "type")

def get_nested_type_string(to_find: str, field: str, 
                           input_types, expected_type, language: str):
  typ = None
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

def python_list_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
  base_indent = ""
  return (
    "\n\n" +
    f"{base_indent}class ListNode:\n" +
    f"{base_indent}{one_indent}def __init__(self, val: {val_type_string}," + 
                              " next: Optional[ListNode]) -> None:\n" +
    f"{base_indent}{one_indent * 2}self.val = val\n" +
    f"{base_indent}{one_indent * 2}self.next = next\n"
  )

def java_list_node(val_type_string: str, one_indent: str, base_indent: int) -> str:
  return (
    "\n\n" +
    f"{base_indent}public static class ListNode" + " {\n" +
    f"{base_indent}{one_indent}public {val_type_string} val;\n" +
    f"{base_indent}{one_indent}public ListNode next;\n\n" +

    f"{base_indent}{one_indent}public ListNode({val_type_string} val," + 
                              " ListNode next) {\n" +
    f"{base_indent}{one_indent * 2}this.val = val;\n" +
    f"{base_indent}{one_indent * 2}this.next = next;\n" +
    f"{base_indent}{one_indent}" + "}\n" +
    f"{base_indent}" + "}\n"
  )

def python_tree_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
  base_indent = ""
  return (
    "\n\n" +
    f"{base_indent}class TreeNode:\n" +
    f"{base_indent}{one_indent}def __init__(self, val: {val_type_string}," + 
                              " left: Optional[TreeNode]," + 
                              " right: Optional[TreeNode]) -> None:\n" +
    f"{base_indent}{one_indent * 2}self.val = val\n" +
    f"{base_indent}{one_indent * 2}self.left = left\n" + 
    f"{base_indent}{one_indent * 2}self.right = right\n"
  )

def java_tree_node(val_type_string: str, one_indent: str, base_indent: int) -> str:
  return (
    "\n\n" + 
    f"{base_indent}public static class TreeNode" + " {\n" +
    f"{base_indent}{one_indent}public {val_type_string} val;\n" +
    f"{base_indent}{one_indent}public TreeNode left;\n" +
    f"{base_indent}{one_indent}public TreeNode right;\n\n" +

    f"{base_indent}{one_indent}public TreeNode({val_type_string} val," + 
                              " TreeNode left, TreeNode right) {\n" +
    f"{base_indent}{one_indent * 2}this.val = val;\n" +
    f"{base_indent}{one_indent * 2}this.left = left;\n" +
    f"{base_indent}{one_indent * 2}this.right = right;\n" +
    f"{base_indent}{one_indent}" + "}\n" +
    f"{base_indent}" + "}\n"
  )

