import streamlit as st
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image
import random
import pandas as pd
import json
import time
from datetime import datetime
import io




# ---------- Page Config ----------
st.set_page_config(
    page_title="LostLanguages AI",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.image("a2.jpg", caption="🪞 Astral Mirror", use_container_width=True)

st.image("a3.jpg", caption="🪞 Astral Mirror", use_container_width=True)

st.image("a4.jpg", caption="🪞 Astral Mirror", use_container_width=True)
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
        border-radius: 5px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        font-size: 1rem;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #6b502a;
        box-shadow: 0 0 15px #e6c967;
        transform: translateY(-2px);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2c2c2c;
        border: 1px solid #8a7737;
        color: #e0dcbf;
        border-radius: 4px 4px 0px 0px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #5a421d !important;
        color: #fff8dc !important;
    }

    .card {
        background: rgba(30, 30, 30, 0.7);
        border-radius: 5px;
        border: 1px solid #8a7737;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .progress-bar {
        height: 20px;
        background-color: #5a421d;
        border-radius: 5px;
        transition: width 0.5s;
        margin-bottom: 10px;
    }

    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ---------- Session State Init ----------
if 'history' not in st.session_state:
    st.session_state.history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Ancient symbols and example languages
SAMPLE_LANGUAGES = {
    "Sumerian Cuneiform": "𒀭 𒌋 𒁹 𒌋 𒀀 𒉡 𒀭 𒌋𒁹 𒊏 𒀀𒊮",
    "Ancient Egyptian": "𓂀 𓀀 𓁐 𓃒 𓆣 𓇯 𓈖 𓉐 𓏏 𓊖",
    "Linear B": "𐀀 𐀁 𐀂 𐀃 𐀄 𐀅 𐀆 𐀇 𐀈 𐀉 𐀊 𐀋",
    "Phoenician": "𐤀 𐤁 𐤂 𐤃 𐤄 𐤅 𐤆 𐤇 𐤈 𐤉 𐤊",
    "Fictional Elvish": "ᚠᛁᚱᛖ ᚹᚨᛏᛖᚱ ᛖᚨᚱᚦ ᚨᛁᚱ ᛗᚨᚷᛁᚲ"
}

# ---------- Sidebar ----------
st.sidebar.title("𒀭 Ancient Oracle")
api_key = st.sidebar.text_input("𓂀 Gemini API Key", type="password")

# ---- New Feature 1: Language Presets ----
st.sidebar.markdown("### 📚 Sample Languages")
selected_sample = st.sidebar.selectbox("Select a sample", list(SAMPLE_LANGUAGES.keys()))
if st.sidebar.button("📝 Use Sample"):
    st.session_state.user_input = SAMPLE_LANGUAGES[selected_sample]

# ---- New Feature 2: Theme Selector ----
st.sidebar.markdown("### 🎨 Visual Theme")
theme = st.sidebar.radio("Choose your experience:", ["Ancient Parchment", "Mystic Night"])
if theme == "Ancient Parchment":
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #2a251f 0%, #1c1a16 100%);
        }
        textarea, .stTextInput>div>div>input {
            background-color: #f0e6cf !important;
            color: #4d3f22 !important;
        }
        h1, h2, h3 {
            color: #6b4c28 !important;
            text-shadow: 0 0 8px rgba(107, 76, 40, 0.3);
        }
        html, body {
            color: #4d3f22;
        }
        .card {
            background: rgba(216, 202, 174, 0.7);
        }
        </style>
    """, unsafe_allow_html=True)

# ---- NEW FEATURE 1: Toggle Dark Mode ----
if st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode):
    st.session_state.dark_mode = True
else:
    st.session_state.dark_mode = False
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #e8d9b5 0%, #c7b68a 100%);
        }
        </style>
    """, unsafe_allow_html=True)

# ---- NEW FEATURE 2: File Upload for Text Analysis ----
st.sidebar.markdown("### 📄 Upload Text File")
uploaded_file = st.sidebar.file_uploader("Upload a text file with symbols", type=["txt"])
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.session_state.user_input = content

# ---------- Title ----------
st.markdown("""
    <div style="text-align:center;">
        <h1>📜 LostLanguages AI</h1>
        <p style="color:#c0b283; font-size: 1.1rem;">Unveil the whispers of forgotten worlds...</p>
    </div>
""", unsafe_allow_html=True)

# ---------- API Setup ----------
def setup_api():
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar to begin your linguistic quest.")
        return False
    else:
        genai.configure(api_key=api_key)
        return True

