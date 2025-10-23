import streamlit as st
import openai
import PyPDF2
from io import BytesIO

# Set your OpenAI API key here (replace with your real key from openai.com)
openai.api_key = "your-openai-api-key-here"  # IMPORTANT: Put your key here in quotes!

# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to get AI response (for chat, explanations, etc.)
def get_ai_response(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500  # Limit response length
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)} (Check your API key or quota)"

# Streamlit App Layout
st.title("AI Powered Study Buddy")
st.markdown("Upload notes, chat with AI, get summaries, explanations, and quizzes!")

# Sidebar for features
feature = st.sidebar.selectbox("Choose Feature", ["Chat", "Upload PDF & Summarize", "Explain Concept", "Generate Quiz"])

# Chat Interface
if feature == "Chat":
    st.header("Chat with AI")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("Ask a question:")
    if st.button("Send") and user_input:
        response = get_ai_response(user_input)
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"AI: {response}")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        st.write(msg)
    
    if st.button("Clear Chat"):
        st.session_state.chat_history = []

# PDF Upload & Summarize
elif feature == "Upload PDF & Summarize":
    st.header("Upload PDF Notes & Get Summary")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded_file and st.button("Summarize"):
        with st.spinner("Extracting text..."):
            text = extract_pdf_text(uploaded_file)
        if text:
            summary_prompt = f"Summarize this text in simple terms: {text[:2000]}"  # Limit to avoid API limits
            summary = get_ai_response(summary_prompt)
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.error("Could not extract text from PDF.")

# Explain Concept
elif feature == "Explain Concept":
    st.header("Explain a Concept")
    concept = st.text_input("Enter a concept (e.g., 'Newton's Laws'):")
    if st.button("Explain") and concept:
        explain_prompt = f"Explain {concept} simply, step-by-step, like to a beginner."
        explanation = get_ai_response(explain_prompt)
        st.subheader(f"Explanation of {concept}:")
        st.write(explanation)

# Generate Quiz
elif feature == "Generate Quiz":
    st.header("Generate MCQ Quiz")
    topic = st.text_input("Enter topic or upload PDF first (then paste text here):")
    num_questions = st.slider("Number of questions", 1, 5, 3)
    if st.button("Generate Quiz") and topic:
        quiz_prompt = f"Generate {num_questions} multiple-choice questions on {topic}. Format: Question? a) option b) option c) option d) option. Then say the correct answer."
        quiz = get_ai_response(quiz_prompt)
        st.subheader("Quiz:")
        st.write(quiz)
        
        # Simple scoring (user inputs answers manually)
        st.markdown("**Answer the questions above, then enter your answers below (e.g., a,b,c):**")
        user_answers = st.text_input("Your answers (comma-separated):")
        if st.button("Check Score"):
            # Basic check (in real app, parse AI response for correct answers)
            st.write("Score: Manual check needed! (For demo, compare with AI output)")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit, OpenAI, and PyPDF2. For Gemini, replace OpenAI calls with Google Generative AI library.")
