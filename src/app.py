import sys
import os
import time
import base64
import uuid
from dotenv import load_dotenv
import sentry_sdk

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'src')))

from utils.analytics import log_async, log_async_audio
from thinker.openai_thinker import OpenaiThinker
from thinker.claude_thinker import ClaudeThinker
import memory.log_components as lc
import speech.tts as tts
import speech.stt as stt
from memory.memory_manager import MemoryManager
from brain.brain import Brain
from game.game_state import GameState
from flask_cors import CORS
from flask import Flask, request, send_file, jsonify

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

def configure_sentry():
    sentry_dsn = os.getenv("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(dsn=sentry_dsn, enable_tracing=True)
    else:
        print("Warning: SENTRY_DSN not set. Error tracking is disabled.")

configure_sentry()

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20000 per day", "4000 per hour"],
)

# Set up the variables
if os.getenv("THINKER_AI_TOOLKIT") == "claude":
    thinker_class = ClaudeThinker
elif os.getenv("THINKER_AI_TOOLKIT") == "openai":
    thinker_class = OpenaiThinker
else:
    raise ValueError(
        "THINKER_AI_TOOLKIT environment variable must be either 'claude' or 'openai'")

agent_brain = Brain(thinker_class=thinker_class)

# Set up the folder for audio files
os.makedirs("audio_files", exist_ok=True)
for file in os.listdir("audio_files"):
    os.remove(os.path.join("audio_files", file))


# Function to get the key for rate limiting (IP or Steam ID)
def get_limit_key():
    return request.get_json().get("player_id") or get_remote_address()


@app.route('/hello_world')
def hello_world():
    return "Hello, World!"


@app.route("/instruct_agent", methods=["POST"])
@limiter.limit("4000/hour", key_func=get_limit_key)
def instruct_agent():

    try:

        # Get request arguments
        request_json = request.get_json()
        player_id = request_json['player_id']
        timestamp = request_json.get('timestamp', time.time())
        game_state = GameState.from_json(request_json['game_state'])
        personality = request_json.get('personality', "")
        voice = request_json.get('voice', "asteria")
        agent_name = request_json.get('agent_name', "agent")
        voice_or_text = request_json.get('voice_or_text', "voice")

        player_instruction = ""

        if voice_or_text == "voice":
            # Get the audio file sent through the HTTP POST request
            player_instruction_audio_file_encoded_string = request_json[
                'player_instruction_audio_file_base64']
            player_instruction_audio_file_decoded_bytes = base64.b64decode(
                player_instruction_audio_file_encoded_string.encode("utf-8"))

            # Save the audio file to the audio_files folder
            player_instruction_audio_file_id = uuid.uuid4()
            player_instruction_audio_file_path = os.path.join(
                "audio_files", f"instruction_{player_instruction_audio_file_id}.wav")
            with open(player_instruction_audio_file_path, "wb") as file:
                file.write(player_instruction_audio_file_decoded_bytes)

            log_async_audio(
                player_instruction_audio_file_path,
                f"instruction_{player_instruction_audio_file_id}.wav",
                str(player_id),
                str(timestamp),
            )

            # Convert the audio file to text
            player_instruction = stt.transcribe_audio(
                player_instruction_audio_file_path)

        else:
            player_instruction = request_json['player_instruction_text']

        # Log the request into the analytics system
        request_dict = {
            "player_id": player_id,
            "timestamp": timestamp,
            "player_instruction": player_instruction,
            "game_state": game_state,
            "personality": personality,
            "voice": voice,
            "agent_name": agent_name
        }
        log_async("PLAYER_REQUEST", str(request_dict))

        # Get the output
        output = agent_brain.generate_agent_output(
            player_instruction, game_state, personality, agent_brain.get_memory_manager().get_player_memory(player_id), agent_name)

        # Speak the agent text response
        agent_text_response_audio_file_id = tts.synthesize_text(
            output.agent_text_response, voice)

        # Log this exchange
        agent_brain.get_memory_manager().get_player_memory(
            player_id).log_conversation("player", player_instruction, timestamp)
        agent_brain.get_memory_manager().get_player_memory(player_id).log_conversation(
            agent_name, output.agent_text_response, timestamp)
        agent_brain.get_memory_manager().get_player_memory(
            player_id).log_agent_commands(output.agent_commands, timestamp)
        agent_brain.get_memory_manager().get_player_memory(
            player_id).log_game_state(game_state, timestamp)

        should_synthesize_reflection = agent_brain.get_memory_manager(
        ).get_player_memory(player_id).should_synthesize_reflection()
        if should_synthesize_reflection:
            agent_brain.get_memory_manager().get_player_memory(
                player_id).async_synthesize_log_reflection()

        log_async_audio(
            f"audio_files/response_{agent_text_response_audio_file_id}.wav",
            f"response_{agent_text_response_audio_file_id}.wav",
            str(player_id),
            str(timestamp),
        )

        # Return the output object (agent commands and agent text response audio file)
        output = {
            "player_id": player_id,
            "timestamp": timestamp,
            "player_instruction_transcription": player_instruction,
            "agent_commands": list(map(lambda agent_command: agent_command.to_json(), output.agent_commands)),
            "agent_text_response": output.agent_text_response,
            "agent_text_response_audio_file_id": agent_text_response_audio_file_id,
            "thinker_ai_toolkit": os.getenv("THINKER_AI_TOOLKIT"),
            "personality": personality,
            "voice": voice
        }

        # Log the output into the analytics system
        log_async("AGENT_RESPONSE", str(output))

        return jsonify(output)
    
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({"error": str(e)}), 500


@app.route("/synthesize_audio", methods=["GET"])  # text-to-speech
def synthesize_audio():
    try:
        # Get the text to synthesize
        text = request.args.get('text')
        voice = request.args.get('voice', "asteria")

        if not text:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        # Synthesize the audio
        audio_file_id = tts.synthesize_text(text, voice)

        return jsonify({
            "audio_file_id": audio_file_id,
            "voice": voice,
            "text": text
        })
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({"error": str(e)}), 500


@app.route("/get_audio_file", methods=["GET"])
def get_audio_file():
    try:
        # Get the ID of the audio file
        audio_file_id = request.args.get('audio_file_id')
        if not audio_file_id:
            return jsonify({"error": "Missing 'audio_file_id' parameter"}), 400
        
        audio_file_path = f"audio_files/response_{audio_file_id}.wav"

        # Return the audio file (quick fix on fly machines)
        fly_path = '/workspace/' + audio_file_path
        local_path = '../' + audio_file_path

        if os.path.exists(fly_path):
            return send_file(fly_path)
        elif os.path.exists(local_path):
            return send_file(local_path)
        else:
            return jsonify({"error": "Audio file not found"}), 404
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({"error": str(e)}), 500


@app.route("/log_valheim", methods=["POST"])
@limiter.limit("4000/hour", key_func=get_limit_key)
def log_valheim():
    try:
        # Get request arguments
        request_json = request.get_json()
        player_id = request_json["player_id"]
        timestamp = request_json.get("timestamp", time.time())
        log_string = request_json["log_string"]

        # Log the request into the analytics system
        log_dict = {
            "player_id": player_id,
            "timestamp": timestamp,
            "log_string": log_string,
        }

        log_async("MOD_CLIENT_LOGS", str(log_dict))

        return jsonify(log_dict)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify({"error": str(e)}), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded", "description": e.description}), 429


if __name__ == '__main__':
    app.run(host='0.0.0.0')
