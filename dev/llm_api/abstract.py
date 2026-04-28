from dev.llm_api.gemini import get_response as get_gemini_response
from dev.llm_api.groq import get_response as get_groq_response

llm_apis = [get_gemini_response]

def get_response(prompt: str) -> str:
  for llm_api in llm_apis:
    resp: str|None = llm_api(prompt)
    if resp is not None:
      return resp
  raise RuntimeError("No llm API gave a response.")