# ---------- Multiple Input Methods with Tabs ----
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("𓆣 Provide Ancient Symbols / Description")
user_input = st.text_area("Enter symbols, fragments, or language traits", 
    height=150, key="user_input", 
    value=st.session_state.get('user_input', ''))

col1, col2 = st.columns(2)
with col1:
    simulate = st.checkbox("✨ Simulate conversation")
with col2:
    detailed = st.checkbox("📚 Include historical context")

# ---- Advanced Options ----
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("⚙️ Analysis Options")
col1, col2, col3 = st.columns(3)
with col1:
    analysis_depth = st.select_slider("Depth of Analysis", options=["Basic", "Standard", "Academic"])
with col2:  
    time_period = st.multiselect("Relevant Time Periods", 
        ["Ancient (3000-500 BCE)", "Classical (500 BCE-500 CE)", 
        "Medieval (500-1500 CE)", "Unknown/Fictional"])
with col3:
    geography = st.selectbox("Geographic Origin", 
        ["Any", "Mesopotamia", "Egypt", "Mediterranean", "Asia", "Americas", "Fantasy"])

# ---- NEW FEATURE 3: AI Model Selection ----
st.markdown("### 🧠 Model Options")
model_type = st.radio("Select AI Model", ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro","gemini-2.0-flash-lite","gemini-2.0-pro-exp-02-05",
"gemini-2.0-flash-thinking-exp-01-21","gemini-2.5-pro-exp-03-25","gemini-1.5-flash-8b"])

# ---- NEW FEATURE 4: Language Translation Options ----
translation_options = st.expander("🔤 Translation Options")
with translation_options:
    col1, col2 = st.columns(2)
    with col1:
        target_language = st.selectbox("Translate results to:", 
                                     ["English", "Spanish", "French", "German", "Japanese", "Arabic"])
    with col2:
        include_pronunciation = st.checkbox("Include pronunciation guide")
        
# ---- NEW FEATURE 5: Custom Prompt Builder ----
custom_prompt = st.expander("✏️ Custom Prompt Builder")
with custom_prompt:
    prompt_template = st.text_area("Customize your prompt template:",
        value="You are an AI expert in ancient and fictional languages.\n[INPUT]\n\nAnalyze this language and provide:\n1. Possible origins\n2. Translation attempt\n3. Cultural context",
        height=150)
    use_custom_prompt = st.checkbox("Use custom prompt")

st.markdown('</div>', unsafe_allow_html=True)

# ---- NEW FEATURE 6: Save Favorites ----
def save_favorite():
    if 'current_result' in st.session_state:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        favorite = {
            "timestamp": timestamp,
            "input": user_input,
            "result": st.session_state.current_result,
            "settings": {
                "analysis_depth": analysis_depth,
                "time_period": time_period,
                "geography": geography
            }
        }
        st.session_state.favorites.append(favorite)
        st.success("✅ Saved to favorites!")

