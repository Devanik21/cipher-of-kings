import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests

# ---------- Page Config ----------
st.set_page_config(
    page_title="LostLanguages AI",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------- Load Lottie Animation ----------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_glyphs = load_lottie("https://lottie.host/15154c13-4531-4780-9186-4dd53cecf7a3/lqFqupAP1k.json")

# ---------- Custom CSS Theme ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&display=swap');

    html, body {
        background-color: #0d0d0d;
        background-image: url('https://www.transparenttextures.com/patterns/black-linen.png');
        color: #e0dcbf;
        font-family: 'Cinzel', serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1b1b1b 100%);
    }

    h1, h2, h3 {
        color: #e6c967 !important;
        text-shadow: 0 0 8px #b29f57, 0 0 4px #7f6b2d;
        letter-spacing: 1.5px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    textarea, .stTextInput>div>div>input {
        background-color: #2c2c2c !important;
        color: #f1e8d7 !important;
        border: 1px solid #8a7737 !important;
        border-radius: 0px;
    }

    .stButton>button {
        background: radial-gradient(circle, #b49d5b, #5a421d);
        color: #fff8dc;
        border: 2px solid #8a7737;
        border-radius: 50%;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 0 10px #bfa85a;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #6b502a;
        color: #ffffff;
    }

    .sidebar .sidebar-content {
        background-color: #1c1c1c;
        color: #f5deb3;
    }

    hr {
        border: 1px solid #e6c967;
        margin: 2rem 0;
    }

    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("𒀭 Ancient Oracle")
api_key = st.sidebar.text_input("𓂀 Gemini API Key", type="password")

# ---------- Title ----------
st.markdown("""
    <div style="text-align:center;">
        <h1>📜 LostLanguages AI</h1>
        <p style="color:#c0b283; font-size: 1.1rem;">Unveil the whispers of forgotten worlds...</p>
    </div>
""", unsafe_allow_html=True)

# ---------- Animation ----------
st_lottie(lottie_glyphs, height=250, key="glyphs")

# ---------- API Setup ----------
if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar to begin your linguistic quest.")
    st.stop()
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ---------- Input Form ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("𓆣 Provide Ancient Symbols / Description")
user_input = st.text_area("Enter symbols, fragments, or language traits", height=200)

simulate = st.checkbox("✨ Simulate a mythical conversation in this language")
generate_btn = st.button("🔓 Reveal Lost Meanings")

# ---------- AI Logic ----------
if generate_btn and user_input:
    with st.spinner("Translating the echoes of ancient minds..."):

        prompt = f"""
        You are an AI expert in ancient and fictional languages.
        Input: {user_input}

        Step 1: Hypothesize the language structure based on ancient patterns.
        Step 2: Attempt a symbolic or contextual translation.
        Step 3: Explain your translation logic.

        {'Step 4: Simulate a conversation in this language between two fictional individuals, with English translations.' if simulate else ''}
        """

        try:
            response = model.generate_content(prompt)
            st.success("✨ Ancient Insight Unlocked:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------- Footer ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color: #b4a077;'>🔮 Crafted by the Oracle of Lost Scripts ✧</div>", unsafe_allow_html=True)
