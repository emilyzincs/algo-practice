from typing import assert_never, Any, override
from boilerplate.util import validate_type
from util.enums import ParseType, member_from_string, member_to_string
from boilerplate.interface import BpInterface
from util.file_paths import get_practice_file_dir, PROJECT_ROOT
from user_testing.test_commands.java import path_to_package


# Java implementation of the boilerplate interface
class JavaBp(BpInterface):

  @override
  def get_start(self) -> str:
    return "package " + path_to_package(get_practice_file_dir(), PROJECT_ROOT) + ";\n\n"
  
  @override
  def get_imports(self, included_types: set[ParseType]) -> str:
    imports = ""
    for t in [ParseType.LIST, ParseType.SET, ParseType.MAP]:
      if t in included_types:
        imports += f"import java.util.{member_to_string(t).capitalize()};\n"
    if imports:
      imports += "\n"
    return imports 

  @override
  def get_class_declaration(self, class_name, one_indent) -> str:
    return f"public class {class_name}" + " {\n"

  @override
  def get_method_declaration(self, require_method_name: str, parameter_names: list[str], 
                             parameter_types: list[str], 
                            return_type: str, one_indent: str) -> str:
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

  @override
  def parse_type_string(self, typ: dict[str, Any], should_box_if_primitive: bool = False) -> str:
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
        return f"{self.parse_type_string(typ["items"], False)}[]"
      case ParseType.LIST:
        return f"List<{self.parse_type_string(typ["items"], True)}>"
      case ParseType.IMMUTABLE_LIST:
        return f"{self.parse_type_string(typ["items"], False)}[]"
      case ParseType.SET:
        return f"Set<{self.parse_type_string(typ["items"], True)}>"
      case ParseType.MAP:
        return (f"Map<{self.parse_type_string(typ["keys"], True)}," + 
              f" {self.parse_type_string(typ["values"], True)}>")
      case ParseType.LISTNODE:
        return "ListNode"
      case ParseType.TREENODE:
        return "TreeNode"
      case _:
        assert_never(curr_type)

  @override
  def list_node(self, val_type_string: str, one_indent: str, base_indent: str) -> str:
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

  @override
  def tree_node(self, val_type_string: str, one_indent: str, base_indent: str) -> str:
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
  
  @override
  def get_end(self, one_indent: str) -> str:
    return "}\n"
