import streamlit as st
import requests
import urllib.parse
import time

# --- DESIGN SETUP ---
st.set_page_config(page_title="EPOCHA AI - Nano Banana Engine", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    .stTextInput input, .stTextArea textarea { border: 2px solid #fbbf24 !important; background-color: #1e293b !important; color: white !important; }
    .stButton>button { background: linear-gradient(to right, #fbbf24, #f59e0b); color: black; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

# Key-Abfrage aus den Secrets oder Sidebar
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Google API Key", type="password")

st.title("🏛️ EPOCHA Studio x Nano Banana")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Design-Konfiguration")
    v_title = st.text_input("Titel im Bild (z.B. Schattenfresser)")
    v_desc = st.text_area("Was soll auf dem Bild zu sehen sein?", height=150)
    format_choice = st.radio("Format:", ["16:9 (YouTube)", "9:16 (Shorts)"], horizontal=True)

    if st.button("BILD GENERIEREN"):
        if v_title and v_desc and api_key:
            with st.spinner("Nano Banana Engine erstellt dein Bild..."):
                w, h = (1280, 720) if "16:9" in format_choice else (720, 1280)
                
                # Optimierter Prompt für Nano Banana / Flux
                refined_prompt = f"Cinematic historical, {v_desc}. The text '{v_title}' is written in epic bold letters. 8k resolution, highly detailed."
                safe_prompt = urllib.parse.quote(refined_prompt)
                
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={w}&height={h}&nologo=true&model=flux&seed={time.time()}"
                
                try:
                    res = requests.get(img_url, timeout=30)
                    if res.status_code == 200:
                        st.session_state.web_img = res.content
                        st.session_state.img_format = "png"
                    else:
                        st.error(f"Server-Limit (Code {res.status_code}). Bitte 10 Sekunden warten.")
                except Exception as e:
                    st.error("Verbindungsfehler zum Server.")
        else:
            st.warning("Bitte Titel, Beschreibung und Key prüfen!")

with col2:
    st.subheader("Vorschau")
    # WICHTIG: Erst prüfen, ob 'web_img' überhaupt existiert!
    if 'web_img' in st.session_state and st.session_state.web_img is not None:
        st.image(st.session_state.web_img, use_container_width=True)
        
        # Download Button nur anzeigen, wenn Bild da ist
        st.download_button(
            label="💾 BILD HERUNTERLADEN",
            data=st.session_state.web_img,
            file_name=f"epocha_{int(time.time())}.png",
            mime="image/png"
        )
    else:
        # Schönerer Platzhalter
        st.info("Dein generiertes Bild wird hier angezeigt.")
        st.image("https://via.placeholder.com/1280x720.png?text=Warte+auf+Generierung...", use_container_width=True)

