
import streamlit as st
from pptx import Presentation
import json
import os
from datetime import date
from pypdf import PdfReader
from ai_engine import ask_ai, ask_ai_stream


# ---------- PAGE SETTINGS ----------
st.set_page_config(
    page_title="MEXA.COM | AI LEARNER",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------- CHAT MEMORY ----------
MEMORY_FILE = "chat_memory.json"


def load_chat_history():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_chat_history():
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            st.session_state.chat_history,
            file,
            ensure_ascii=False,
            indent=2
        )


if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()


# ---------- MEXA.COM BEAUTIFUL UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff5fa, #fce7f3, #fdf2f8);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fbcfe8, #fce7f3);
    border-right: 2px solid #f9a8d4;
}

h1, h2, h3 {
    color: #9d174d;
}

.stButton > button {
    background-color: #ec4899;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 9px 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #be185d;
    color: white;
    border: 1px solid #f9a8d4;
}

[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 14px;
    border: 1px solid #fbcfe8;
    padding: 12px;
}

[data-testid="stChatInput"] {
    border-radius: 14px;
}

/* MEXA.COM chat improvements */
[data-testid="stChatMessage"] {
    background: #24211b;
    border: 1px solid #80652c;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #c9a64c;
    border-radius: 14px;
}

[data-testid="stChatInput"] textarea {
    color: #f5e6bd;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #e0bd62;
}

</style>
""", unsafe_allow_html=True)


# ---------- MEXA.COM PLAN SETTINGS ----------
if "plan" not in st.session_state:
    st.session_state.plan = "Free"

today = date.today().isoformat()

if st.session_state.get("usage_date") != today:
    st.session_state.usage_date = today
    st.session_state.daily_chat_count = 0

if "daily_chat_count" not in st.session_state:
    st.session_state.daily_chat_count = 0

daily_limit = 100 if st.session_state.plan == "Premium" else 10

# ---------- 🎨 COLOR SETTINGS ----------
# Change colors here whenever you want!
# Use CSS color names like "black", "gold", "white", "pink"
# You can also use HEX colors like "#D8B56D".


# ---------- COLOR SETTINGS 🎨 ----------
PAGE_BACKGROUND = "black"
SIDEBAR_BACKGROUND = "black"
CARD_BACKGROUND = "darkslategray"

HEADING_COLOR = "lightgoldenrodyellow"
BUTTON_BACKGROUND = "lightgoldenrodyellow"
BUTTON_TEXT_COLOR = "black"

TEXT_COLOR = "ivory"
BORDER_COLOR = "goldenrod"

INPUT_BACKGROUND = "darkslategray"
PLACEHOLDER_COLOR = "silver"

# Special typing bar colors

CHAT_INPUT_BACKGROUND = "black"
CHAT_INPUT_TEXT = "black"
CHAT_INPUT_BORDER = "goldenrod"
CHAT_INPUT_PLACEHOLDER = "black"





# ---------- BEAUTIFUL BLACK & GOLD UI DESIGN ----------
st.markdown("""
<style>

/* Main page background */
.stApp {
    background: linear-gradient(135deg, #111111 0%, #1C1C1C 55%, #242019 100%);
    color: #F5F1E8;
}

/* Main content area */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Main headings */
h1, h2, h3 {
    color: #D8B56D !important;
    font-weight: 800 !important;
}

p, label, .stMarkdown, .stCaption {
    color: #F0EDE5;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0A0A 0%, #292319 100%);
    border-right: 1px solid #806A3E;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #D8B56D !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #F5F1E8;
}

/* Radio selection */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: #211F1B;
    border-radius: 10px;
    padding: 8px;
    margin-bottom: 5px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, #E4C47A, #B8954F) !important;
    color: #17130B !important;
    border: 1px solid #E4C47A !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.2rem;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}

/* Button hover */
.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #F5DDA0, #D8B56D) !important;
    color: #000000 !important;
    border-color: #F5DDA0 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(216, 181, 109, 0.2);
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea {
    background-color: #252525 !important;
    color: #FFFFFF !important;
    border: 1px solid #806A3E !important;
    border-radius: 10px !important;
}

/* Input placeholders */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #BDB5A6 !important;
}

