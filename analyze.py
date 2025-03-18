import openai
from config_reader import openai_api_key
from prompt_reader import read_prompt

api_key = openai_api_key()
prompt = read_prompt()

def analyze_post(post_text):
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a text analyzer. Extract information from the following listing. You can also normalize it for yourself."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": post_text}]
        )
        return response.choices[0].message.content
    except openai.AuthenticationError:
        return "Invalid API Key!"
    except Exception as e:
        return ("Error:", str(e))
