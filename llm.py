
from openai import OpenAI
from openai import OpenAI
from config import BASE_URL, HF_API_KEY, MAX_TOKENS, MODEL_NAME, TEMPERATURE




if not HF_API_KEY:
  raise ValueError(
      "problem with API_KEY in .env"
      )
  

client = OpenAI(
    base_url=BASE_URL,
    api_key=HF_API_KEY,
)


def ask_llm(system_prompt, user_prompt):
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return completion.choices[0].message.content
    except Exception as e:
       print(f"model connection failed {e}")
       return f"ERROR:   failed connection model - {str(e)}"



