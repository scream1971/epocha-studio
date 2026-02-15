import streamlit as st
import requests
import urllib.parse
import time

# --- DESIGN ---
st.set_page_config(page_title="EPOCHA Multi-Engine", layout="wide")
st.markdown("<style>.stApp { background-color: #0d1117; color: white; }</style>", unsafe_allow_html=True)

# Key-Abfrage (Secrets oder Sidebar)
api_key = st.secrets.get("GOOGLE_API_KEY", st.sidebar.text_input("API Key", type="password"))

st.title("🏛️ EPOCHA Multi-AI Studio")

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("🎨 Bild-Konfiguration")
    v_title = st.text_input("Titel (für Nano Banana)", placeholder="z.B. Schattenfresser")
    v_desc = st.text_area("Szene beschreiben", height=100)
    
    engine = st.selectbox("KI-Modell wählen:", [
        "Nano Banana (Beste Qualität/Text)", 
        "Turbo Engine (Schnell & Stabil)", 
        "Creative Engine (Künstlerisch)"
    ])
    
    format_choice = st.radio("Format:", ["16:9", "9:16"], horizontal=True)

    if st.button("BILD GENERIEREN"):
        if v_desc:
            with st.spinner(f"Verbinde mit {engine}..."):
                w, h = (1280, 720) if "16:9" in format_choice else (720, 1280)
                
                model_param = "flux"
                if "Turbo" in engine: model_param = "turbo"
                if "Creative" in engine: model_param = "any"
                
                prompt = urllib.parse.quote(f"cinematic history, {v_title}, {v_desc}, 8k")
                img_url = f"https://image.pollinations.ai/prompt/{prompt}?width={w}&height={h}&nologo=true&model={model_param}&seed={time.time()}"
                
                try:
                    res = requests.get(img_url, timeout=30)
                    if res.status_code == 200:
                        st.session_state.current_img = res.content
                        st.success(f"Erfolgreich generiert!")
                    else:
                        st.error(f"Fehler {res.status_code}. Probiere die 'Turbo Engine'.")
                except:
                    st.error("Server-Verbindung fehlgeschlagen.")
        else:
            st.warning("Bitte gib eine Beschreibung ein.")

with col2:
    st.subheader("🖼️ Vorschau")
    # Hier war der Fehler: Alle Zeilen unter "with col2:" müssen exakt gleich weit eingerückt sein
    if 'current_img' in st.session_state:
        st.image(st.session_state.current_img, use_container_width=True)
        st.download_button("💾 DOWNLOAD", st.session_state.current_img, f"epocha_{int(time.time())}.png")
    else:
        st.info("Dein generiertes Bild wird hier angezeigt.")
        st.image("https://via.placeholder.com/1280x720.png?text=Warte+auf+Generierung...", use_container_width=True)



