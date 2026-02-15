import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(page_title="EPOCHA Web Studio", layout="wide")

st.title("🏛️ EPOCHA - Online AI Studio")

# Wir holen uns den Key sicher aus den "Secrets" des Webservers
# Wenn lokal getestet wird, nutzt er das Eingabefeld
api_key = st.sidebar.text_input("Google API Key", type="password")

col1, col2 = st.columns([1, 1])

with col1:
    v_title = st.text_input("Videotitel")
    v_desc = st.text_area("Beschreibung", height=150)
    format_choice = st.radio("Format:", ["16:9", "9:16"], horizontal=True)
    
    if st.button("BILD GENERIEREN"):
        if v_title and v_desc and api_key:
            with st.spinner("KI arbeitet im Web..."):
                w, h = (1280, 720) if "16:9" in format_choice else (720, 1280)
                prompt = urllib.parse.quote(f"cinematic historical 8k, {v_title}, {v_desc}")
                # Im Web nutzen wir eine stabilere Route
                img_url = f"https://image.pollinations.ai/prompt/{prompt}?width={w}&height={h}&nologo=true&seed={time.time()}"
                
                try:
                    res = requests.get(img_url, timeout=30)
                    if res.status_code == 200:
                        st.session_state.web_img = res.content
                    else:
                        st.error("Server im Web gerade ausgelastet.")
                except:
                    st.error("Verbindungsfehler.")
        else:
            st.warning("Bitte Titel, Beschreibung und Key eingeben!")

with col2:
    if 'web_img' in st.session_state:
        st.image(st.session_state.web_img)
        st.download_button("Download", st.session_state.web_img, "thumbnail.png")