import os
import streamlit as st
from huggingface_hub import InferenceClient

# Hugging Face Configuration
HF_TOKEN = st.secrets["HF_TOKEN"]

client = InferenceClient(
    model="meta-llama/Llama-3.1-8B",
    token=HF_TOKEN
)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Calm"

# Emotion Mapping
EMOTIONS = {
    "😄 Happy": "positive, high energy",
    "🤩 Excited": "positive, very high energy",
    "🙂 Calm": "positive, balanced energy",
    "😌 Relaxed": "positive, low energy",
    "😇 Content": "positive, peaceful energy",
    "😢 Sad": "negative, low energy",
    "😔 Lonely": "negative, low energy",
    "😕 Confused": "neutral, medium energy",
    "😬 Nervous": "negative, medium energy",
    "😤 Angry": "negative, high energy",
    "😟 Stressed": "negative, medium-high energy",
    "😴 Tired": "neutral, very low energy",
    "😐 Bored": "neutral, low energy",
    "😲 Surprised": "neutral, high energy",
    "😎 Confident": "positive, high energy",
    "💛 Grateful": "positive, medium energy",
    "💪 Motivated": "positive, high energy",
    "😖 Frustrated": "negative, medium energy",
    "😞 Disappointed": "negative, low energy",
    "😳 Embarrassed": "negative, medium energy",
    "😡 Furious": "negative, very high energy",
    "😌 Peaceful": "positive, low energy",
    "😕 Anxious": "negative, medium energy"

}

# Sidebar: Mood Tracker
st.sidebar.header("💆🏻Quick Emotional Check-In")

mood = st.sidebar.selectbox(
    "What's your mood right now?",
    list(EMOTIONS.keys())
)

st.session_state.mood = mood
st.sidebar.write(f"*Current mood:* {mood}")

# Tabs
tab_chat, tab_journal = st.tabs(["💬 Chat Support", "📝 Personal Journal"])

# LLM Response Function
def get_wellness_response(user_message: str, mood: str) -> str:
    emotion_context = EMOTIONS.get(mood, "neutral")

    system_prompt = (
        "You are a kind and emotionally intelligent wellness chatbot for students. "
        f"The student is feeling {mood}, which reflects {emotion_context}. "
        "Respond with empathy, emotional validation, and gentle encouragement. "
        "If appropriate, suggest one simple calming or grounding idea "
        "(like breathing, short breaks, or positive reflection). "
        "End with ONE gentle follow-up question."
    )

    full_prompt = (
        f"<|system|>\n{system_prompt}\n"
        f"<|user|>\n{user_message}\n"
        f"<|assistant|>"
    )

    response = client.text_generation(
        full_prompt,
        max_new_tokens=150,
        temperature=0.7
    )

    return response.strip()

# 💬 Chat Tab
with tab_chat:
    st.title("🫂 Student Emotional Wellness Chatbot")
    st.markdown(
        "This is a safe place to share your thoughts freely—your feelings truly matter ✨"
    )

    user_input = st.text_area(
        "What’s been on your mind today?",
        placeholder="For example: I feel stressed about assignments"
    )

    if st.button("Send", key="chat_send"):
        if user_input.strip():
            with st.spinner("Listening and responding thoughtfully..."):
                bot_reply = get_wellness_response(
                    user_input,
                    st.session_state.mood
                )

                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", bot_reply))

    for sender, message in st.session_state.chat_history:
        st.markdown(f"*{sender}:* {message}")

# 📝 Journal Tab
with tab_journal:
    st.title("Mood Log 🗒️🖋️")
    st.markdown(
        "Write freely 🤸🏻 No judgment... Just your thoughts and feelings."
    )

    journal_input = st.text_area(
        "Today's Mood",
        placeholder="What happened today? How did it make you feel?"
    )

    if st.button("Save Entry", key="journal_save"):
        if journal_input.strip():
            st.session_state.journal_entries.append(journal_input)
            st.success("✅ Your journal entry has been saved.")

    if st.session_state.journal_entries:
        st.markdown("### 📚 Previous Reflections")
        for i, entry in enumerate(st.session_state.journal_entries, start=1):
            st.markdown(f"*Entry {i}:* {entry}")