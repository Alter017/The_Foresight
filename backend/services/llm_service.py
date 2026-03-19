from openai import OpenAI
from prompts.pros_cons_prompt import PC_PROMPT, build_user_prompt
import os #lets us read api key from .env
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #making openai client 

def generate_pros_cons(scenario, options):
    user_prompt = build_user_prompt(scenario, options)

    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content":PC_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7 #how varaible we want the response to be. 0.2-0.5 is strict, less varied more predictable. 
    )

    content = response.choices[0].message.content

    try:
        #convert json string to python dict
        parsed_content = json.loads(content)
        return parsed_content
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by model",
            "raw_output": content
        }

    