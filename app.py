import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="Mina's Belleville 2030", page_icon="🏗️", layout="wide")

# 2. نظام الباسورد (بوابة الدخول)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    st.markdown("<h2 style='text-align: center;'>Bonjour Mina ☕</h2>", unsafe_allow_html=True)
    password = st.text_input("Veuillez entrer le mot de passe (ادخل كلمة المرور)", type="password")
    if st.button("Entrer"):
        if password == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect (الباسورد غلط يا هندسة)")

# لو لسه مكلمش الدخول، يعرض صفحة الباسورد ويوقف الكود هنا
if not st.session_state.authenticated:
    check_password()
    st.stop()

# --- لو الباسورد صح، الكود اللي تحت ده هو اللي هيشتغل ---

# 3. تصميم الأزرار التفاعلية (CSS)
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        background-color: #161b22;
        color: #58a6ff;
        border: 2px solid #58a6ff;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #58a6ff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. دالة جلب البيانات من جوجل شيت
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

# 5. إدارة حالة الفلتر
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = 'All'

st.title("Bienvenue, Mina! 🏗️")
st.markdown("### 🇫🇷 Dashboard Interactif - Belleville 2030")
st.divider()

# حساب الأعداد
total = len(df)
noms = len(df[df['Type'].str.contains('N', na=False)]) if 'Type' in df.columns else 0
verbes = len(df[df['Type'].str.contains('v', na=False)]) if 'Type' in df.columns else 0
adjs = len(df[df['Type'].str.contains('adj', na=False)]) if 'Type' in df.columns else 0

# صف الأزرار (الأكشن)
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

# تصفية الجدول بناءً على الضغط
if st.session_state.filter_type == 'All':
    filtered_df = df
    st.subheader("Toute la liste (الكل)")
else:
    filtered_df = df[df['Type'].str.contains(st.session_state.filter_type, na=False)]
    st.subheader(f"Filtré par: {st.session_state.filter_type}")

# عرض الجدول
st.table(filtered_df)

if st.sidebar.button("🔄 Déconnexion / Logout"):
    st.session_state.authenticated = False
    st.rerun()
