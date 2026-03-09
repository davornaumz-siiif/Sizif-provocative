import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACIJA ---
# Ova linija kaže: "Uzmi ključ iz tajnog sefa koji sam podesio"
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Sizif ne vidi ključ u sefu: {e}")

# --- 2. DIZAJN (DARK MODE) ---
st.set_page_config(page_title="Sizif.ai", page_icon="🗿")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #d0d0d0; }
    h1 { color: #ff4b4b; text-align: center; font-family: monospace; }
    .stChatMessage { border: 1px solid #333; background-color: #111 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🗿 SIZIF.AI: PROVOKATIV")

# --- 3. LOGIKA ČETA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sedi. O čemu danas lažeš sebe?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Tvoj odgovor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            instr = "Ti si Sizif Provokator. Koristi Columbo metod. Postavi jedno drsko pitanje. Bez saveta."
            response = model.generate_content(f"{instr}\nKorisnik kaže: {prompt}")
            
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Tehnička greška: {e}")