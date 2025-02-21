import streamlit as st
import requests

st.set_page_config(page_title="AI Blog Generator", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "welcome"

def go_to_generator():
    st.session_state.page = "generator"

if st.session_state.page == "welcome":
    st.markdown(
        """
        <style>
            .welcome-text { text-align: center; font-size: 36px; font-weight: bold; color: #ff66b2; }
            .subheading { text-align: center; font-size: 20px; color: #555; }
            .caption { text-align: center; font-size: 18px; font-style: italic; color: #888; margin-top: 10px; }
            .button-container { display: flex; justify-content: center; margin-top: 30px; }
            .stButton>button { width: 220px; height: 50px; font-size: 18px; font-weight: bold; border-radius: 10px; background-color: #ff66b2; color: white; border: none; cursor: pointer; margin-left: 50px; }
            .stButton>button:hover { background-color: #ff3385; }
        </style>
        <div class="welcome-text">✨ Welcome to AI Blog Generator! ✨</div>
        <div class="subheading">Unleash your creativity with AI-powered writing! 🚀</div>
        <div class="caption">"Writing made easy – just imagine, click, create!"</div>
        <div class="button-container">
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("Get Started"):
            go_to_generator()

elif st.session_state.page == "generator":
    st.title("AI Blog Generator")
    topic = st.text_input("Enter your blog topic", placeholder="E.g., The Future of AI")
    tone = st.selectbox("Select the tone", ["Fluent", "Formal", "Informal", "Humorous"])
    word_count = st.slider("Select word count", min_value=100, max_value=1000, step=50, value=500)

    if st.button("Generate Blog"):
        if topic:
            st.write("Generating blog... Please wait.")
            try:
                response = requests.post(
                    "http://localhost:8000/generate",
                    json={"topic": topic, "tone": tone, "word_count": word_count},
                )
                if response.status_code == 200:
                    data = response.json()
                    if "blog" in data:
                        st.success("✅ Blog Generated!")
                        st.write(data["blog"])
                    else:
                        st.warning("⚠️ No content generated. Try again.")
                else:
                    st.error(f"🚨 Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a blog topic.")
