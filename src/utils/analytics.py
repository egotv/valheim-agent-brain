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


def log_sync_audio(filepath: str, file_base_path: str, player_id: str, timestamp: str):
    try:
        with open(filepath, 'rb') as f:
            supabase.storage.from_("audio").upload(
                file=f,
                path="audio/" + player_id + f"/{timestamp}" + f"/{file_base_path}",
                file_options={"content-type": "audio/wav"},
            )

    except Exception as e:
        print(f"Failed to log audio to Supabase: {e}")


def log_async_audio(filepath: str, file_base_path: str, player_id: str, timestamp: str):
    thread = threading.Thread(
        target=log_sync_audio, args=(filepath, file_base_path, player_id, timestamp)
    )
    thread.start()


def log_sync_game_logs(filepath: str, file_base_path: str, player_id: str):
    try:
        with open(filepath, "rb") as f:
            supabase.storage.from_("textlogs").upload(
                file=f,
                path="textlogs/" + player_id + f"/{file_base_path}",
                file_options={"content-type": "audio/wav"},
            )

    except Exception as e:
        print(f"Failed to log game logs to Supabase: {e}")


def log_async_game_logs(filepath: str, file_base_path: str, player_id: str):
    thread = threading.Thread(
        target=log_sync_game_logs, args=(filepath, file_base_path, player_id)
    )
    thread.start()


# Example usage
# if __name__ == "__main__":
#     log_async_audio("./audio_files/Recording.wav",
#                     "Recording.wav", "player123")
# log_async("info", "This is a log entry.")
