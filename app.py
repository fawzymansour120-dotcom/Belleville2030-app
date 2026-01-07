import streamlit as st
import pandas as pd

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Belleville 2030", page_icon="🏗️", layout="wide")

# 2. منطق التبديل بين الـ Dark و Light Mode
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

MY_BLUE = "#2596be" 
MY_GREEN = "#24bf57" 

# 3. واجهة التنسيق (CSS) - تم إصلاح التداخل في الأقواس
if st.session_state.theme == 'light':
    bg_color = "#FFFFFF"; text_color = "#121212"; border_color = "#dee2e6"
else:
    bg_color = "#121212"; text_color = "#FFFFFF"; border_color = "#333333"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .stButton > button {{
        height: 100px !important;
        background-color: {MY_BLUE} !important;
        color: white !important;
        border: 1px solid {border_color} !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        border-radius: 15px !important;
    }}
    .header-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        background: {bg_color};
        padding: 10px 20px;
        border-radius: 50px;
        border: 2px solid {MY_BLUE};
        width: fit-content;
        margin-bottom: 20px;
    }}
    .dog-image {{
        width: 55px;
        height: 55px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid {MY_BLUE};
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. نظام الدخول
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>Bonjour 👋</h1>", unsafe_allow_html=True)
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

# 5. الهيدر (صورة الكلب من درايفك + الترحيب)
col_head, col_toggle = st.columns([0.8, 0.2])
with col_head:
    # تم إصلاح الرابط المباشر من جوجل درايف الخاص بك
    dog_id = "1702lVuPmDClSvkfvpdTwYJ5_aDpRvcQU"
    dog_url = f"https://lh3.googleusercontent.com/d/{dog_id}"
    st.markdown(f"""
        <div class="header-container">
            <img src="{dog_url}" class="dog-image">
            <span style="font-size: 1.3rem; font-weight: bold;">Bonjour, {st.session_state.user_name}</span>
        </div>
        """, unsafe_allow_html=True)

with col_toggle:
    label = "🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"
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

# 7. العدادات (إصلاح عرض الأرقام)
total = len(df)
noms = len(df[df['Type'].fillna('').str.contains('N', na=False)]) if 'Type' in df.columns else 0
verbes = len(df[df['Type'].fillna('').str.contains('v', na=False)]) if 'Type' in df.columns else 0
adjs = len(df[df['Type'].fillna('').str.contains('adj', na=False)]) if 'Type' in df.columns else 0

c1, c2, c3, c4 = st.columns(4)

def draw_button(label, val, key):
    is_active = st.session_state.filter == val
    btn_bg = MY_GREEN if is_active else MY_BLUE
    # استخدام ستايل منفصل لكل زر لتجنب تداخل الأقواس
    st.markdown(f"<style>div.stButton > button[key='{key}'] {{ background-color: {btn_bg} !important; }}</style>", unsafe_allow_html=True)
    if st.button(label, key=key):
        st.session_state.filter = val
        st.rerun()

with c1: draw_button(f"📖 TOTAL\n{total}", 'All', 'b1')
with c2: draw_button(f"🏛️ NOMS\n{noms}", 'N', 'b2')
with c3: draw_button(f"🚀 VERBES\n{verbes}", 'v', 'b3')
with c4: draw_button(f"🎨 ADJECTIFS\n{adjs}", 'adj', 'b4')

st.divider()

# 8. عرض الجدول (إصلاح الاختفاء)
f = st.session_state.filter
filtered_df = df if f == 'All' else df[df['Type'].fillna('').str.contains(f, na=False)]
st.dataframe(filtered_df, use_container_width=True)

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()
