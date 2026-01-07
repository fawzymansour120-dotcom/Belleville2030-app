import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="Belleville 2030", page_icon="🏗️", layout="wide")

# 2. التنسيق الجمالي (CSS) - تم إصلاح علامات التنصيص
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    
    /* تصميم زر الدخول الزاهي */
    div.stButton > button[kind="primary"] {
        background: #007bff !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border-radius: 30px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4) !important;
        width: 100% !important;
    }

    /* تصميم الزراير الأربعة */
    div.stButton > button {
        width: 100% !important;
        height: 120px !important;
        background-color: #1a2a3a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
    }

    /* الهيدر الشخصي */
    .profile-section {
        display: flex;
        align-items: center;
        background: #1a1a1a;
        padding: 8px 15px;
        border-radius: 30px;
        border: 1px solid #333;
        width: fit-content;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام الدخول
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #d4af37; font-weight: 200; letter-spacing: 3px;'>BELLEVILLE 2030</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        name = st.text_input("Prénom")
        password = st.text_input("Mot de passe", type="password")
        if st.button("SE CONNECTER 🚀", kind="primary"):
            if password == "1234" and name.strip() != "":
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.rerun()
    st.stop()

# --- واجهة المستخدم الداخلية ---
gemini_pic = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530393333333333.svg"
st.markdown(f"""
    <div class="profile-section">
        <img src="{gemini_pic}" style="width:25px; margin-right:10px;">
        <span style="color:#d4af37; font-weight:bold;">Bonjour, {st.session_state.user_name}</span>
    </div>
    """, unsafe_allow_html=True)

# جلب البيانات بأمان
@st.cache_data(ttl=30)
def get_data():
    sheet_id = "1-iAlhlDViZ_dNIjRfv6PRTEA8RPI_YzSgwCvZGrlYeA"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [c.strip() for c in data.columns]
        return data
    except:
        return pd.DataFrame(columns=["Mots", "Type", "المعنى"])

df = get_data()

if 'filter' not in st.session_state: st.session_state.filter = 'All'

st.markdown("<h1 style='color: white; font-weight: 200;'>Archives du Projet</h1>", unsafe_allow_html=True)
st.divider()

# حساب العدادات
total = len(df)
noms = len(df[df['Type'].str.contains('N', na=False)]) if 'Type' in df.columns else 0
verbes = len(df[df['Type'].str.contains('v', na=False)]) if 'Type' in df.columns else 0
adjs = len(df[df['Type'].str.contains('adj', na=False)]) if 'Type' in df.columns else 0

# المربعات الأربعة
c1, c2, c3, c4 = st.columns(4)

def btn_logic(label, filter_val, key):
    is_active = st.session_state.filter == filter_val
    bg = "#28a745" if is_active else "#1a2a3a"
    st.markdown(f"""
        <style>
        div.stButton > button[key="{key}"] {{
            background-color: {bg} !important;
            border: {"2px solid white" if is_active else "1px solid #333"} !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    if st.button(label, key=key):
        st.session_state.filter = filter_val
        st.rerun()

with c1: btn_logic(f"📖\nTOTAL\n{total}", 'All', 'btn_all')
with c2: btn_logic(f"🏛️\nNOMS\n{noms}", 'N', 'btn_n')
with c3: btn_logic(f"🚀\nVERBES\n{verbes}", 'v', 'btn_v')
with c4: btn_logic(f"🎨\nADJECTIFS\n{adjs}", 'adj', 'btn_adj')

st.divider()

# عرض النتائج
f = st.session_state.filter
filtered_df = df if f == 'All' else df[df['Type'].str.contains(f, na=False)]
st.table(filtered_df)

if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()
