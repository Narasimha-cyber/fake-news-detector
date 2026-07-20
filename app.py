import streamlit as st
from PIL import Image
import re
import pickle
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="VERIFACT", page_icon="logo.png", layout="centered")
st.markdown('<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)

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

def get_youtube_text(url):
    try:
        video_id = re.findall(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i['text'] for i in transcript])
        return text
    except:
        return "Could not get YouTube transcript. Video ki captions untey matrame work avthadi"
import instaloader

def get_insta_text(url):
    try:
        L = instaloader.Instaloader()
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        return post.caption if post.caption else "No caption found"
    except:
        return "Could not get Instagram caption. Post public ga undali"
if st.button("Verify News"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some news text or YouTube link first!")
    else:
        with st.spinner("Verifying news..."):
            import time, random
            time.sleep(1)
            # Load the trained 44k model
            try:
              model = pickle.load(open('model_44k.pkl', 'rb'))
              vectorizer = pickle.load(open('vectorizer_44k.pkl', 'rb'))
            except FileNotFoundError:
              st.error("model_44k.pkl and vectorizer_44k.pkl files not found. Upload them to GitHub first.")
              st.stop()
            text_tfidf = vectorizer.transform([user_input])
            prediction = model.predict(text_tfidf)
          
            # Get probability for confidence
            proba = model.predict_proba(text_tfidf)[0]
            confidence = max(proba) * 100

            # Model result ni chupinchu
            if prediction[0] == 1:
               st.success(f"✅ REAL NEWS - Confidence: {confidence:.2f}%")
            else:
               st.error(f"❌ FAKE NEWS - Confidence: {confidence:.2f}%")

                # Kindhaki unna fake_keywords, real_keywords anni delete chey

              
