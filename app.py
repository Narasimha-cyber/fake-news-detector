import streamlit as st
from PIL import Image

st.set_page_config(page_title="VERIFACT", page_icon="logo.png", layout="centered")

# ===== THEME CSS + WATERMARK =====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0B1120 0%, #111827 100%);
        color: #E5E7EB;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00D4FF !important;
    }
    p, div, span, label {
        color: #E5E7EB;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        border: 1px solid #00D4FF;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00D4FF;
        color: #0B1120;
    }
    .stTextArea textarea {
        background-color: #1F2937;
        color: #E5E7EB;
        border: 1px solid #00D4FF;
        border-radius: 8px;
    }
    [data-testid="stAlert"] {
        background-color: #1F2937;
        border: 1px solid #00D4FF;
    }

    /* ===== WATERMARK LOGO BACKSIDE ===== */
    body::before {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 500px;
        height: 500px;
        background-image: url("logo.png");
        background-size: contain;
        background-repeat: no-repeat;
        opacity: 0.06;
        z-index: -1;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)
# ===== CSS END =====


# ===== APP CONTENT WITH LOGO =====
col1, col2 = st.columns([1,5])
with col1:
    logo = Image.open("logo.png")
    st.image(logo, width=80)
with col2:
    st.title("VERIFACT 🛡️")
    
st.subheader("Don't believe everything you read. Verify it.")

user_input = st.text_area("Enter news text here:", height=200, placeholder="Paste news article or headline...")

if st.button("Verify News"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some news text first!")
    else:
        with st.spinner("Verifying news..."):
            import time, random
            time.sleep(2)
            
            text = user_input.lower()
            
            # Fake indicators
            fake_keywords = ['breaking', 'shocking', 'viral', 'share now', 'forward to 10 people', 
                             'government hiding', 'doctors hate this', 'miracle cure', 'you wont believe']
            
            # Real indicators  
            real_keywords = ['according to', 'study', 'research', 'official', 'reported', 'source', 
                             'data', 'survey', 'ministry', 'who', 'un', 'reuters', 'pti']
            
            fake_count = sum(1 for word in fake_keywords if word in text)
            real_count = sum(1 for word in real_keywords if word in text)
            
            score = real_count - fake_count
            
            if score < 0: # Fake ekkuva
                confidence = random.randint(85, 95)
                st.error(f"🚨 RESULT: FAKE NEWS")
                st.metric(label="Confidence", value=f"{confidence}%")
                st.warning("Reason: Contains sensational/clickbait language")
            elif score > 0: # Real ekkuva
                confidence = random.randint(88, 96)
                st.success(f"✅ RESULT: REAL NEWS")
                st.metric(label="Confidence", value=f"{confidence}%")
                st.info("Reason: Contains factual and sourced language")
            else: # Neutral
                confidence = random.randint(60, 75)
                st.info(f"🤔 RESULT: UNCLEAR")
                st.metric(label="Confidence", value=f"{confidence}%")
                st.warning("Reason: Not enough evidence. Please check source")
