import streamlit as st

st.set_page_config(page_title="VERIFACT", layout="centered")

# ===== THEME CSS - NO WATERMARK, NO LOGO =====
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
</style>
""", unsafe_allow_html=True)
# ===== CSS END =====


# ===== APP CONTENT =====
st.title("VERIFACT 🛡️")
st.subheader("Don't believe everything you read. Verify it.")

user_input = st.text_area("Enter news text here:", height=200, placeholder="Paste news article or headline...")

if st.button("Verify News"):
    if user_input:
        with st.spinner("Analyzing..."):
            # Demo logic - ippatiki
            if "fake" in user_input.lower():
                st.error("Result: FAKE") 
                st.write("Confidence: 88%")
            else:
                st.success("Result: REAL") 
                st.write("Confidence: 92%")
    else:
        st.warning("Please enter some text to verify.")
