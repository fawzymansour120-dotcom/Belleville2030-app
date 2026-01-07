import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="Mina's Belleville 2030", page_icon="🏗️", layout="wide")

# 2. تصميم CSS للألوان والأكشن (المحور الجمالي)
st.markdown("""
    <style>
    /* تصميم زر الدخول */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #4f8bf9, #2b5cb7);
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(79, 139, 249, 0.4);
    }
    /* تصميم اسم المستخدم أعلى اليسار */
    .user-greeting {
        position: absolute;
        top: -50px;
        left: 0;
        color: #58a6ff;
        font-weight: bold;
        font-size: 18px;
    }
    /* تنسيقات المربعات التفاعلية */
    .metric-btn {
        border: 2px solid #58a6ff;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام الدخول المتطور
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

def login_page():
    st.markdown("<h1 style='text-align: center;'>Bonjour 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Veuillez entrer vos معلومات (من فضلك أدخل بياناتك)</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("ادخل اسمك الأول (Prénom)")
        password = st.text_input("ادخل الباسورد (Mot de passe)", type="password")
        
        if st.button("Entrer 🚀"):
            if password == "1234" and name.strip() != "":
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.rerun()
            elif name.strip() == "":
                st.warning("من فضلك اكتب اسمك الأول")
            else:
                st.error("الباسورد غير صحيح يا هندسة")

if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- الكود بعد الدخول بنجاح ---

# عرض الترحيب أعلى اليسار
st.markdown(f"<div class='user-greeting'>👤 Bonjour, {st.session_state.user_name}</div>", unsafe_allow_html=True)

# 4. دالة جلب البيانات
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

# إدارة الفلتر
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = 'All'

st.title("Belleville 2030 🏗️")
st.divider()

# حساب الأعداد
total = len(df)
noms = len(df[df['Type'].str.contains('N', na=False)]) if 'Type' in df.columns else 0
verbes = len(df[df['Type'].str.contains('v', na=False)]) if 'Type' in df.columns else 0
adjs = len(df[df['Type'].str.contains('adj', na=False)]) if 'Type' in df.columns else 0

# صف الأزرار التفاعلية
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

# تصفية وعرض البيانات
if st.session_state.filter_type == 'All':
    filtered_df = df
    st.subheader("Dictionnaire complet")
else:
    filtered_df = df[df['Type'].str.contains(st.session_state.filter_type, na=False)]
    st.subheader(f"Catégorie: {st.session_state.filter_type}")

st.table(filtered_df)

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()
