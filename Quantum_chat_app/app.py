import streamlit as st
import websocket
from websocket import create_connection
import json
from encrypt_message import encrypt, decrypt
from bb84_protocol import generate_key
import urllib.parse 
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="SANDESH - Quantum Secure", layout="wide")

# --- ROYAL CALLIGRAPHY & ANCIENT GOLDEN CSS (100% UNTOUCHED) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Pinyon+Script&family=Cinzel:wght@400;700&display=swap');

    .stApp {
        background: radial-gradient(circle, #2c1e14 0%, #0e0906 100%);
        color: #d4af37; 
        font-family: 'Cinzel', serif; 
    }

    div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    h1 {
        font-family: 'Cinzel Decorative', cursive !important;
        color: #fcf6ba !important;
        text-shadow: 3px 3px 15px rgba(191, 149, 63, 0.9) !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 12px !important;
        border-bottom: 2px double #bf953f;
        padding-bottom: 20px;
        font-weight: 900 !important;
    }
    
    h2, h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        color: #bf953f !important;
        letter-spacing: 4px !important;
    }

    .stAlert {
        background-color: #000000 !important;
        color: #fcf6ba !important;
        border: 1px solid #bf953f !important;
        border-radius: 4px !important;
        font-family: 'Pinyon Script', cursive !important;
        font-size: 1.8em !important;
    }
    
    .stAlert div, .stAlert p { color: #fcf6ba !important; }

    .stButton>button {
        background: linear-gradient(145deg, #bf953f, #fcf6ba, #b38728) !important;
        color: #1a0f00 !important;
        border: 1px solid #7d5e1a !important;
        font-family: 'Cinzel', serif !important;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8) !important;
    }

    .stTextInput>div>div>input {
        background-color: #0e0906 !important;
        color: #fcf6ba !important;
        border-bottom: 2px solid #bf953f !important;
        border-top: none !important; border-left: none !important; border-right: none !important;
    }

    [data-testid="stSidebar"] h3 {
        font-family: 'Pinyon Script', cursive !important;
        font-size: 2.8em !important;
        color: #fcf6ba !important;
    }

    .chat-container b {
        font-family: 'Pinyon Script', cursive !important;
        font-size: 2.2em !important;
        color: #fcf6ba !important;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("⚜️ SANDESH ⚜️")
st.write("<p style='text-align:center; opacity:0.9; font-family:\"Pinyon Script\", cursive; font-size: 2.2em; color:#fcf6ba;'>The Divine Laws of Subatomic Encryption</p>", unsafe_allow_html=True)
st.divider()

# --- 1. SESSION STATE ---
if "ws" not in st.session_state: st.session_state["ws"] = None
if "key" not in st.session_state: st.session_state["key"] = None
if "chat_history" not in st.session_state: st.session_state["chat_history"] = []

# --- 2. SIDEBAR (CONFIG & VAULT RECOVERY) ---
with st.sidebar:
    st.markdown("### 🏛️ Sandesh Gateway")
    
    user_name = st.text_input("Thy Name (User):", value="Scribe")
    server_ip = st.text_input("Server Portal (IP / Ngrok):", value="https://bifoliate-tyree-tumulous.ngrok-free.dev")
    room_id = st.text_input("Chamber ID:")
    passcode = st.text_input("Seal Passcode:", type="password")
    
    if st.button("OPEN CHAMBER"):
        if room_id and passcode and server_ip:
            try:
                safe_passcode = urllib.parse.quote(passcode.strip())
                ip_input = server_ip.strip()
                
                # --- SMART URL PARSER (Handles Ngrok & Local) ---
                if "ngrok" in ip_input:
                    clean_ip = ip_input.replace("https://", "").replace("http://", "").strip("/")
                    target_url = f"wss://{clean_ip}/ws/{room_id.strip()}?passcode={safe_passcode}"
                else:
                    target_url = f"ws://{ip_input}:8000/ws/{room_id.strip()}?passcode={safe_passcode}"
                
                # --- NGROK WARNING BYPASS HEADERS ---
                custom_headers = {
                    "ngrok-skip-browser-warning": "true",
                    "User-Agent": "Mozilla/5.0"
                }
                
                ws = create_connection(target_url, header=custom_headers)
                st.session_state["ws"] = ws
                
                # --- AUTOMATIC VAULT RECOVERY (MONGODB) ---
                st.session_state["chat_history"] = [] 
                ws.settimeout(0.5) 
                try:
                    while True:
                        msg = ws.recv()
                        parsed = json.loads(msg)
                        if parsed.get("type") == "message":
                            st.session_state["chat_history"].append({
                                "sender": parsed.get("sender", "Partner"), 
                                "encrypted": parsed.get("data", ""),
                                "original": "[RECOVERED SANDESH]", 
                                "display_name": parsed.get("sender", "Partner")
                            })
                except Exception:
                    pass 
                
                st.success(f"Chamber Sealed for {user_name} ✅")
            except Exception as e:
                # St.error mein error message bhi dikhayenge takki debug asaan ho
                st.error(f"Access Denied: Chamber Seal Broken. ({str(e)})")

    st.divider()
    eve_mode = st.checkbox("Invoke Cursed Interference (Eve)")
    
    if st.session_state["key"]:
        st.markdown("<p style='color:#fcf6ba; font-family:\"Pinyon Script\", cursive; font-size:1.5em;'>The Key is Secured</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#7d5e1a; font-family:\"Pinyon Script\", cursive; font-size:1.5em;'>The Key is Missing</p>", unsafe_allow_html=True)

# --- 3. QUANTUM KEY PHASE ---
st.header("I. The Gilded Exchange")
col1, col2 = st.columns(2)

with col1:
    if st.button("CAST QUANTUM BITS"):
        if st.session_state["ws"]:
            key_bits = generate_key()
            key = ''.join(map(str, key_bits))
            if not eve_mode: st.session_state["key"] = key
            payload = json.dumps({"type": "key", "data": key, "eve_active": eve_mode, "sender": user_name})
            st.session_state["ws"].send(payload)
            st.info("Bits have been cast into the infinite void.")
        else:
            st.error("Chamber sync required.")

with col2:
    if st.button("DIVINE THE STATE"):
        if st.session_state["ws"]:
            st.session_state["ws"].settimeout(1.0)
            try:
                parsed = json.loads(st.session_state["ws"].recv())
                if parsed.get("type") == "key":
                    if parsed.get("eve_active", False):
                        st.error("The Key has collapsed into Dust (Eve Detected).")
                        st.session_state["key"] = None
                    else:
                        st.session_state["key"] = parsed.get("data")
                        st.success(f"Key Sync Complete with {parsed.get('sender', 'Partner')}")
                elif parsed.get("type") == "message":
                    st.session_state["chat_history"].append({
                        "sender": parsed.get("sender", "Partner"), 
                        "encrypted": parsed.get("data", "")
                    })
                    st.rerun()
            except websocket.WebSocketTimeoutException:
                st.info("The void remains silent.")
            except Exception as e:
                st.error(f"Sync Error: {str(e)}")

st.divider()

# --- 4. SECURE TERMINAL ---
st.header("II. The Golden Parchment")
message = st.text_input("Inscribe your Truth:")

if st.button("SEAL & DISPATCH"):
    if st.session_state["key"] and st.session_state["ws"] and message:
        try:
            enc = encrypt(message, st.session_state["key"])
            payload = json.dumps({"type": "message", "data": enc, "sender": user_name})
            st.session_state["ws"].send(payload)
            st.session_state["chat_history"].append({
                "sender": "You", 
                "original": message, 
                "encrypted": enc,
                "display_name": user_name
            })
            st.success("Sandesh has been Sealed.")
        except ValueError as e:
            st.error(f"Alchemy Error: {e}")
    else:
        st.error("QKD synchronization required.")

# --- 5. DATA LOGS (CRASH PROOF) ---
st.subheader("> The Chronicles")
for chat in st.session_state["chat_history"]:
    t = datetime.now().strftime("%H:%M")
    
    chat_sender = chat.get("sender", "Unknown")
    chat_encrypted = chat.get("encrypted", "ERROR_NO_CIPHER")
    chat_original = chat.get("original", "")
    chat_display_name = chat.get("display_name", user_name)
    
    trim_cipher = chat_encrypted[:30] + "..." if len(chat_encrypted) > 30 else chat_encrypted

    if chat_sender == "You":
        st.markdown(f"""
        <div class="chat-container">
            <span style="opacity:0.6; font-size:0.8em;">{t}</span> 
            <b style="color:#fcf6ba;">{chat_display_name} (You)</b> : <span style="font-family:'Cinzel', serif;">{chat_original}</span><br>
            <span style="color:#7d5e1a; font-size:0.8em; font-family:monospace;">SEAL: {trim_cipher}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.session_state["key"]:
            try:
                dec = decrypt(chat_encrypted, st.session_state["key"])
                st.markdown(f"""
                <div class="chat-container">
                    <span style="opacity:0.6; font-size:0.8em;">{t}</span> 
                    <b style="color:#fcf6ba;">{chat_sender}</b> : <span style="font-family:'Cinzel', serif;">{dec}</span><br>
                    <span style="color:#7d5e1a; font-size:0.8em; font-family:monospace;">SEAL: {trim_cipher}</span>
                </div>
                """, unsafe_allow_html=True)
            except Exception:
                st.markdown(f"""
                <div class="chat-container">
                    <span style="opacity:0.6; font-size:0.8em;">{t}</span> 
                    <b style="color:#fcf6ba;">{chat_sender}</b> : <i style="color:#ff4b4b; font-family:'Cinzel', serif;">[INTEGRITY COMPROMISED - VAULT DATA]</i><br>
                    <span style="color:#7d5e1a; font-size:0.8em; font-family:monospace;">SEAL: {trim_cipher}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-container">
                <span style="opacity:0.6; font-size:0.8em;">{t}</span> 
                <b style="color:#7d5e1a;">{chat_sender}</b> : <i style="font-family:'Cinzel', serif;">Sealed Sandesh - Key Unknown</i>
            </div>
            """, unsafe_allow_html=True)