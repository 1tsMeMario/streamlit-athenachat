import time
import json
from pathlib import Path

import streamlit as st
from openai import OpenAI

BASE_DIR = Path(__file__).parent
PERSONAS_PATH = BASE_DIR / "personas/all.json"
CONVERSATIONS_DIR = BASE_DIR / "data"
CONVERSATIONS_FILE = CONVERSATIONS_DIR / "conversations.json"
CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_MODEL = "darkidol-llama-3.1-8b-instruct-1.2-uncensored"
AVAILABLE_MODELS = ["darkidol-llama-3.1-8b-instruct-1.2-uncensored", "hermes-3-llama-3.2-3b", "llama-3-8b-lexi-uncensored"]
BOT_AVATAR = "https://files.catbox.moe/x3kr0e.png"
USER_AVATAR = "https://files.catbox.moe/u2y7vf.jpg"

def save_conversations():
    with open(CONVERSATIONS_FILE, 'w') as f:
        json.dump(st.session_state.conversations, f, indent=2)

def load_conversations():
    if CONVERSATIONS_FILE.exists():
        with open(CONVERSATIONS_FILE, 'r') as f:
            st.session_state.conversations = json.load(f)
            return
    st.session_state.conversations = []

def load_personas(path: Path):
    if not path.exists():
        return []
    personas = json.loads(path.read_text())
    return personas


def save_personas(personas, path: Path):
    with open(path, 'w') as f:
        json.dump(personas, f, indent=2)


client = OpenAI(api_key="None", base_url="https://l7crq0c7-1234.use.devtunnels.ms/v1")

if 'conversations' not in st.session_state:
    load_conversations()

if 'personas' not in st.session_state:
    st.session_state.personas = load_personas(PERSONAS_PATH)

if 'model_version' not in st.session_state:
    st.session_state.model_version = DEFAULT_MODEL

if 'selected_convo' not in st.session_state:
    st.session_state.selected_convo = next(iter(st.session_state.conversations), None)

if 'message_text' not in st.session_state:
    st.session_state['message_text'] = ''

if 'current_persona' not in st.session_state:
    st.session_state['current_persona'] = ""

if 'current_persona_name' not in st.session_state:
    st.session_state['current_persona_name'] = ""

def send_message(convo_id, message_text):
    print("Sending message")
    print(message_text)
    if message_text.strip():
        user_message = {"role": "user", "content": message_text}
        st.session_state.conversations[convo_id].append(user_message)

        messages = []
        if st.session_state.current_persona:
            system_message = {"role": "system", "content": st.session_state.current_persona}
            messages.append(system_message)
        messages.extend(st.session_state.conversations[convo_id])

        try:
            print(messages)
            print("Inferencing with model: ", st.session_state.model_version)
            with st.spinner("AI is typing..."):
                completion = client.chat.completions.create(
                    model=st.session_state.model_version,
                    messages=messages
                )
            ai_content = completion.choices[0].message.content.strip()

            ai_message = {
                "role": "assistant",
                "content": ai_content
            }
            st.session_state.conversations[convo_id].append(ai_message)
            print("AI Response:", ai_content)
        except Exception as e:
            st.error(f"An error occurred: {e}")

        save_conversations()
        st.session_state.message_text = ''


