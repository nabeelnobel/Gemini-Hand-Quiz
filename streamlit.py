# streamlit_app.py
import streamlit as st
import cv2
import numpy as np
import time
from hand_quiz import QuizSystem
from gemini_utils import generate_mcqs_from_paragraph

st.set_page_config(page_title="Gemini Hand Quiz", layout="wide")

st.title("🧠 Interactive Hand Quiz Generator")
st.markdown("### Step 1: Enter a paragraph below to generate questions.")

# Input Paragraph
paragraph = st.text_area("📝 Paragraph Input", height=200)

if st.button("✨ Generate Quiz"):
    try:
        with st.spinner("Generating questions using Gemini..."):
            output_path = generate_mcqs_from_paragraph(paragraph)
            st.session_state['quiz'] = QuizSystem(csv_path=output_path)
            st.session_state['run_quiz'] = True
            st.success("Quiz generated successfully! Scroll down to start.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# If quiz is ready to run
if st.session_state.get('run_quiz'):
    st.markdown("### Step 2: Play the quiz using hand gestures!")

    stop = st.button("❌ Stop Quiz", key="stop_quiz_btn")
    frame_placeholder = st.empty()

    while st.session_state['run_quiz'] and not stop:
        frame = st.session_state['quiz'].get_frame()

        if frame is None:
            st.error("Failed to access webcam or quiz ended.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB")
        time.sleep(1 / 15)

    if stop:
        st.session_state['run_quiz'] = False
        st.success("Quiz stopped. Reload the page or input new paragraph.")

    # Show final score and detailed review if quiz is completed
    if st.session_state['quiz'].qNo >= st.session_state['quiz'].qTotal:
        correct = sum(1 for q in st.session_state['quiz'].mcqList if q.answer == q.userAns)
        total = st.session_state['quiz'].qTotal
        score_percent = round((correct / total) * 100, 2)

        st.markdown(f"### ✅ Quiz Completed! Your Score: **{score_percent}%** ({correct}/{total})")

        incorrect = total - correct
        st.markdown(f"""
        - 🟢 Correct: {correct}  
        - 🔴 Incorrect: {incorrect}  
        - 📋 Total Questions: {total}
        """)

        with st.expander("🔍 Review Your Answers"):
            for idx, q in enumerate(st.session_state['quiz'].mcqList, start=1):
                st.markdown(f"**Q{idx}. {q.question}**")
                choices = [q.choice1, q.choice2, q.choice3, q.choice4]
                for i, choice in enumerate(choices, start=1):
                    if i == q.answer and i == q.userAns:
                        st.success(f"✅ {i}. {choice} (Your Answer - Correct)")
                    elif i == q.userAns and i != q.answer:
                        st.error(f"❌ {i}. {choice} (Your Answer - Incorrect)")
                    elif i == q.answer:
                        st.info(f"✔️ {i}. {choice} (Correct Answer)")
                    else:
                        st.write(f"{i}. {choice}")
                st.markdown("---")
