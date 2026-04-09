# Runtime error for when cases were meant to be exhaustively handled
# but were not.
class UnhandledCaseError(RuntimeError):
  def __init__(self, input: str, case_type: str):
    msg = f"Unhandled {case_type} case: {input}."
    super().__init__(msg)
