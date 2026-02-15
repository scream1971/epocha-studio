import streamlit as st
import requests
import urllib.parse
import time

# --- DESIGN ---
st.set_page_config(page_title="EPOCHA Multi-Engine", layout="wide")
st.markdown("<style>.stApp { background-color: #0d1117; color: white; }</style>", unsafe_allow_html=True)

# Key-Abfrage
api_key = st.secrets.get("GOOGLE_API_KEY", st.sidebar.text_input("API Key", type="password"))

st.title("🏛️ EPOCHA Multi-AI Studio")

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("🎨 Bild-Konfiguration")
    v_title = st.text_input("Titel (für Nano Banana)", placeholder="z.B. Schattenfresser")
    v_desc = st.text_area("Szene beschreiben", height=100)
    
    # --- MULTI-KI WAHL ---
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
                
                # Modell-Logik
                model_param = "flux" # Standard
                if "Turbo" in engine: model_param = "turbo"
                if "Creative" in engine: model_param = "any" # Zufälliges kreatives Modell
                
                # Prompt-Optimierung
                prompt = urllib.parse.quote(f"cinematic history, {v_title}, {v_desc}, 8k")
                img_url = f"https://image.pollinations.ai/prompt/{prompt}?width={w}&height={h}&nologo=true&model={model_param}&seed={time.time()}"
                
                try:
                    res = requests.get(img_url, timeout=30)
                    if res.status_code == 200:
                        st.session_state.current_img = res.content
                        st.success(f"Erfolgreich generiert mit {engine}")
                    else:
                        st.error(f"Fehler {res.status_code}. Versuche es mit der 'Turbo Engine'!")
                except:
                    st.error("Server-Verbindung fehlgeschlagen.")
        else:
            st.warning("Bitte gib eine Beschreibung ein.")

with col2:
    st.subheader("🖼️ Vorschau")
    if 'current_img' in st.session_state:
        st.image(st.session_state.current_img, use_container_width=True)
        st.download_button("💾 DOWNLOAD", st.session_state.current_img, f"epocha_{int(time.time())}.png")
    else:
        st.info("Wähle eine KI und klicke auf Generieren.")

st.divider()
st.caption("Tipp: Wenn Nano Banana (530) überlastet ist, schalte auf 'Turbo Engine' um.")
        st.info("Dein generiertes Bild wird hier angezeigt.")
        st.image("https://via.placeholder.com/1280x720.png?text=Warte+auf+Generierung...", use_container_width=True)


