import os
import streamlit as st
from huggingface_hub import InferenceClient

#huggingface token (security stored in streamlit secrets)
HF_TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient("meta-llama/Llama-3.1-8B-instruct ",token=HF_TOKEN)

# Initialize session state
if "chat_history" not in st.session_state:
  st.session_state.chat_history = []
if "journal_entries" not in st.session_state:
  st.session_state.journal_entries = []
if "mood" not in st.session_state:
  st.session_state.mood = "😃"

# sidbar:Emoji mood Traker
st.sidebar.header("🧠 Mood Tracker")
mood = st.sidebar.radio("How are you feeling today?",["🙂 Normal","😢 Sad","😤 Angry","🙂‍↔️ Calm","😕 Upset","😎 Cool"])
st.session_state.mood = mood
st.sidebar.write(f"Selected mood : {mood}")

# Tab for chat and Journaling
tab1,tab2 = st.tabs(["💬 Chat","📝 Journal"])
 
# LLAMA response functons with follow-up
def get_wellness_response(user_message,mood):
  system_prompt = (
                  f"You are a compassionate mentel willnese chatbot for students. "
                  f"The student is currently feeling {mood}. "
                  "Detect emotional tone and responnd with empathy, motivation, and relaxation tips. "
                  "After your response, ask a gentle follow-up question to encourage  reflection or consideration of next steps. "
                )
  full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_message}\n<|assistant|>"
  response = client.text_generation(full_prompt, max_new_tokens=300, temperature=0.7 )
  return response.strip()

# 💬 Chat Tab
with tab1:
  st.title("🌱 Student Wellness Chatbot")
  st.markdown("Type how you're feeling. I'm here to support you with empathy and encouragement. ")
   
  user_input = st.text_area("🌝  What'son your mind?",placeholder="e.g.,'I feel anxious about exams'")

  if st.button("send",key="chat_send"):
     if user_input:
         with st.spinner("Thinking with empathy...."):
            bot_response = get_wellness_response(user_input,st.session_state.mood)
            st.session_state.chat_history.append(("You",user_input))
            st.session_state.chat_history.append(("Bot",bot_response))

  # Display chat history
  for sender,message in st.session_state.chat_history:
      st.markdown(f"*{sender}:* {message}")

# 📝 Journal Tab
with tab2:
  st.title("📝 Personal Journal")
  st.markdown("Write freely about your thoughts. This is just for you. ")

  journal_input = st.text_area("Today's reflection",placeholder="Write anything you want to reflect on....")

  if st.button("Save Entry",key="Journal_save"):
     if journal_input:
         st.session_state.journal_entries.append(journal_input)
         st.success("Journal entry saved!")

  if st.session_state.journal_entries:
      st.markdown("### 📚 Your Entries")
      for i,entry in enumerate(st.session_state.journal_entries,1):
         st.markdown(f"*Entry{i}:*{entry}")