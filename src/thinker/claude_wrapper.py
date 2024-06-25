import os
from anthropic import Anthropic
from dotenv import load_dotenv
import utils.utils as utils

load_dotenv()

client = Anthropic()

def run(prompt: str, model="claude-3-5-sonnet-20240620", temperature=1.0) -> str:

    utils.log_timestamp(marker="Anthropic Completions Start")
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=temperature,
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
    result = message.content[0].text
    utils.log_timestamp(marker=f"Anthropic Completions End ({result})")

    return result

if __name__ == "__main__":
    run("Why is the ocean salty?")