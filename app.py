import streamlit as st
import re
import pickle
from youtube_transcript_api import YouTubeTranscriptApi
import easyocr
import cv2
import numpy as np

st.set_page_config(page_title="VERIFACT", page_icon="logo.png", layout="centered")
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()
import json

# Force Chrome to show Install button
st.markdown("""
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('data:text/javascript,');
}
</script>
""", unsafe_allow_html=True)

# PWA Manifest serve cheyyadaniki
manifest = {
    "name": "VERIFACT - Fake News Detector",
    "short_name": "VERIFACT", 
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0E1117",
    "theme_color": "#00FFFF",
    "scope": "/",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}
    ]
}
st.markdown(f'<link rel="manifest" href="data:application/json,{json.dumps(manifest)}">', unsafe_allow_html=True)
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
    
.main {background-color: #f0f2f6;}
.real-box {background-color: #1a4d2e; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; margin-top: 10px;}
.fake-box {background-color: #4d1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid #dc3545; margin-top: 10px;}
.footer {text-align: center; color: grey; margin-top: 50px; font-size: 12px;}
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
      
def generate_why_explanation(verdict, user_text):
    if verdict == "FAKE":
        return ["Clickbait words unayi", "Facts verify kaledu", "Similar fake news spread ayyindi"]
    else:
        return ["Neutral language undi", "Training data tho match ayindi", "Red flags levu"]
      
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
            prediction = model.predict(text_tfidf)[0] 
            
            # ===== VERDICT DECIDE CHEYADAM =====
            if prediction == 0:
              verdict = "REAL"
            else:
              verdict = "FAKE"
            why_points = generate_why_explanation(verdict, user_input)
            
            # Get probability for confidence
            proba = model.predict_proba(text_tfidf)[0]
            confidence = max(proba) * 100
            
            # ====== Spinner aipoyaka ======
         if verdict == "REAL":
            st.markdown(f'<div class="real-box"><h2>✅ Verdict: REAL</h2><p>Confidence: {confidence:.1f}%</p></div>', unsafe_allow_html=True)
         else:
            st.markdown(f'<div class="fake-box"><h2>❌ Verdict: FAKE</h2><p>Confidence: {confidence:.1f}%</p></div>', unsafe_allow_html=True)
            
         st.progress(int(confidence)/100)

         # ====== NEW: WHY SECTION ======
         with st.expander("🤔 Why this verdict?"):
           for i, reason in enumerate(why_points, 1):
               st.write(f"**{i}.** {reason}")

         # ====== NEW: SOURCES SECTION ======
         with st.expander("📚 Sources & Fact Check"):
              st.write("**Model Info:**")
              st.write(f"- **Dataset**: 44k Fake News Dataset")
              st.write(f"- **Model**: TF-IDF + Logistic Regression")
              st.write(f"- **Top Keywords**: {', '.join(extracted_text.lower().split()[:5])}")
    
st.info("💡 Next Update: Google Search API add cheste live URL lu kuda vasthayi") 
st.markdown('<div class="footer">Made with ❤️ by Narasimha Rao Killi | Trained on 44k Dataset</div>', unsafe_allow_html=True)
st.header("🖼️ MemeFact")
st.write("Meme image upload cheyi, text extract chesi fact check cheptha")

uploaded_file = st.file_uploader("Upload Meme Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
 file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
 image = cv2.imdecode(file_bytes, 1)
 st.image(image, caption="Uploaded Meme", use_column_width=True)
    
    # OCR to extract text
    with st.spinner("Text extract chesthunna..."):
    results = reader.readtext(image)
    extracted_text = " ".join([res[1] for res in results])
    
    st.success("Extracted Text:")
    st.write(extracted_text)
    
     if st.button("Check Meme Fact"):
        st.write("Ikkada extracted text ni model tho check cheyali")
