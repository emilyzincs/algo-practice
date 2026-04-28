import os
import sys
from groq import Groq, RateLimitError, InternalServerError # type: ignore

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

def get_response(prompt: str) -> str|None:
  try:
    chat_completion = client.chat.completions.create(
      messages=[
        {
          "role": "user",
          "content": prompt,
        }
      ],
      model=MODEL,
    )
    return chat_completion.choices[0].message.content

  except RateLimitError:
    print("Groq API rate limit hit.", file=sys.stderr)
    return None

  except InternalServerError:
    print("Groq's servers experienced an error.", file=sys.stderr)
    return None

  except Exception as e:
    raise Exception(f"An unexpected Groq error occurred: {e}")