import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="Mina's Belleville", page_icon="🏗️", layout="wide")

# 2. التنسيق الجمالي (CSS المضمون)
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    
    /* تنسيق زر الدخول الأزرق */
    div.stButton > button:first-child {
        background-color: #007bff !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        height: 45px !important;
        font-weight: bold !important;
    }

    /* تنسيق أزرار الفلتر الأربعة */
    .filter-btn > div > button {
        height: 100px !important;
        background-color: #1a2a3a !important;
        color: white !important;
        border: 1px solid #333 !important;
        font-weight: bold !important;
        font-size: 18px !important;
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
    st.markdown("<h1 style='text-align: center; color: white; margin-bottom:0;'>Bonjour 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37; letter-spacing: 2px; margin-top:0;'>BELLEVILLE 2030</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        name = st.text_input("Prénom", key="login_name")
        password = st.text_input("Mot de passe", type="password", key="login_pass")
        if st.button("SE CONNECTER 🚀"):
            if password == "1234" and name.strip() != "":
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()

# --- واجهة المستخدم الداخلية ---
# الهيدر وصورة البروفايل
gemini_pic = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530393333333333.svg"
st.markdown(f"""
    <div class="profile-section">
        <img src="{gemini_pic}" style="width:25px; margin-right:10px;">
        <span style="color:#d4af37; font-weight:bold;">Bonjour, {st.session_state.user_name}</span>
    </div>
    """, unsafe_allow_html=True)

# جلب البيانات مع معالجة الخطأ KeyError
@st.cache_data(ttl=30)
def get_data():
    sheet_id = "1-iAlhlDViZ_dNIjRfv6PRTEA8RPI_YzSgwCvZGrlYeA"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [c.strip() for c in data.columns]
        return data
    except Exception as e:
        return pd.DataFrame(columns=["Mots", "Type", "المعنى"])

df = get_data()

# التأكد من وجود عمود Type لتجنب الخطأ الأحمر
if "Type" not in df.columns:
    st.error("Attention: Le colonne 'Type' est انت مسميتش العمود في الشيت Type")
    st.stop()

if 'filter' not in st.session_state: st.session_state.filter = 'All'

st.markdown("<h1 style='color: white; font-weight: 200;'>Archives du Projet</h1>", unsafe_allow_html=True)
st.divider()

# حساب العدادات بأمان
total = len(df)
noms = len(df[df['Type'].fillna('').str.contains('N')])
verbes = len(df[df['Type'].fillna('').str.contains('v')])
adjs = len(df[df['Type'].fillna('').str.contains('adj')])

# المربعات الأربعة
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button(f"📖\nTOTAL\n{total}", key="all"): st.session_state.filter = 'All'; st.rerun()
with c2:
    if st.button(f"🏛️\nNOMS\n{noms}", key="n"): st.session_state.filter = 'N'; st.rerun()
with c3:
    if st.button(f"🚀\nVERBES\n{verbes}", key="v"): st.session_state.filter = 'v'; st.rerun()
with c4:
    if st.button(f"🎨\nADJECTIFS\n{adjs}", key="adj"): st.session_state.filter = 'adj'; st.rerun()

st.divider()

# عرض الجدول
f = st.session_state.filter
filtered_df = df if f == 'All' else df[df['Type'].fillna('').str.contains(f)]
st.table(filtered_df)

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()
