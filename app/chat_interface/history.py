import streamlit as st
from langchain_core.messages import AIMessage
import re
import base64
from PIL import Image
from io import BytesIO


# dev: correctly show images in chat

# --- Visualization Functions ---
def display_base64_image_or_text(received_text):
    """
    Parses the input text to check for Base64-encoded images. If found, decodes and displays the image.
    Otherwise, displays the text as is.

    Args:
        received_text (str): Text potentially containing a Base64-encoded image.
    """
    base64_pattern = r"data:image\/png;base64,(.+)"
    match = re.search(base64_pattern, received_text)

    if match:
        try:
            # Extract and decode Base64 string
            base64_string = match.group(1)
            base64_string += "=" * ((4 - len(base64_string) % 4) % 4)  # Add padding if missing
            image_bytes = base64.b64decode(base64_string)
            image = Image.open(BytesIO(image_bytes))
            st.image(image, use_column_width=True)
        except Exception as e:
            st.error(f"Error displaying image: {e}")
            st.write(received_text)  # Fallback to displaying text
    else:
        st.write(received_text)


# --- Chat Display Functions ---
def render_chat_message(message):
    """
    Renders a single chat message in the Streamlit chat UI.

    Args:
        message: A message object (HumanMessage or AIMessage).
    """
    role = "Assistant" if isinstance(message, AIMessage) else "User"

    with st.chat_message(role):
        display_base64_image_or_text(message.content)


def render_chat_history(show_latest=True):
    """
    Displays the chat history for the current thread.

    Args:
        show_latest (bool): If True, shows the latest message; otherwise, shows all except the last message.
    """
    if st.session_state.thread_data:
        chat_history = st.session_state.thread_data[st.session_state.current_thread].get("chat_history", [])
        messages_to_display = chat_history if show_latest else chat_history[:-1]
        print("messages_to_display:")
        print(messages_to_display)
        for message in messages_to_display:
            render_chat_message(message)


# --- Helper Functions ---
def add_padding_to_base64_string(base64_string):
    """
    Adds padding to a Base64 string to make its length a multiple of 4.

    Args:
        base64_string (str): The Base64 string to pad.

    Returns:
        str: The padded Base64 string.
    """
    padding_length = (4 - len(base64_string) % 4) % 4
    return base64_string + ("=" * padding_length)


def update_chat_history():
    pass


def get_chat_history():
    thread_data = st.session_state.thread_data
    current_thread_name = st.session_state.current_thread
    chat_history = thread_data[current_thread_name].get("chat_history", [])
    return chat_history