/* Dropdowns and select boxes */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #252525 !important;
    color: #FFFFFF !important;
    border-color: #806A3E !important;
    border-radius: 10px !important;
}

/* Dropdown text */
.stSelectbox div[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: #242424 !important;
    border: 1px solid #66532F !important;
    border-radius: 16px !important;
    padding: 14px !important;
    margin-bottom: 12px !important;
}


/* Chat input and bottom white strip */
div[data-testid="stBottom"],
div[data-testid="stBottom"] > div,
div[data-testid="stBottom"] > div > div {
    background: black !important;
    background-color: black !important;
    background-image: none !important;
    box-shadow: none !important;
}

/* Chat input box */
div[data-testid="stChatInput"] {
    background: darkslategray !important;
    background-color: darkslategray !important;
    border: 2px solid goldenrod !important;
    border-radius: 16px !important;
}

/* Text typed inside the box */
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    background-color: transparent !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    caret-color: white !important;
}

/* Placeholder text */
div[data-testid="stChatInput"] textarea::placeholder {
    color: silver !important;
    -webkit-text-fill-color: silver !important;
    opacity: 1 !important;
}


/* Forms and cards */
div[data-testid="stForm"] {
    background: #202020 !important;
    padding: 22px !important;
    border: 1px solid #806A3E !important;
    border-radius: 18px !important;
}

/* Radio buttons and checkboxes */
.stRadio label,
.stCheckbox label {
    color: #F5F1E8 !important;
}

/* Dividers */
hr {
    border-color: #66532F !important;
}

/* Success messages */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #151515;
}

::-webkit-scrollbar-thumb {
    background: #806A3E;
    border-radius: 10px;
}

/* Footer */
.stCaption {
    color: #D8B56D !important;
}

</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.title("📚 MEXA.COM")
st.write("Your Intelligence. Your Assistant")
st.divider()


# ---------- SIDEBAR ----------
st.sidebar.title("🎓 Study Dashboard")

page = st.sidebar.radio(
    "Choose a feature:",
    [
        "💬 AI Chat",
        "📝 Quiz Generator",
        "📖 Notes Generator",
        "📄 PDF Study Assistant",
        "🎞️ PowerPoint Study Assistant",
        "✨ Smart Study Mode",
    ]
)


st.sidebar.divider()
st.sidebar.caption("Powered by Groq AI")
st.sidebar.caption("Model: Llama 3.3 70B")

# ---------- MEXA.COM PLAN SELECTION ----------
st.sidebar.divider()
st.sidebar.subheader("💎 Choose Your Plan")

selected_plan = st.sidebar.radio(
    "Your Plan",
    ["Free", "Premium"],
    index=0
)
if "plan" not in st.session_state:
    st.session_state.plan = "Free"
if selected_plan != st.session_state.plan:
    st.session_state.plan = selected_plan
    st.rerun()

if st.session_state.plan == "Free":
    st.sidebar.info("Free Plan: 10 chats per day")
else:
    st.sidebar.success("Premium Plan: 100 chats per day")
    st.sidebar.caption("Payment setup coming soon!")


# ---------- AI CHAT ----------
if page == "💬 AI Chat":

    st.subheader("💬 ASK QUESTIONS")
    st.write("Ask questions and learn topics in easy words.")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        save_chat_history()
        st.rerun()

    # Show old messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    # Check daily chat limit
    limit_reached = (
        st.session_state.daily_chat_count >= daily_limit
    )

    if limit_reached:
        st.warning(
            "You have reached your daily chat limit. "
            "Upgrade to Premium for more messages!"
        )

    user_message = st.chat_input(
        "Daily limit reached"
        if limit_reached
        else "Ask your study question here...",
        disabled=limit_reached
    )

    if user_message:
        try:
            with st.spinner("MEXA is thinking..."):

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are MEXA.COM, a smart, friendly and helpful AI assistant. "
                            "Understand the user's question and answer it directly. "
                            "Reply in the same language as the user. If the user writes "
                            "in Roman Urdu, reply in natural Roman Urdu. If the user "
                            "writes in English, reply in clear English. "
                            "For greetings, respond naturally and briefly. "
                            "For study questions, explain concepts in easy words with "
                            "correct examples. For coding questions, give working code "
                            "and explain important parts. Use headings and bullet points "
                            "when helpful. Keep simple answers short and detailed answers "
                            "complete. Do not give unrelated suggestions. "
                            "Do not invent facts. Be warm, respectful and patient. "
                            "Your name is MEXA.COM."
                        )
                    },
                    *st.session_state.chat_history[-10:],
                    {"role": "user", "content": user_message}
                ]

                stream = ask_ai_stream(messages)

                def response_generator():
                    for chunk in stream:
                        content = chunk.choices[0].delta.content
                        if content:
                            yield content

                answer = st.write_stream(response_generator())
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_message}
                )

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )

                st.session_state.daily_chat_count += 1
                save_chat_history()
        except Exception as e:
            st.error(f"AI error: {e}")
     
