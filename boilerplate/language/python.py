from typing import assert_never, Any, override
from boilerplate.util import validate_type
from boilerplate.interface import BpInterface
from util.enums import ParseType, member_from_string


# Python implementation of the boilerplate interface
class PythonBp(BpInterface):

  @override
  def get_start(self, path: str) -> str:
    return ""
  
  @override
  def get_imports(self, included_types: set[ParseType]) -> str:
    return ""

  @override
  def get_class_declaration(self, class_name, one_indent) -> str:
    return f"class {class_name}:\n"

  @override
  def get_method_declaration(self, require_method_name: str, parameter_names: list[str], 
                             parameter_types: list[str], 
                            return_type: str, one_indent: str) -> str:
    in_parentheses = None
    n = len(parameter_names)
    in_parentheses = "self"
    for i in range(n):
      in_parentheses += f", {parameter_names[i]}: {parameter_types[i]}"
    return (f"{one_indent}def {require_method_name}({in_parentheses})" + 
            f" -> {return_type}:\n{one_indent * 2}")

  @override
  def parse_type_string(self, typ: dict[str, Any]) -> str:
    validate_type(typ)
    curr_type: ParseType = member_from_string(ParseType, typ["type"])
    match curr_type:
      case ParseType.INT | ParseType.LONG:
        return "int"
      case ParseType.FLOAT:
        return "float"
      case ParseType.BOOLEAN:
        return "bool"
      case ParseType.STRING:
        return "str"
      case ParseType.ARRAY | ParseType.LIST | ParseType.UNORDERED_LIST:
        return f"list[{self.parse_type_string(typ["items"])}]"
      case _:
        assert_never(curr_type)

  @override
  def get_end(self, one_indent: str) -> str:
    return ""