with st.sidebar:
    st.title("Conversations")

    if st.button("New Conversation"):
        new_convo_id = str(int(time.time()))
        st.session_state.conversations[new_convo_id] = []
        st.session_state.selected_convo = new_convo_id
        save_conversations()

    st.markdown("---")
    st.header("Rename Conversation")
    new_convo_name = st.text_input("New Conversation Name", value=st.session_state.selected_convo)
    if st.button("Rename Conversation"):
        if new_convo_name.strip() == "":
            st.error("Please enter a valid name for the conversation.")
        elif new_convo_name in st.session_state.conversations:
            st.error("A conversation with this name already exists.")
        else:
            st.session_state.conversations[new_convo_name] = st.session_state.conversations.pop(st.session_state.selected_convo)
            st.session_state.selected_convo = new_convo_name
            save_conversations()
            st.success(f"Conversation renamed to '{new_convo_name}' successfully.")

    st.markdown("---")
    st.header("Conversation Actions")

    if st.button("Save Conversation"):
        save_conversations()
        st.success("Conversation saved successfully.")

    if st.button("Delete Conversation"):
        if st.session_state.selected_convo:
            del st.session_state.conversations[st.session_state.selected_convo]
            st.session_state.selected_convo = next(iter(st.session_state.conversations), None) if st.session_state.conversations else None
            save_conversations()
            st.success("Conversation deleted successfully.")
        else:
            st.error("No conversation selected to delete.")

    if st.button("Clear Conversation"):
        if st.session_state.selected_convo:
            st.session_state.conversations[st.session_state.selected_convo] = []
            save_conversations()
            st.success("Conversation cleared successfully.")
        else:
            st.error("No conversation selected to clear.")

    if st.session_state.conversations:
        st.selectbox(
            "Select a Conversation",
            options=list(st.session_state.conversations.keys()),
            format_func=lambda x: f"{x}",
            key="selected_convo"
        )

    st.markdown("---")
    st.header("Model Selection")

    selected_model = st.selectbox(
        "Select Model",
        options=AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(st.session_state.model_version) if st.session_state.model_version in AVAILABLE_MODELS else 0
    )
    st.session_state.model_version = selected_model

    st.markdown("---")
    st.header("Persona Management")

    if st.button("New Persona"):
        st.session_state.current_persona = ""
        st.session_state.current_persona_name = ""

    persona_names = [persona['name'] for persona in st.session_state.personas]
    selected_persona = st.selectbox(
        "Select a Persona",
        options=["__Select Persona__"] + persona_names
    )

    if selected_persona != "__Select Persona__":
        for persona in st.session_state.personas:
            if persona['name'] == selected_persona:
                st.session_state.current_persona = persona['persona']
                st.session_state.current_persona_name = persona['name']
                break

    persona_text = st.text_area(
        "Persona (System Prompt)",
        value=st.session_state.get('current_persona', ''),
        height=200
    )
    st.session_state.current_persona = persona_text

    persona_name_input = st.text_input(
        "Persona Name",
        value=st.session_state.get('current_persona_name', '')
    )
    st.session_state.current_persona_name = persona_name_input

    if st.button("Save Persona"):
        if not st.session_state.current_persona_name.strip():
            st.error("Please provide a name for the persona.")
        elif not st.session_state.current_persona.strip():
            st.error("Persona content cannot be empty.")
        else:
            existing = next((p for p in st.session_state.personas if p['name'] == st.session_state.current_persona_name), None)
            if existing:
                existing['persona'] = st.session_state.current_persona
                st.success(f"Persona '{st.session_state.current_persona_name}' updated successfully!")
            else:
                new_persona = {
                    "name": st.session_state.current_persona_name,
                    "persona": st.session_state.current_persona
                }
                st.session_state.personas.append(new_persona)
                st.success(f"Persona '{st.session_state.current_persona_name}' added successfully!")
            save_personas(st.session_state.personas, PERSONAS_PATH)

st.title('Athena Chat v1.0.1')

if st.session_state.selected_convo is not None:
    message = st.chat_input("Enter your message here:")
    if message:
        send_message(st.session_state.selected_convo, message)

    if st.session_state.conversations[st.session_state.selected_convo]:
        for message in st.session_state.conversations[st.session_state.selected_convo]:
            role = message["role"]
            content = message["content"]
            if role == "assistant":
                with st.chat_message(name=role.lower(), avatar=BOT_AVATAR):
                    st.markdown(content)
            else:
                with st.chat_message(name=role.lower(), avatar=USER_AVATAR):
                    st.markdown(content)
else:
    st.write("Welcome to Athena Chat v1.0.1. Select or create a conversation to start chatting.")
