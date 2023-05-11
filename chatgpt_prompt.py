import openai

# KEY OpenAI
openai.api_key = "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"

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message
