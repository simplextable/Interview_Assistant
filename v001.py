import streamlit as st
import openai

openai.api_key = "WRITE HERE API KEY"

st.title("🤖 AI Görüşme Asistanı (GPT-3.5 Turbo)")

job_title = st.text_input("Pozisyon Gir (Örn: Yazılım Mühendisi)")

if job_title and st.button("Görüşmeye Başla"):
    prompt = f"{job_title} için 3 adet teknik veya davranışsal iş görüşmesi sorusu yaz."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    questions = response.choices[0].message.content.strip().split("\n")
    questions = [q for q in questions if q.strip()]

    st.session_state.questions = questions
    st.session_state.answers = []
    st.session_state.index = 0

if "questions" in st.session_state and st.session_state.index < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.index]
    st.subheader(f"Soru {st.session_state.index + 1}")
    st.write(q)

    answer = st.text_area("Cevabınızı yazın:")

    if st.button("Cevabı Gönder"):
        st.session_state.answers.append(answer)
        st.session_state.index += 1

elif "questions" in st.session_state and st.session_state.index == len(st.session_state.questions):
    # Tüm cevaplar alındıysa, özetle
    full_text = ""
    for i in range(len(st.session_state.questions)):
        full_text += f"Soru: {st.session_state.questions[i]}\nCevap: {st.session_state.answers[i]}\n\n"

    summary_prompt = f"Aşağıda bir iş görüşmesindeki sorular ve adayın cevapları var. Bunları değerlendir. Güçlü yönlerini, zayıf yönlerini ve genel izlenimi özetle:\n\n{full_text}"

    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": summary_prompt}]
    )

    st.success("Görüşme tamamlandı! 📝")
    st.write("### Değerlendirme:")
    st.write(result.choices[0].message.content)