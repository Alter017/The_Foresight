from openai import OpenAI
from prompts.pros_cons_prompt import PC_PROMPT, build_user_prompt
import os #lets us read api key from .env
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #making openai client 

def generate_pros_cons(scenario, options):
    user_prompt = build_user_prompt(scenario, options)

    print("Calling OpenAI...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": PC_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
        )
    except Exception as e:
        print("OpenAI error:", e)
        return {"error": "LLM failed"}

    print("OpenAI responded")

    content = response.choices[0].message.content

    try:
        content = content.strip()

        start = content.find("[")
        end = content.rfind("]") + 1

        parsed_content = json.loads(content[start:end])
        formatted = []
        for item in parsed_content:
            formatted.append({
                "name": item.get("name") or item.get("option"),
                "shortPros": item.get("shortPros", []),
                "shortCons": item.get("shortCons", []),
                "longPros": item.get("longPros", []),
                "longCons": item.get("longCons", [])
            })

        return formatted
        
    except json.JSONDecodeError:
        print("Bad JSON:", content)
        return []

        
