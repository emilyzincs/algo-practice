import json
COMPLEX_TYPES = {"array", "list", "immutable_list", "set", "map", "ListNode", "TreeNode"}

def parse_type_string(typ, language: str) -> str:
  func_name = f"{language}_parse_type_string"
  func = globals().get(func_name)
  if func is None:
    raise ValueError(f"Unrecognized language: {language}.")
  func(typ)

def get_required_method_line(parameter_names: list[str], parameter_types: list[str], 
                             return_type: str, indent: str, 
                             required_method_name: str, language: str) -> str:
  if len(parameter_names) != len(parameter_types):
    raise ValueError(f"Must have same number of parameter names and types." +
                     " Names: {parameter_names}. Types: {parameter_types}.")
  func_name = f"{language}_get_method_line"
  func = globals().get(func_name)
  if func is None:
    raise ValueError(f"Unrecognized language: {language}.")
  func(parameter_names, parameter_types, return_type, indent, required_method_name)

def python_parse_type_string(typ) -> str:
  if typ["type"] in COMPLEX_TYPES and isinstance(val, str):
    try:
      val = json.loads(val)  # Convert string to Python object
    except json.JSONDecodeError:
      raise Exception(f"Could not parse string as JSON: {val}")
    
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
      return f"list[{parse_type_string(typ["items"])}]"
    case "list":
      return f"list[{parse_type_string(typ["items"])}]"
    case "immutable_list":
      return f"tuple[{parse_type_string(typ["items"])}]"
    case "set":
      return f"set[{parse_type_string(typ["items"])}]"
    case "map":
      return f"dict[{parse_type_string(typ["keys"])}, {parse_type_string(typ["values"])}]"
    case "ListNode":
      return "ListNode"
    case "TreeNode":
      return "TreeNode"
    case _:
      raise Exception(f"Unknown type: {typ["type"]}")

def java_parse_type_string(typ, should_box_if_primitive: False) -> str:

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
      return f"{parse_type_string(typ["items"], False)}[]"
    case "list":
      return f"List<{parse_type_string(typ["items"], True)}>"
    case "immutable_list":
      return f"{parse_type_string(typ["items"], False)}[]"
    case "set":
      return f"Set<{parse_type_string(typ["items"], True)}>"
    case "map":
      return f"Map<[{parse_type_string(typ["keys"], True)}, {parse_type_string(typ["values"], True)}>"
    case "ListNode":
      return "ListNode"
    case "TreeNode":
      return "TreeNode"
    case _:
      raise Exception(f"Unknown type: {typ["type"]}")
    
def python_get_method_line(parameter_names: list[str], parameter_types: list[str], 
                          return_type: str, indent: str, require_method_name: str) -> str:
  in_parentheses = None
  n = len(parameter_names)
  if n == 0:
    in_parentheses = ""
  else:
    in_parentheses = f"{parameter_names[0]}: {parameter_types[0]}"
    for i in range(1, n):
      in_parentheses += f", {parameter_names[i]}: {parameter_types[i]}"
  return f"{indent}def {require_method_name}({in_parentheses}):\n"

def java_get_method_line(parameter_names: list[str], parameter_types: list[str], 
                          return_type: str, indent: str, require_method_name: str) -> str:
  in_parentheses = None
  n = len(parameter_names)
  if n == 0:
    in_parentheses = ""
  else:
    in_parentheses = f"{parameter_names[0]}: {parameter_types[0]}"
    for i in range(1, n):
      in_parentheses += f", {parameter_types[i]} {parameter_names[i]}"
  return (f"{indent}public static {return_type} {require_method_name}({in_parentheses})" +
          " {\n" + indent + "\n" + indent + "}\n")