# ---------- QUIZ GENERATOR ----------
elif page == "📝 Quiz Generator":

    st.subheader("📝 Interactive AI Quiz")
    st.write("Generate MCQs, select answers, and check your score.")

    with st.form("quiz_form"):
        subject = st.text_input(
            "Subject",
            placeholder="e.g. Data Structures"
        )
        topic = st.text_input(
            "Topic",
            placeholder="e.g. Arrays and Pointers"
        )
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"]
        )
        number = st.selectbox(
            "Number of MCQs",
            [3, 5, 10]
        )

        generate_quiz = st.form_submit_button(
            "✨ Generate Quiz"
        )

    if generate_quiz:
        if not subject.strip() or not topic.strip():
            st.warning("Please enter both subject and topic.")
        else:
            prompt = f"""
Create exactly {number} MCQs about {topic}
for the subject {subject}.
Difficulty: {difficulty}.

Return ONLY a valid JSON array.
Each item must have these keys:
"question": question text,
"options": a list of exactly four options,
"answer": the exact text of the correct option,
"explanation": a short explanation.

Do not add markdown fences or text outside the JSON.
Make sure every answer exactly matches one option.
"""

            try:
                import json

                with st.spinner("AI is creating your quiz..."):
                    result = ask_ai(
                        prompt,
                        "You create educational quizzes. "
                        "Return valid JSON only. Ensure accuracy."
                    )

                # Extract JSON if the AI adds extra text
                start = result.find("[")
                end = result.rfind("]")

                if start == -1 or end == -1:
                    raise ValueError("AI did not return a valid quiz.")

                questions = json.loads(result[start:end + 1])

                if not questions:
                    raise ValueError("The quiz is empty.")

                st.session_state["interactive_questions"] = questions
                st.session_state["quiz_selections"] = {}
                st.session_state["quiz_submitted"] = False

            except Exception as e:
                st.error(f"Quiz creation failed: {e}")

    questions = st.session_state.get("interactive_questions", [])

    if questions:
        st.divider()
        st.markdown("### 🎯 Answer the Questions")

        if not st.session_state.get("quiz_submitted", False):

            with st.form("answer_quiz_form"):

                selections = {}

                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i + 1}. {q['question']}**")

                    options = q.get("options", [])

                    if len(options) != 4:
                        st.warning(f"Question {i + 1} has invalid options.")
                        continue

                    selections[i] = st.radio(
                        "Choose your answer:",
                        options,
                        key=f"answer_{i}"
                    )

                    st.write("")

                submitted = st.form_submit_button("✅ Submit Quiz")

            if submitted:
                st.session_state["quiz_selections"] = selections
                st.session_state["quiz_submitted"] = True
                st.rerun()

        else:
            selections = st.session_state["quiz_selections"]
            score = 0

            for i, q in enumerate(questions):
                chosen = selections.get(i)
                correct = q.get("answer", "")

                st.markdown(f"**Q{i + 1}. {q['question']}**")

                if chosen == correct:
                    score += 1
                    st.success(f"Correct! {correct}")
                else:
                    st.error(f"Your answer: {chosen or 'Not answered'}")
                    st.info(f"Correct answer: {correct}")

                st.write(f"Explanation: {q.get('explanation', 'No explanation provided.')}")
                st.divider()

            st.subheader(f"🏆 Your Score: {score}/{len(questions)}")

            if st.button("🔄 Try Another Quiz"):
                st.session_state["interactive_questions"] = []
                st.session_state["quiz_selections"] = {}
                st.session_state["quiz_submitted"] = False
                st.rerun()



