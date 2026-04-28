from dev.llm_api.gemini import get_response as get_gemini_response
from dev.llm_api.groq import get_response as get_groq_response

llm_apis = [get_groq_response, get_gemini_response]

def get_response(prompt: str, idx: int = 0) -> tuple[str, int]:
  for i in range(idx, len(llm_apis)):
    llm_api = llm_apis[i]
    resp: str|None = llm_api(prompt)
    if resp is not None:
      return resp, idx
  raise RuntimeError("No llm API gave a response.")
