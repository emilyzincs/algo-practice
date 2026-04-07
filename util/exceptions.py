class UnhandledCaseException(Exception):
  def __init__(self, input: str, case_type: str):
    msg = f"Unhandled {case_type} case: {input}."
    super().__init__(msg)
