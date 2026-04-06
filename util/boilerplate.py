from util.get_file_paths import get_practice_file_dir, PROJECT_ROOT
from util.exceptions import UnhandledCaseException
from commands.practice.java import path_to_package
from typing import assert_never, Any
from util.enums import Language, ParseType, is_member, member_from_string, member_to_string

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
      return python_parse_type_string(typ)
    case Language.JAVA:
      return java_parse_type_string(typ)
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
      return python_get_method_line(parameter_names, parameter_types, 
                                    return_type, one_indent, required_method_name)
    case Language.JAVA:
      return java_get_method_line(parameter_names, parameter_types, 
                                  return_type, one_indent, required_method_name)
    case _:
      assert_never()

def get_list_node_text(val_type_string: str, one_indent: str, 
                       num_indents: int, language: Language) -> str:
  match language:
    case Language.PYTHON:
      return python_list_node(val_type_string, one_indent, one_indent * num_indents)
    case Language.JAVA:
      return java_list_node(val_type_string, one_indent, one_indent * num_indents)
    case _:
      assert_never()

def get_tree_node_text(val_type_string: str, one_indent: str,
                      num_indents: int, language: Language) -> str:
    match language:
      case Language.PYTHON:
        return python_tree_node(val_type_string, one_indent, one_indent * num_indents)
      case Language.JAVA:
        return java_tree_node(val_type_string, one_indent, one_indent * num_indents)
      case _:
        assert_never()

def validate_type(typ: dict[str, Any]) -> None:
  if type(typ) != dict:
    raise ValueError(f"Not a dict: {typ}.")
  if "type" not in typ:
    raise ValueError(f"Type dicts must contain a 'type' field. Dict: {typ}.")
  if not type(typ["type"]) == str:
    raise ValueError("The  corresponding to 'type' in a type dict must be a string." +
                     f" Dict: {typ}.")
  if not is_member(ParseType, typ["type"]):
   raise ValueError("The value corresponding to 'type' in a type dict must be a ParseType type." +
                    f" Dict: {typ}.") 

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

def python_parse_type_string(typ: dict[str, Any]) -> str:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])
  match curr_type:
    case ParseType.INT:
      return "int"
    case ParseType.LONG:
      return "int"
    case ParseType.FLOAT:
      return "float"
    case ParseType.BOOLEAN:
      return "bool"
    case ParseType.STRING:
      return "str"
    case ParseType.ARRAY:
      return f"list[{python_parse_type_string(typ["items"])}]"
    case ParseType.LIST:
      return f"list[{python_parse_type_string(typ["items"])}]"
    case ParseType.IMMUTABLE_LIST:
      return f"tuple[{python_parse_type_string(typ["items"])}, ...]"
    case ParseType.SET:
      return f"set[{python_parse_type_string(typ["items"])}]"
    case ParseType.MAP:
      return (f"dict[{python_parse_type_string(typ["keys"])}," + 
             f" {python_parse_type_string(typ["values"])}]")
    case ParseType.LISTNODE:
      return "Optional[ListNode]"
    case ParseType.TREENODE:
      return "Optional[TreeNode]"
    case _:
      assert_never(curr_type)

def java_parse_type_string(typ: dict[str, Any], should_box_if_primitive: bool = False) -> str:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])
  match curr_type:
    case ParseType.INT:
      return "int" if not should_box_if_primitive else "Integer"
    case ParseType.LONG:
      return "long" if not should_box_if_primitive else "Long"
    case ParseType.FLOAT:
      return "double" if not should_box_if_primitive else "Double"
    case ParseType.BOOLEAN:
      return "boolean" if not should_box_if_primitive else "Boolean"
    case ParseType.STRING:
      return "String"
    case ParseType.ARRAY:
      return f"{java_parse_type_string(typ["items"], False)}[]"
    case ParseType.LIST:
      return f"List<{java_parse_type_string(typ["items"], True)}>"
    case ParseType.IMMUTABLE_LIST:
      return f"{java_parse_type_string(typ["items"], False)}[]"
    case ParseType.SET:
      return f"Set<{java_parse_type_string(typ["items"], True)}>"
    case ParseType.MAP:
      return (f"Map<{java_parse_type_string(typ["keys"], True)}," + 
             f" {java_parse_type_string(typ["values"], True)}>")
    case ParseType.LISTNODE:
      return "ListNode"
    case ParseType.TREENODE:
      return "TreeNode"
    case _:
      assert_never(curr_type)
    
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

def java_list_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
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

def java_tree_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
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
