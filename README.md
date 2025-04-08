
# 🧠 Gemini Hand Quiz

**Gemini Hand Quiz** is an interactive, AI-powered quiz system that combines Google Gemini's generative AI with real-time hand gesture recognition using a webcam (OpenCV). It allows users to generate multiple-choice questions from any paragraphs and answer them using finger gestures SO no clicks needed!

---

## 🚀 Features

- ✅ Generate MCQs from any paragraph using **Google Gemini (via API)**
- ✋ Answer quiz questions using **hand tracking** and **gesture-based selection**
- 📷 Real-time webcam interface powered by **OpenCV** and **cvzone**
- 🌐 Interactive user interface using **Streamlit**

---

## 🧩 How It Works

1. **Text to Quiz**: Users input a paragraph. The app uses Gemini to generate exactly 4 MCQs in a raw CSV format.
2. **Gesture Quiz Game**: Using hand gestures (pinching motion), users can select answers. Progress is visualized, and a final score is shown.
3. **Review**: At the end of the quiz, users can see a breakdown of correct and incorrect answers.

---

## 🛠️ Project Structure

```plaintext
.
├── gemini_utils.py      # Generates MCQs using Gemini API
├── hand_quiz.py         # Core logic for hand-tracked quiz interaction
├── streamlit_app.py     # Streamlit interface for quiz generation and play
├── output_mcqs.csv      # Generated MCQs (auto-generated after quiz creation)
└── README.md            # This file
```

---

## 📦 Requirements

Install dependencies using pip

Ensure you have a `.env` file with your Gemini API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

---

## 🧪 How to Run

1. Run the Streamlit app:
   ```bash
   streamlit run streamlit.py
   ```

2. In the web interface:
   - Enter a paragraph and click **"Generate Quiz"**
   - Scroll down and interact with the quiz using hand gestures
   - See your score and review your answers!

---

## 🎯 Use Cases

- Educational tools and interactive learning
- AI-enhanced teaching aids
- Fun demo for hand-tracking and AI integration

---

## 📌 Notes

- Ensure your webcam is functional.
- Make sure there’s good lighting and clear visibility of your hand for accurate gesture detection.
- Each quiz consists of exactly 4 questions per Gemini API constraints.

---

## 👤 Author

**Nabeel Adriansyah**  
📧 *Reach out if you want to collaborate on educational tech projects!*