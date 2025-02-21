import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(page_title="AI Blog Generator", layout="centered")

# Load Gemini API Key from Environment Variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🚨 API Key missing! Please set GEMINI_API_KEY in your environment variables.")
    st.stop()

# Configure Gemini AI
genai.configure(api_key=api_key)

# Session state to track navigation
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# Function to navigate to the blog generator
def go_to_generator():
    st.session_state.page = "generator"

# 🏡 WELCOME PAGE
if st.session_state.page == "welcome":
    st.markdown(
        """
        <style>
            .welcome-text {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                color: #ff66b2;
            }
            .subheading {
                text-align: center;
                font-size: 20px;
                color: #555;
            }
            .caption {
                text-align: center;
                font-size: 18px;
                font-style: italic;
                color: #888;
                margin-top: 10px;
            }
            .button-container {
                display: flex;
                justify-content: center;
                margin-top: 30px;
            }
            .stButton>button {
                width: 220px;
                height: 50px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                background-color: #ff66b2;
                color: white;
                border: none;
                cursor: pointer;
                margin-left: 50px;  /* Moves button slightly to the right */
            }
            .stButton>button:hover {
                background-color: #ff3385;
            }
        </style>
        <div class="welcome-text">✨ Welcome to AI Blog Generator! ✨</div>
        <div class="subheading">Unleash your creativity with AI-powered writing! 🚀</div>
        <div class="caption">"Writing made easy – just imagine, click, create!"</div>
        <div class="button-container">
    """,
        unsafe_allow_html=True
    )

    # Adjusted 'Get Started' Button
    col1, col2, col3 = st.columns([1, 1.5, 1])  # Adjust column widths for alignment
    with col2:
        if st.button("Get Started"):
            go_to_generator()

# ✍ BLOG GENERATOR PAGE
elif st.session_state.page == "generator":
    st.title("AI Blog Generator")

    # User Input Section
    topic = st.text_input("Enter your blog topic", placeholder="E.g., The Future of AI")

    # Tone Selection
    tone = st.selectbox("Select the tone", ["Fluent", "Formal", "Informal", "Humorous"])

    # Word Count Selection
    word_count = st.slider("Select word count", min_value=100, max_value=1000, step=50, value=500)

    # Generate Button
    if st.button("Generate Blog"):
        if topic:
            st.write("Generating blog... Please wait.")

            # Using Gemini AI Model
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            prompt = f"Write a {word_count}-word {tone.lower()} blog about {topic}."

            try:
                response = model.generate_content(prompt)
                if response and response.text:
                    st.success("✅ Blog Generated!")
                    st.write(response.text)
                else:
                    st.warning("⚠️ No content generated. Try again.")
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a blog topic.")