# ---------- NOTES GENERATOR ----------
elif page == "📖 Notes Generator":

    st.subheader("📖 AI Notes Generator")
    st.write("Generate easy notes to help you prepare for exams.")

    with st.form("notes_form"):
        subject = st.text_input(
            "Subject",
            placeholder="e.g. Computer Networks"
        )

        topic = st.text_input(
            "Topic",
            placeholder="e.g. Types of Networks"
        )

        note_style = st.selectbox(
            "Notes Style",
            [
                "Short Exam Notes",
                "Detailed Notes",
                "Beginner-Friendly Explanation"
            ]
        )

        generate_notes = st.form_submit_button(
            "✨ Generate Notes"
        )

    if generate_notes:
        if not subject.strip() or not topic.strip():
            st.warning("Please enter both subject and topic.")
        else:
            prompt = f"""
Create study notes for the following:

Subject: {subject}
Topic: {topic}
Style: {note_style}

Include:
1. A simple introduction.
2. Important definitions.
3. Main concepts in headings and bullet points.
4. Easy examples.
5. Important exam points.
6. A short summary.

Use simple English and keep the notes relevant to the topic.
"""

            try:
                with st.spinner("Preparing your notes..."):
                    notes = ask_ai(
                        prompt,
                        "You are a helpful teacher who creates "
                        "clear, organized and beginner-friendly study notes."
                    )

                st.session_state["latest_notes"] = notes
                st.session_state["notes_subject"] = subject
                st.session_state["notes_topic"] = topic

            except Exception as e:
                st.error(f"Could not generate notes: {e}")

    if st.session_state.get("latest_notes"):
        st.divider()
        st.markdown("### Your Study Notes")
        st.markdown(st.session_state["latest_notes"])

        st.download_button(
            "⬇️ Download Notes",
            data=st.session_state["latest_notes"],
            file_name="study_notes.txt",
            mime="text/plain"
        )


# ---------- FOOTER ----------
st.divider()
st.caption("learner.com| Local AI Study Assistant")



# ---------- PDF STUDY ASSISTANT ----------
if page == "📄 PDF Study Assistant":

    st.subheader("📚 PDF Study Assistant")

    uploaded_pdf = st.file_uploader(
        "Upload your PDF file",
        type=["pdf"],
        key="study_pdf"
    )

    if uploaded_pdf is not None:
        if uploaded_pdf.size == 0:
            st.error("This PDF file is empty. Please upload another PDF.")
        else:
            try:
                uploaded_pdf.seek(0)
                reader = PdfReader(uploaded_pdf)

                pdf_text = "\n".join(
                    p.extract_text() or ""
                    for p in reader.pages
                )

                if not pdf_text.strip():
                    st.warning("No readable text found in this PDF.")
                else:
                    st.session_state["pdf_text"] = pdf_text
                    st.session_state["pdf_name"] = uploaded_pdf.name

                    st.success("PDF uploaded successfully! 🎉")
                    st.write("Total pages:", len(reader.pages))

                    with st.expander("Preview PDF Text"):
                        st.write(pdf_text[:3000])

            except Exception as e:
                st.error(f"Could not read PDF: {e}")

    if st.session_state.get("pdf_text", "").strip():
        st.markdown("---")
        st.subheader("💬 Ask Questions from Your PDF")

        pdf_question = st.text_input(
            "Write your question about the PDF:",
            key="pdf_question"
        )

        
        if st.button("✨ Get Answer", key="pdf_answer_button"):
            if pdf_question.strip():
                try:
                    with st.spinner("MEXA.COM is reading your PDF..."):

                        system_message = (
                            "Answer using the provided PDF text. "
                            "Use simple words. If the answer is "
                            "missing, say so clearly."
                        )

                        prompt = (
                            "PDF TEXT:\n"
                            + st.session_state["pdf_text"][:12000]
                            + "\n\nQUESTION:\n"
                            + pdf_question
                        )

                        answer = ask_ai(prompt, system_message)

                    st.markdown("### 🌷 MEXA.COM's Answer")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please write a question about your PDF.")


