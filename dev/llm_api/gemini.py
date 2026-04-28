from google import genai # type: ignore
from google.genai import errors # type: ignore
import sys

client = genai.Client()

MODEL = "gemini-3-flash-preview"


def get_response(prompt: str) -> str|None:
  try:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    return response.text

  except errors.ClientError as e:
    if e.code == 429:
      print("Gemini API rate limit hit.", file=sys.stderr)
      return None
    print("Client error: ", file=sys.stderr)
    raise 
    
  except errors.ServerError:
    print("Gemini's servers experienced an error.", file=sys.stderr)
    return None
    
  except Exception as e:
    print(f"An unexpected Gemini error occurred: {e}", file=sys.stderr)
    raise