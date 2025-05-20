import streamlit as st
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image
import random

# ---------- Page Config ----------
st.set_page_config(
    page_title="LostLanguages AI",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="expanded"
)

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

    /* Tabs styling */
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

    /* Enhanced card effect for sections */
    .card {
        background: rgba(30, 30, 30, 0.7);
        border-radius: 5px;
        border: 1px solid #8a7737;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

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
            background: linear-gradient(135deg, #e8dcb5 0%, #d3c59e 100%);
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
        </style>
    """, unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("""
    <div style="text-align:center;">
        <h1>📜 LostLanguages AI</h1>
        <p style="color:#c0b283; font-size: 1.1rem;">Unveil the whispers of forgotten worlds...</p>
    </div>
""", unsafe_allow_html=True)

# ---------- API Setup ----------
if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar to begin your linguistic quest.")
    st.stop()
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ---- New Feature 3: Multiple Input Methods with Tabs ----
st.markdown("<hr>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📝 Text Input", "📷 Image Analysis"])

with tab1:
    st.subheader("𓆣 Provide Ancient Symbols / Description")
    user_input = st.text_area("Enter symbols, fragments, or language traits", 
        height=150, key="user_input", 
        value=st.session_state.get('user_input', ''))
    
    col1, col2 = st.columns(2)
    with col1:
        simulate = st.checkbox("✨ Simulate conversation")
    with col2:
        detailed = st.checkbox("📚 Include historical context")

with tab2:
    st.subheader("🔍 Upload Image of Ancient Script")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Script", use_container_width=True)
        
        # Convert image to base64 for API
        buffered = BytesIO()
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        if st.button("🔍 Analyze Image"):
            with st.spinner("Deciphering visual symbols..."):
                try:
                    vision_prompt = "Describe and analyze the ancient script or symbols in this image."
                    
                    # Prepare image data for Gemini API
                    image_parts = [
                        {"text": vision_prompt},
                        {"image": {"data": img_str}}
                    ]
                    
                    response = model.generate_content(image_parts)
                    st.session_state.user_input = response.text[:500] + "..."
                    st.success("Image analyzed! Results transferred to text input.")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Vision analysis error: {e}")

# ---- New Feature 4: Advanced Options ----
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
st.markdown('</div>', unsafe_allow_html=True)

# Generate button - centered and enhanced
st.markdown('<div style="display: flex; justify-content: center; margin: 30px 0;">', unsafe_allow_html=True)
generate_btn = st.button("🔓 Reveal Lost Meanings", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- AI Logic ----------
if generate_btn and (user_input or 'user_input' in st.session_state):
    # Use the input from session state if available
    input_text = user_input or st.session_state.get('user_input', '')
    
    if not input_text:
        st.warning("Please provide text or upload an image of ancient script.")
    else:
        with st.spinner("📜 Translating the echoes of ancient minds..."):
            # Build advanced prompt based on selected options
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
            """

            try:
                response = model.generate_content(prompt)
                
                # ---- New Feature 5: Interactive Results Display ----
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.success("✨ Ancient Insight Unlocked")
                
                # Create tabs for organized results display
                result_tabs = st.tabs(["📜 Translation", "🔍 Analysis", "📚 References"])
                
                # Split response into sections
                full_text = response.text
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
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ---------- Footer ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color: #b4a077;'>🔮 Crafted by the Oracle of Lost Scripts ✧</div>", unsafe_allow_html=True)
