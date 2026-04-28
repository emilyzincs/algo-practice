from abc import ABC, abstractmethod
from typing import Any
from util.enums import ParseType


# Interface for boilerplate text generation that each language must implement
class BpInterface(ABC):

  # Returns the pre-import boilerplate as a string (e.g. package declaration).
  @abstractmethod
  def get_start(self, implementation_dir: str) -> str:
    pass

  # Returns string representing the imports corresponding to the class 
  # and method declaration.
  @abstractmethod
  def get_imports(self, included_types: set[ParseType]) -> str:
    pass
  
  # Returns the class declaration as a string
  @abstractmethod
  def get_class_declaration(self, class_name: str, one_indent: str) -> str:
    pass

  # Returns the string representing the method declaration corresponding
  # to the given 'parameter_names', 'parameter_types', 'return_type', 
  # and 'required_method_name', using appropriate indentation as specified by 'one_indent'.
  @abstractmethod
  def get_method_declaration(self, method_name: str, parameter_names: list[str], 
                             parameter_types: list[str], 
                             return_type: str, one_indent: str) -> str:
    pass
  
  # Parses a recursive JSON type description 'typ' into the corresponding type string
  # and returns it.
  @abstractmethod
  def parse_type_string(self, typ: dict[str, Any]) -> str:
    pass
  
  # Returns the end boilerplate as a string (e.g., closing curly brace).
  @abstractmethod
  def get_end(self, one_indent: str) -> str:
    pass
