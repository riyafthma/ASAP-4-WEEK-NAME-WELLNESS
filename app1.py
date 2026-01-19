import os
import streamlit as st
from huggingface_hub import InferenceClient
# Hugging Face token (stored in secrets)
HF_TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)
# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Normal"
# Sidebar: Emoji Mood Tracker
st.sidebar.header("🧠 Mood Tracker")

mood = st.sidebar.radio(
    "How are you feeling today?",
    ["🙂 Normal", "😢 Sad", "😤 Angry", "🙂‍↔️ Calm", "😕 Upset", "😎 Cool"]
)

st.session_state.mood = mood
st.sidebar.write(f"Selected mood : {mood}")
# Tabs for Chat and Journal
tab1, tab2 = st.tabs(["💬 Chat", "📝 Journal"])
# Emotion Detection (NEW – simple & clear)
def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in ["happy", "good", "great", "excited"]):
        return "😊 Happy"
    elif any(word in text for word in ["sad", "down", "cry", "lonely"]):
        return "😢 Sad"
    elif any(word in text for word in ["angry", "mad", "annoyed"]):
        return "😠 Angry"
    elif any(word in text for word in ["stress", "exam", "anxious", "worried"]):
        return "😟 Anxious"
    elif any(word in text for word in ["calm", "relaxed", "peaceful"]):
        return "😌 Calm"
    else:
        return "😐 Neutral"
# LLAMA response function
def get_wellness_response(user_message, emotion):
    system_prompt = (
        f"You are a compassionate mental wellness chatbot for students. "
        f"The detected emotion is {emotion}. "
        "Respond with empathy, motivation, and simple relaxation tips. "
        "After your response, ask a gentle follow-up question."
    )

    full_prompt = f"""
<|system|>
{system_prompt}
<|user|>
{user_message}
<|assistant|>
"""

    response = client.text_generation(
        full_prompt,
        max_new_tokens=300,
        temperature=0.7
    )

    return response.strip()
# 💬 Chat Tab
with tab1:
    st.title("🌱 Student Wellness Chatbot")
    st.markdown("Type how you're feeling. I'm here to support you.")

    user_input = st.text_area(
        "🌝 What's on your mind?",
        placeholder="e.g., I feel anxious about exams"
    )

    if st.button("Send", key="chat_send"):
        if user_input.strip():
            with st.spinner("Thinking with empathy..."):

                detected_emotion = detect_emotion(user_input)

                bot_response = get_wellness_response(
                    user_input,
                    detected_emotion
                )

                st.session_state.chat_history.append(
                    ("You", f"{user_input}\n\n🧠 Detected Emotion: {detected_emotion}")
                )
                st.session_state.chat_history.append(
                    ("Bot", bot_response)
                )

    # Display chat history
    for sender, message in st.session_state.chat_history:
        st.markdown(f"*{sender}:* {message}")

# 📝 Journal Tab
with tab2:
    st.title("📝 Personal Journal")
    st.markdown("Write freely about your thoughts. This is just for you.")

    journal_input = st.text_area(
        "Today's reflection",
        placeholder="Write anything you want to reflect on..."
    )

    if st.button("Save Entry", key="journal_save"):
        if journal_input.strip():
            st.session_state.journal_entries.append(journal_input)
            st.success("Journal entry saved!")

    if st.session_state.journal_entries:
        st.markdown("### 📚 Your Entries")
        for i, entry in enumerate(st.session_state.journal_entries, 1):
            st.markdown(f"*Entry {i}:* {entry}")