import threading
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

# Initialize Supabase client from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def log_sync(category: str, content: str):

    try:
        data = {"category": category, "content": content}
        response = supabase.table('logs').insert(data).execute()
    except Exception as e:
        print(f"Failed to log to Supabase: {e}")


def log_async(category: str, content: str):
    thread = threading.Thread(target=log_sync, args=(category, content))
    thread.start()

# Example usage
# if __name__ == "__main__":
#     log_async("info", "This is a log entry.")