# ---------- POWERPOINT STUDY ASSISTANT ----------
elif page == "🎞️ PowerPoint Study Assistant":

    st.subheader("🎞️ PowerPoint Study Assistant")

    uploaded_pptx = st.file_uploader(
        "Upload your PowerPoint slides",
        type=["pptx"],
        key="study_pptx"
    )

    if uploaded_pptx is not None:
        try:
            presentation = Presentation(uploaded_pptx)
            slides_text = []

            for slide_number, slide in enumerate(
                presentation.slides, start=1
            ):
                slide_content = []

                for shape in slide.shapes:
                    if shape.has_text_frame and shape.text.strip():
                        slide_content.append(shape.text.strip())

                    if shape.has_table:
                        for row in shape.table.rows:
                            slide_content.append(
                                " | ".join(
                                    cell.text.strip()
                                    for cell in row.cells
                                )
                            )

                slides_text.append(
                    f"SLIDE {slide_number}\n"
                    + "\n".join(slide_content)
                )

            ppt_text = "\n\n".join(slides_text)

            if not ppt_text.strip():
                st.warning("No readable text found in these slides.")
            else:
                st.session_state["ppt_text"] = ppt_text
                st.session_state["ppt_name"] = uploaded_pptx.name

                st.success("PowerPoint uploaded successfully! 🎉")
                st.write("Total slides:", len(presentation.slides))

                with st.expander("Preview Slide Text"):
                    st.write(ppt_text[:4000])

        except Exception as e:
            st.error(f"Could not read PowerPoint: {e}")

    if st.session_state.get("ppt_text", "").strip():
        st.markdown("---")
        st.subheader("💬 Ask Questions from Your Slides")

        ppt_question = st.text_input(
            "Ask something about your slides:",
            key="ppt_question"
        )

        if st.button("✨ Answer from Slides", key="ppt_answer_button"):
            
            if ppt_question.strip():
                try:
                    with st.spinner("MEXA.COM is reading your slides..."):

                        system_message = (
                            "You are MEXA.COM, a helpful study assistant. "
                            "Answer using the provided PowerPoint text in simple words. "
                            "If the answer is missing, say so."
                        )

                        prompt = (
                            "SLIDE CONTENT:\n"
                            + st.session_state["ppt_text"][:12000]
                            + "\n\nQUESTION:\n"
                            + ppt_question
                        )

                        answer = ask_ai(prompt, system_message)

                    st.markdown("### 🌷 MEXA.COM's Answer")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please write a question about your slides.")

# ---------- SMART STUDY MODE ----------
elif page == "✨ Smart Study Mode":

    st.subheader("✨ Smart Study Mode")
    st.write("Generate notes and practice questions from your study files.")

    study_source = st.radio(
        "Choose your study material:",
        ["📄 PDF", "🎞️ PowerPoint"],
        horizontal=True
    )

    if study_source == "📄 PDF":
        study_text = st.session_state.get("pdf_text", "")
    else:
        study_text = st.session_state.get("ppt_text", "")

    if not study_text.strip():
        st.info("Please upload a PDF or PowerPoint first.")
    else:
        study_action = st.selectbox(
            "What would you like MEXA.COM to create?",
            [
                "📝 Short Notes",
                "❓ Important Questions",
                "🎯 MCQs"
            ]
        )

        if st.button("✨ Generate", key="smart_study_generate"):
            if study_action == "📝 Short Notes":
                instruction = (
                    "Create clear, organized study notes in simple English. "
                    "Use headings and bullet points."
                )
            elif study_action == "❓ Important Questions":
                instruction = (
                    "Generate 10 important exam questions from this material. "
                    "Do not invent facts outside the material."
                )
            else:
                instruction = (
                    "Generate 10 multiple-choice questions with four options "
                    "each. Give the correct answer and a short explanation."
                )

            
            try:
                with st.spinner("MEXA.COM is preparing your study material..."):

                    system_message = (
                        "You are MEXA.COM, a helpful study assistant. "
                        "Use simple English and base your response "
                        "on the supplied study material."
                    )

                    prompt = (
                        instruction
                        + "\n\nSTUDY MATERIAL:\n"
                        + study_text[:12000]
                    )

                    answer = ask_ai(prompt, system_message)

                st.markdown("### 📚 Your Study Material")
                st.markdown(answer)

            except Exception as e:
                st.error(f"Could not generate study material: {e}")
