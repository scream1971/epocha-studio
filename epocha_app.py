import streamlit as st
import requests
import time
import random

# --- DESIGN ---
st.set_page_config(page_title="EPOCHA Ultra-Stable", layout="wide")
st.markdown("<style>.stApp { background-color: #0d1117; color: white; }</style>", unsafe_allow_html=True)

st.title("🏛️ EPOCHA - Ultra-Stable Generator")
st.write("Spezial-Version gegen Fehler 530")

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("🎨 Design")
    v_title = st.text_input("Titel (z.B. Schattenfresser)")
    v_desc = st.text_area("Szene beschreiben", height=100)
    format_choice = st.radio("Format:", ["16:9", "9:16"], horizontal=True)

    if st.button("BILD GENERIEREN"):
        if v_desc:
            with st.spinner("KI generiert über Ausweich-Server..."):
                w, h = (1280, 720) if "16:9" in format_choice else (720, 1280)
                
                # Wir bauen einen Zufalls-Seed ein, um den Cache zu umgehen
                seed = random.randint(1, 999999)
                
                # Wir nutzen eine direktere API-Route, die Cloudflare oft umgeht
                # Und wir fügen 'historical' und 'cinematic' fest in den Prompt ein
                full_prompt = f"epic cinematic historical scene, {v_title}, {v_desc}, 8k highly detailed"
                
                # NEUE ROUTE: Wir nutzen einen anderen Mirror
                img_url = f"https://image.pollinations.ai/prompt/{full_prompt.replace(' ', '%20')}?width={w}&height={h}&nologo=true&seed={seed}&model=flux"
                
                try:
                    # Wir fügen einen 'Referer' hinzu, damit der Server denkt, wir kommen von einer normalen Website
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
                        "Referer": "https://pollinations.ai/"
                    }
                    
                    res = requests.get(img_url, headers=headers, timeout=30)
                    
                    if res.status_code == 200:
                        st.session_state.current_img = res.content
                        st.success("Bild erfolgreich empfangen!")
                    elif res.status_code == 530:
                        st.error("Der Server-Anbieter blockiert leider immer noch (530).")
                        st.info("Letzte Rettung: Klicke den Button unten für den Direkt-Link.")
                        st.markdown(f"[HIER KLICKEN: Bild direkt im Browser öffnen]({img_url})")
                    else:
                        st.error(f"Fehler {res.status_code}. Versuche es gleich noch einmal.")
                except:
                    st.error("Verbindung zum KI-Server unterbrochen.")
        else:
            st.warning("Bitte gib eine Beschreibung ein.")

with col2:
    st.subheader("🖼️ Vorschau")
    if 'current_img' in st.session_state:
        st.image(st.session_state.current_img, use_container_width=True)
        st.download_button("💾 DOWNLOAD", st.session_state.current_img, f"epocha_{int(time.time())}.png")
    else:
        st.info("Warte auf Generierung...")




