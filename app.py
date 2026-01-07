import streamlit as st
import pandas as pd

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Belleville 2030", page_icon="🏗️", layout="wide")

# 2. منطق التبديل بين الـ Dark و Light Mode
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# 3. واجهة التنسيق (CSS ديناميكي يتغير حسب اختيارك)
if st.session_state.theme == 'light':
    bg_color = "#FFFFFF"
    text_color = "#121212"
    card_bg = "#f8f9fa"
    border_color = "#dee2e6"
else:
    bg_color = "#121212"
    text_color = "#FFFFFF"
    card_bg = "#1a2a3a"
    border_color = "#333333"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    h1, h2, p, span {{ color: {text_color} !important; }}
    
    /* تصميم زر الدخول */
    div.stButton > button:first-child {{
        background-color: #007bff !important;
        color: white !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
    }}

    /* أزرار الفلتر الأربعة */
    .stButton > button {{
        height: 100px !important;
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        font-weight: 900 !important;
        font-size: 20px !important;
    }}

    /* الهيدر الشخصي */
    .header-container {{
        display: flex;
        align-items: center;
        gap: 12px;
        background: {card_bg};
        padding: 8px 15px;
        border-radius: 30px;
        border: 1px solid {border_color};
        width: fit-content;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. نظام الدخول
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>Bonjour 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37;'>BELLEVILLE 2030</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        name = st.text_input("Prénom")
        password = st.text_input("Mot de passe", type="password")
        if st.button("SE CONNECTER 🚀"):
            if password == "1234" and name.strip() != "":
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.rerun()
    st.stop()

# 5. الهيدر الداخلي (Bonjour + زر الـ Dark Mode)
col_head, col_toggle = st.columns([0.8, 0.2])

with col_head:
    gemini_pic = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530393333333333.svg"
    st.markdown(f"""
        <div class="header-container">
            <img src="{gemini_pic}" style="width:30px;">
            <span style="font-weight:bold;">Bonjour, {st.session_state.user_name}</span>
        </div>
        """, unsafe_allow_html=True)

with col_toggle:
    label = "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"
    if st.button(label):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.rerun()

# 6. جلب البيانات
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

st.markdown("<h1>Archives du Projet</h1>", unsafe_allow_html=True)
st.divider()

# 7. العدادات والفلترة
total = len(df)
noms = len(df[df['Type'].fillna('').str.contains('N', na=False)]) if 'Type' in df.columns else 0
verbes = len(df[df['Type'].fillna('').str.contains('v', na=False)]) if 'Type' in df.columns else 0
adjs = len(df[df['Type'].fillna('').str.contains('adj', na=False)]) if 'Type' in df.columns else 0

c1, c2, c3, c4 = st.columns(4)

def draw_button(label, val, key):
    is_active = st.session_state.filter == val
    # اللون الأخضر يظهر فقط عند التفعيل، وإلا يتبع الثيم
    btn_bg = "#28a745" if is_active else card_bg
    btn_text = "white" if is_active else text_color
    st.markdown(f"<style>div.stButton > button[key='{key}'] {{ background-color: {btn_bg} !important; color: {btn_text} !important; }}</style>", unsafe_allow_html=True)
    if st.button(label, key=key):
        st.session_state.filter = val
        st.rerun()

with c1: draw_button(f"📖\nTOTAL\n{total}", 'All', 'b1')
with c2: draw_button(f"🏛️\nNOMS\n{noms}", 'N', 'b2')
with c3: draw_button(f"🚀\nVERBES\n{verbes}", 'v', 'b3')
with c4: draw_button(f"🎨\nADJECTIFS\n{adjs}", 'adj', 'b4')

st.divider()

# 8. عرض الجدول
f = st.session_state.filter
filtered_df = df if f == 'All' else df[df['Type'].fillna('').str.contains(f, na=False)]
st.dataframe(filtered_df, use_container_width=True)

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()
