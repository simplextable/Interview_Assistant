import streamlit as st
from openai import OpenAI

st.title("🤖 AI Interview Assistant (GPT-3.5 Turbo)")

# 🔐 Ask for API key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# 🧠 Prompt input
job_title = st.text_input("Enter the job title (e.g., Software Engineer)")

# 🚀 Start interview
if api_key and job_title and st.button("Start Interview"):
    client = OpenAI(api_key=api_key)

    prompt = f"Generate 3 technical or behavioral interview questions for a {job_title} position."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    questions = response.choices[0].message.content.strip().split("\n")
    questions = [q for q in questions if q.strip()]

    st.session_state.questions = questions
    st.session_state.answers = []
    st.session_state.index = 0

# 🗨️ Question-answer flow
if "questions" in st.session_state and st.session_state.index < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.index]
    st.subheader(f"Question {st.session_state.index + 1}")
    st.write(q)

    answer = st.text_area("Your answer:")

    if st.button("Submit Answer"):
        st.session_state.answers.append(answer)
        st.session_state.index += 1

# ✅ Evaluation
elif "questions" in st.session_state and st.session_state.index == len(st.session_state.questions):
    client = OpenAI(api_key=api_key)  # Ensure client is available here too

    full_text = ""
    for i in range(len(st.session_state.questions)):
        full_text += f"Question: {st.session_state.questions[i]}\nAnswer: {st.session_state.answers[i]}\n\n"

    summary_prompt = (
        f"Below are some interview questions and the candidate's responses. "
        f"Please provide an overall evaluation of the candidate's performance in the interview. "
        f"Identify general strengths, weaknesses, and share a brief overall impression:\n\n{full_text}"
    )

    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": summary_prompt}]
    )

    st.success("Interview completed! 📝")
    st.write("### Evaluation:")
    st.write(result.choices[0].message.content)
