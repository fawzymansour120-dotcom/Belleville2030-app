import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="Mina's Belleville 2030", page_icon="🏗️", layout="wide")

# 2. تصميم الأزرار التفاعلية (الأكشن)
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

# 3. دالة جلب البيانات مع حماية ضد الأخطاء
def get_data():
    sheet_id = "1-iAlhlDViZ_dNIjRfv6PRTEA8RPI_YzSgwCvZGrlYeA"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        data = pd.read_csv(url)
        # التأكد من تنظيف المسافات في أسماء الأعمدة
        data.columns = [c.strip() for c in data.columns]
        return data
    except:
        # بيانات احتياطية في حال فشل الاتصال بالشيت
        return pd.DataFrame({
            'Mots': ['Paris', 'Manger', 'Calm'],
            'Type': ['N', 'v', 'adj'],
            'المعنى': ['باريس', 'يأكل', 'هادئ']
        })

df = get_data()

# 4. إدارة حالة الفلتر (الأكشن)
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = 'All'

# 5. الواجهة
st.title("Bonjour Mina ☕")
st.markdown("### 🇫🇷 Dashboard Interactif - Belleville")

# حساب الأعداد بأمان
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

# عرض الجدول النهائي
st.table(filtered_df)

if st.sidebar.button("🔄 Refresh"):
    st.rerun()
