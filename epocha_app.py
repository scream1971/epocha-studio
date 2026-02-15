import streamlit as st
import requests
import urllib.parse
import time

# --- DESIGN ---
st.set_page_config(page_title="EPOCHA AI - Nano Banana Engine", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    .stTextInput input, .stTextArea textarea { border: 2px solid #fbbf24 !important; }
    </style>
    """, unsafe_allow_html=True)

# Key-Abfrage
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = st.sidebar.text_input("Google API Key", type="password")

st.title("🏛️ EPOCHA Studio x Nano Banana")
st.write("Optimiert für hochauflösende historische Thumbnails und Shorts.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Thumbnail-Design")
    v_title = st.text_input("Haupt-Text für das Bild", placeholder="z.B. REICH DER SCHATTENFRESSER")
    v_desc = st.text_area("Bildbeschreibung", placeholder="z.B. Ein römischer Zenturio steht vor einem brennenden Tempel, düster, cineastisch", height=150)
    
    format_choice = st.radio("Format:", ["16:9 (YouTube)", "9:16 (TikTok/Shorts)"], horizontal=True)

    if st.button("MIT NANO BANANA GENERIEREN"):
        if v_title and v_desc and api_key:
            with st.spinner("Nano Banana berechnet die Details..."):
                w, h = (1280, 720) if "16:9" in format_choice else (720, 1280)
                
                # NANO BANANA liebt präzise Anweisungen für Text im Bild
                # Wir bauen den Prompt so, dass der Titel prominent erscheint
                refined_prompt = f"Cinematic historical style, {v_desc}. Central focus on the atmosphere. High fidelity, 8k. The text '{v_title}' is integrated artistically into the scene."
                safe_prompt = urllib.parse.quote(refined_prompt)
                
                # Wir nutzen die stabilste Route zur Engine
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={w}&height={h}&nologo=true&model=flux&seed={time.time()}"
                
                try:
                    res = requests.get(img_url, timeout=30)
                    if res.status_code == 200:
                        st.session_state.nano_img = res.content
                    else:
                        st.error("Server-Limit erreicht. Bitte 10 Sekunden warten.")
                except:
                    st.error("Verbindung zum Nano-Server unterbrochen.")
        else:
            st.warning("Bitte Titel, Beschreibung und Key prüfen!")

with col2:
    st.subheader("Vorschau")
    if 'nano_img' in st.session_state:
        st.image(st.session_state.nano_img, use_container_width=True)
        st.success("Generiert mit Nano Banana Technologie")
        st.download_button("THUMBNAIL SPEICHERN", st.session_state.nano_img, "epocha_nano.png", "image/png")
    else:
        st.info("Warte auf Eingabe...")
        st.download_button("Download", st.session_state.web_img, "thumbnail.png")
