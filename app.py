import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="Mina's Belleville 2030", page_icon="🏗️", layout="wide")

# تصميم المربعات كأزرار تفاعلية (CSS)
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        background-color: #161b22;
        color: white;
        border: 2px solid #58a6ff;
        border-radius: 15px;
        padding: 20px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #58a6ff;
        color: black;
        border-color: white;
    }
    .metric-label { font-size: 16px; font-weight: bold; margin-bottom: 5px; }
    .metric-value { font-size: 32px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ربط جوجل شيت
sheet_id = "1-iAlhlDViZ_dNIjRfv6PRTEA8RPI_YzSgwCvZGrlYeA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def load_data():
    try:
        return pd.read_csv(sheet_url)
    except:
        return pd.DataFrame(columns=["Mots", "Type", "المعنى"])

df = load_data()

# عنوان التطبيق
st.title("Bonjour Mina ☕")
st.markdown("### 🇫🇷 Dashboard Interactif - Belleville")

# حالة العرض (عشان الأكشن)
if 'filter' not in st.session_state:
    st.session_state.filter = 'All'

# حساب العدادات
total = len(df)
noms = len(df[df['Type'].str.strip() == 'N']) if not df.empty else 0
verbes = len(df[df['Type'].str.strip() == 'v']) if not df.empty else 0
adjs = len(df[df['Type'].str.strip() == 'adj']) if not df.empty else 0

# عرض المربعات كأزرار (هنا الأكشن اللي طلبته)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(f"📊 Mots\n{total}"): st.session_state.filter = 'All'
with col2:
    if st.button(f"🏛️ Noms (N)\n{noms}"): st.session_state.filter = 'N'
with col3:
    if st.button(f"🚀 Verbes (v)\n{verbes}"): st.session_state.filter = 'v'
with col4:
    if st.button(f"🎨 Adjs (adj)\n{adjs}"): st.session_state.filter = 'adj'

st.divider()

# تطبيق الفلتر بناءً على الزرار اللي اتضغط
if st.session_state.filter == 'All':
    display_df = df
    label = "Tous les mots (الكل)"
else:
    display_df = df[df['Type'].str.strip() == st.session_state.filter]
    label = f"Filtré par: {st.session_state.filter}"

# محرك البحث والجدول
st.subheader(label)
search = st.text_input("🔍 Rechercher...")

if search:
    mask = display_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
    st.table(display_df[mask])
else:
    st.table(display_df)

# زر التحديث
if st.sidebar.button("🔄 Actualiser"):
    st.rerun()
