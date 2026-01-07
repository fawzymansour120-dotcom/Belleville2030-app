import streamlit as st
import pandas as pd

# 1. إعداد الصفحة والخطوط
st.set_page_config(page_title="Mina's Belleville 2030", page_icon="🏗️", layout="wide")

# 2. المحور الجمالي: CSS للألوان والأكشن والخطوط
st.markdown("""
    <style>
    /* تغيير الخط العام */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* تصميم الأزرار الأربعة مع تأثير التوهج عند الوقوف عليها */
    div.stButton > button {
        width: 100%;
        height: 100px; /* التحكم في حجم المربع */
        background-color: #161b22;
        color: #58a6ff;
        border: 2px solid #30363d;
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }

    /* الأكشن: التوهج بلون مختلف عند الوقوف على الزر */
    div.stButton > button:hover {
        border-color: #00d4ff; /* لون فسفوري */
        color: #ffffff;
        box-shadow: 0 0 15px #00d4ff; /* تأثير التوهج */
        transform: translateY(-5px); /* حركة خفيفة للأعلى */
    }

    /* تصميم زر تسجيل الدخول */
    .stTextInput>div>div>input {
        border-radius: 10px;
    }

    /* صورة البروفايل */
    .header-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px;
        background: #161b22;
        border-radius: 50px;
        width: fit-content;
        border: 1px solid #30363d;
    }
    .profile-pic {
        width: 35px;
        height: 35px;
        border-radius: 50%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام الدخول
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>Bonjour 👋</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        name = st.text_input("Prénom")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            if password == "1234" and name.strip() != "":
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.rerun()
    st.stop()

# --- بعد الدخول ---
# الهيدر الشخصي
gemini_pic = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530393333333333.svg"
st.markdown(f"""
    <div class="header-container">
        <img src="{gemini_pic}" class="profile-pic">
        <span style="color:white; font-weight:bold;">Bonjour, {st.session_state.user_name}</span>
    </div>
    """, unsafe_allow_html=True)

# جلب البيانات
@st.cache_data(ttl=60) # تحديث كل دقيقة
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

if 'filter_type' not in st.session_state:
    st.session_state.filter_type = 'All'

st.title("Belleville 2030 🏗️")
st.divider()

# حساب العدادات
total = len(df)
noms = len(df[df['Type'].str.contains('N', na=False)]) if 'Type' in df.columns else 0
verbes = len(df[df['Type'].str.contains('v', na=False)]) if 'Type' in df.columns else 0
adjs = len(df[df['Type'].str.contains('adj', na=False)]) if 'Type' in df.columns else 0

# المربعات الأربعة التفاعلية
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button(f"📊 Mots\n{total}"): st.session_state.filter_type = 'All'
with c2:
    if st.button(f"🏛️ Noms\n{noms}"): st.session_state.filter_type = 'N'
with c3:
    if st.button(f"🚀 Verbes\n{verbes}"): st.session_state.filter_type = 'v'
with c4:
    if st.button(f"🎨 Adjs\n{adjs}"): st.session_state.filter_type = 'adj'

st.divider()

# عرض النتائج
if st.session_state.filter_type == 'All':
    filtered_df = df
else:
    filtered_df = df[df['Type'].str.contains(st.session_state.filter_type, na=False)]

st.table(filtered_df)

if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()
