import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Belleville 2030", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.title("Belleville 2030")
    st.image("https://lh3.googleusercontent.com/u/0/d/1702IVuPmDCISvkfvp dTwYJ5_aDPrvcQU", width=80)
    st.markdown("### **Bonjour Mon Ami**")
    st.write("---")
    st.info("Magazine Project Dashboard")

# العنوان الرئيسي الفلسفي
st.markdown("<h2 style='font-style: italic; color: #1e293b; text-align: center;'>\"Peut-être n'es-tu pas né sur cette terre, mais tu naitras là où tu apprendras.\"</h2>", unsafe_allow_html=True)

# جلب البيانات
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RMpE1HR_rsgy9luptAHgD0DyTpD1uTYBTbTKNLOWYbI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# دالة لإضافة الألوان بناءً على نوع الكلمة (نفس ألوان الصورة)
def color_type(val):
    if str(val).lower() == 'verbe': color = '#dcfce7; color: #166534' # أخضر
    elif str(val).lower() == 'nom': color = '#e0f2fe; color: #075985' # أزرق
    elif str(val).lower() == 'adjectif': color = '#f3e8ff; color: #6b21a8' # بنفسجي
    else: color = '#f1f5f9; color: #475569' # رمادي
    return f'background-color: {color}; border-radius: 12px; padding: 2px 10px; font-weight: bold;'

if not df.empty:
    # إحصائيات سريعة
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Mots", len(df))
    c2.metric("Verbes", len(df[df['Type'].str.contains('Verbe', na=False, case=False)]))
    c3.metric("Noms", len(df[df['Type'].str.contains('Nom', na=False, case=False)]))

    search = st.text_input("🔍 Rechercher un mot...")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    # تطبيق الألوان وعرض الجدول
    styled_df = df.style.applymap(color_type, subset=['Type'])
    st.table(styled_df) # استخدمنا st.table لعرض الألوان بشكل ثابت وواضح

else:
    st.warning("⚠️ لا توجد بيانات في الجدول.")
