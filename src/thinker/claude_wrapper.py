import os
from anthropic import Anthropic
from dotenv import load_dotenv
import utils.utils as utils
from utils.analytics import log_async

load_dotenv()

client = Anthropic()

def run(prompt: str, model="claude-3-5-sonnet-20240620", temperature=0.9) -> str:

    start_timestamp = utils.get_timestamp()

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
    
    time_elapsed = utils.get_timestamp() - start_timestamp
    log_async("CLAUDE_CHAT_LATENCY", f"{time_elapsed}")

    return result

if __name__ == "__main__":
    run("Why is the ocean salty?")