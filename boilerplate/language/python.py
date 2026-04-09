from typing import assert_never, Any
from boilerplate.util import validate_type
from boilerplate.interface import BpInterface
from util.enums import ParseType, member_from_string


# Python implementation of the boilerplate interface
class PythonBp(BpInterface):
  @staticmethod
  def get_start() -> str:
    return ""
  
  @staticmethod
  def get_imports(included_types: set[ParseType]) -> str:
    return ("from __future__ import annotations\n" + "from typing import Optional\n\n"
              if ParseType.LISTNODE in included_types or ParseType.TREENODE in included_types
              else "")

  @staticmethod
  def get_class_declaration(class_name, one_indent):
    return f"class {class_name}:\n"

  @staticmethod
  def get_method_line(parameter_names: list[str], parameter_types: list[str], 
                            return_type: str, one_indent: str, require_method_name: str) -> str:
    in_parentheses = None
    n = len(parameter_names)
    in_parentheses = "self"
    for i in range(n):
      in_parentheses += f", {parameter_names[i]}: {parameter_types[i]}"
    return (f"{one_indent}def {require_method_name}({in_parentheses})" + 
            f" -> {return_type}:\n{one_indent * 2}")

  @staticmethod
  def parse_type_string(typ: dict[str, Any]) -> str:
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
        return f"list[{PythonBp.parse_type_string(typ["items"])}]"
      case ParseType.LIST:
        return f"list[{PythonBp.parse_type_string(typ["items"])}]"
      case ParseType.IMMUTABLE_LIST:
        return f"tuple[{PythonBp.parse_type_string(typ["items"])}, ...]"
      case ParseType.SET:
        return f"set[{PythonBp.parse_type_string(typ["items"])}]"
      case ParseType.MAP:
        return (f"dict[{PythonBp.parse_type_string(typ["keys"])}," + 
              f" {PythonBp.parse_type_string(typ["values"])}]")
      case ParseType.LISTNODE:
        return "Optional[ListNode]"
      case ParseType.TREENODE:
        return "Optional[TreeNode]"
      case _:
        assert_never(curr_type)

  @staticmethod
  def list_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
    base_indent = ""
    return (
      "\n\n" +
      f"{base_indent}class ListNode:\n" +
      f"{base_indent}{one_indent}def __init__(self, val: {val_type_string}," + 
                                " next: Optional[ListNode]) -> None:\n" +
      f"{base_indent}{one_indent * 2}self.val = val\n" +
      f"{base_indent}{one_indent * 2}self.next = next\n"
    )

  @staticmethod
  def tree_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
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

  @staticmethod
  def get_end(one_indent: str) -> str:
    return ""