# ---- NEW FEATURE 7: Export Results ----
def export_results():
    if 'current_result' in st.session_state:
        export_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "input": user_input,
            "result": st.session_state.current_result,
            "settings": {
                "analysis_depth": analysis_depth,
                "time_period": time_period,
                "geography": geography
            }
        }
        
        # Convert to JSON string
        json_str = json.dumps(export_data, indent=4)
        
        # Create a download button
        st.download_button(
            label="📥 Download Results (JSON)",
            data=json_str,
            file_name=f"lost_language_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

# Generate button - centered and enhanced
st.markdown('<div style="display: flex; justify-content: center; margin: 30px 0;">', unsafe_allow_html=True)
generate_btn = st.button("🔓 Reveal Lost Meanings", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- AI Logic ----------
def generate_translation():
    if not setup_api():
        return
        
    input_text = user_input or st.session_state.get('user_input', '')
    
    if not input_text:
        st.warning("Please provide text or upload a file of ancient script.")
        return
        
    # Show animated progress
    progress_placeholder = st.empty()
    for i in range(101):
        progress_placeholder.markdown(f"""
            <div class="progress-bar" style="width: {i}%;"></div>
            <div style="text-align: center;">Decoding ancient wisdom... {i}%</div>
        """, unsafe_allow_html=True)
        time.sleep(0.01)
    
    # Build prompt based on selected options
    if use_custom_prompt:
        prompt = prompt_template.replace("[INPUT]", f"Input: {input_text}")
    else:
        prompt = f"""
        You are an AI expert in ancient and fictional languages.
        Input: {input_text}
        
        Analysis depth: {analysis_depth}
        Relevant time periods: {', '.join(time_period) if time_period else 'Any'}
        Geographic origin: {geography}
        
        Step 1: Hypothesize the language structure based on ancient patterns.
        Step 2: Attempt a symbolic or contextual translation.
        Step 3: Explain your translation logic.
        {"Step 4: Include detailed historical and cultural context." if detailed else ""}
        {"Step 5: Simulate a conversation in this language between two fictional individuals, with English translations." if simulate else ""}
        
        {f"Translate all results to {target_language}." if target_language != "English" else ""}
        {f"Include pronunciation guides for ancient terms." if include_pronunciation else ""}
        """

    try:
        # Use the selected model
        model = genai.GenerativeModel(model_name=model_type)
        response = model.generate_content(prompt)
        
        # Store result in session state for favorites and export
        st.session_state.current_result = response.text
        
        # Add to history
        history_item = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "input": input_text,
            "result": response.text[:100] + "..." if len(response.text) > 100 else response.text
        }
        st.session_state.history.append(history_item)
        
        # Display results
        progress_placeholder.empty()
        display_results(response.text)
        
    except Exception as e:
        st.error(f"Something went wrong: {e}")

def display_results(full_text):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.success("✨ Ancient Insight Unlocked")
    
    # Create tabs for organized results display
    result_tabs = st.tabs(["📜 Translation", "🔍 Analysis", "📚 References", "🔧 Export"])
    
    # Split response into sections
    translation_part = full_text[:int(len(full_text)/2)]
    analysis_part = full_text[int(len(full_text)/2):]
    
    with result_tabs[0]:
        st.markdown(translation_part)
        
    with result_tabs[1]:
        st.markdown(analysis_part)
        
    with result_tabs[2]:
        st.markdown("### Suggested Sources")
        # Generate random fictional references based on the input
        references = [
            f"The Codex of {random.choice(['Lost', 'Ancient', 'Forgotten'])} {random.choice(['Scripts', 'Languages', 'Symbols'])}",
            f"Journal of {random.choice(['Historical', 'Ancient', 'Comparative'])} Linguistics, vol. {random.randint(1, 50)}",
            f"University of {random.choice(['Oxford', 'Cambridge', 'Harvard'])} Archive of Ancient Texts"
        ]
        for ref in references:
            st.markdown(f"- {ref}")
            
    with result_tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⭐ Save to Favorites"):
                save_favorite()
        with col2:
            export_results()
        
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn and (user_input or 'user_input' in st.session_state):
    generate_translation()

# ---- NEW FEATURE 8: History Tab ----
if st.session_state.history:
    history_expander = st.expander("📖 Translation History")
    with history_expander:
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**{item['timestamp']}**")
            st.markdown(f"Input: {item['input'][:50]}..." if len(item['input']) > 50 else f"Input: {item['input']}")
            st.markdown(f"Result: {item['result']}")
            st.markdown("---")

# ---- NEW FEATURE 9: Favorites Collection ----
if st.session_state.favorites:
    favorites_expander = st.expander("⭐ Favorite Translations")
    with favorites_expander:
        for i, fav in enumerate(st.session_state.favorites):
            st.markdown(f"**{fav['timestamp']}**")
            if st.button(f"Load Favorite #{i+1}", key=f"load_fav_{i}"):
                st.session_state.user_input = fav['input']
                st.experimental_rerun()
            st.markdown("---")

# ---- NEW FEATURE 10: Collaborative Mode ----
collab_expander = st.expander("👥 Collaborative Translation Mode")
with collab_expander:
    st.markdown("Share your findings with colleagues or save for later:")
    
    # Generate a unique session ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = f"session-{random.randint(1000, 9999)}"
        
    st.code(st.session_state.session_id)
    st.markdown("Enter a colleague's session ID to load their work:")
    colleague_session = st.text_input("Session ID")
    if st.button("Load Colleague Session") and colleague_session:
        st.success(f"Attempted to load session {colleague_session}")
        # In a real app, this would load the colleague's session data
        
    # Export session data option
    if 'current_result' in st.session_state:
        session_data = {
            "session_id": st.session_state.session_id,
            "history": st.session_state.history,
            "favorites": st.session_state.favorites
        }
        json_session = json.dumps(session_data)
        st.download_button(
            "💾 Export Session Data",
            data=json_session,
            file_name=f"lost_languages_session_{st.session_state.session_id}.json",
            mime="application/json"
        )

with st.sidebar:
    st.image("a1.jpg", caption="🪞 Astral Mirror", use_container_width=True)

# ---------- Footer ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color: #b4a077;'>🔮 Crafted by the Oracle of Lost Scripts ✧</div>", unsafe_allow_html=True)
