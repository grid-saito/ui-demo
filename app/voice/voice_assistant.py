import asyncio
import websockets
import pyaudio
import base64
import json
import os
from io import BytesIO
from scipy.io.wavfile import write
import streamlit as st
from dotenv import load_dotenv
from prompt import instruction
from voice.config import tools_json 
from utils import add_debug_message

# Load environment variables
load_dotenv()

# Azure OpenAI settings
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
WS_URL = os.getenv("AZURE_OPENAI_WS_URL")
HEADERS = {
    "api-key": API_KEY,
}

# PCM16 conversion helper
def base64_to_pcm16(base64_audio):
    return base64.b64decode(base64_audio)

# Save PCM16 data to WAV format
def save_pcm16_to_wav(pcm16_audio, rate=24000):
    buffer = BytesIO()
    write(buffer, rate, pcm16_audio)
    buffer.seek(0)  # Reset the buffer to the beginning for reading
    return buffer

# WebSocket communication for voice assistant
async def stream_audio_and_process_commands(command_processor):
    add_debug_message("[DEBUG] Starting WebSocket connection...")
    try:
        async with websockets.connect(WS_URL, additional_headers=HEADERS) as websocket:
            add_debug_message("[DEBUG] WebSocket connection established.")

            # Configure session
            init_request = {
                "type": "session.update",
                "session": {
                    "voice": "alloy",
                    "instructions": instruction,
                    "input_audio_format": "pcm16",
                    "input_audio_transcription": {"model": "whisper-1"},
                    "turn_detection": {"type": "server_vad", "threshold": 0.4, "silence_duration_ms": 600},
                    "tools": tools_json
                },
            }
            add_debug_message(f"[DEBUG] Sending session configuration: {json.dumps(init_request, indent=2)}")
            await websocket.send(json.dumps(init_request))

            # Set up audio streaming
            CHUNK = 2048
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 24000
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

            add_debug_message("[DEBUG] Audio stream initialized.")

            async def send_audio():
                add_debug_message("[DEBUG] Starting audio sending loop...")
                while True:
                    try:
                        audio_data = stream.read(CHUNK, exception_on_overflow=False)
                        base64_audio = base64.b64encode(audio_data).decode("utf-8")
                        audio_event = {"type": "input_audio_buffer.append", "audio": base64_audio}
                        await websocket.send(json.dumps(audio_event))
                    except Exception as e:
                        add_debug_message(f"[ERROR] Error while sending audio: {e}")

            async def process_responses():
                add_debug_message("[DEBUG] Starting response processing loop...")
                audio_buffers = []  # Store audio chunks for playback
                transcription = ""  # Store text transcription

                while True:
                    try:
                        response = await websocket.recv()
                        response_data = json.loads(response)
                        add_debug_message(f"[DEBUG] Received response: {json.dumps(response_data, indent=2)}")

                        # Handle transcription updates
                        if response_data.get("type") == "response.audio_transcript.delta":
                            delta = response_data.get("delta", "")
                            transcription += delta
                            add_debug_message(f"[DEBUG] Transcript update: {delta}")
                            add_debug_message(f"Current Transcript: {transcription}")

                        # Final transcription
                        elif response_data.get("type") == "response.audio_transcript.done":
                            add_debug_message(f"Final Transcript: {transcription}")
                            transcription = ""  # Reset transcription for next response

                        # Handle audio data
                        elif response_data.get("type") == "response.audio.delta":
                            base64_audio_response = response_data.get("delta", "")
                            if base64_audio_response:
                                pcm16_audio = base64_to_pcm16(base64_audio_response)
                                audio_buffers.append(pcm16_audio)

                                # Convert to WAV and play
                                wav_audio = save_pcm16_to_wav(pcm16_audio)
                                st.audio(wav_audio, format="audio/wav")
                         
                        # Handle function call arguments (done)
                        elif response_data.get("type") == "response.function_call_arguments.done":
                            function_name = response_data.get("name")
                            function_args = json.loads(response_data.get("arguments", "{}"))

                            add_debug_message(f"[DEBUG] Function call received: {function_name}")
                            add_debug_message(f"[DEBUG] Arguments: {function_args}")

                            # Call the appropriate function
                            if function_name in globals():
                                function = globals()[function_name]
                                function(**function_args)
                            else:
                                add_debug_message(f"[ERROR] Function '{function_name}' not found.")

                    except Exception as e:
                        add_debug_message(f"[ERROR] Error while processing response: {e}")

            try:
                await asyncio.gather(send_audio(), process_responses())
            except Exception as e:
                add_debug_message(f"[ERROR] Unexpected error during async tasks: {e}")
            finally:
                add_debug_message("[DEBUG] Closing audio streams.")
                stream.stop_stream()
                stream.close()
                p.terminate()

    except websockets.exceptions.InvalidStatusCode as e:
        add_debug_message(f"[ERROR] WebSocket connection failed with status code: {e.status_code}")
    except Exception as e:
        add_debug_message(f"[ERROR] Unexpected error: {e}")
    finally:
        add_debug_message("[DEBUG] Cleaning up resources.")