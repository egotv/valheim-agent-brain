import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

def run(prompt: str, model="claude-3-5-sonnet-20240620", temperature=1.0) -> str:

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="Follow the instructions in the prompt strictly.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return message.content[0].text

if __name__ == "__main__":
    run("Why is the ocean salty?")