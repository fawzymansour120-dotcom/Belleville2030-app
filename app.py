import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والهوية الشخصية
st.set_page_config(page_title="Belleville 2030", layout="wide")

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("Belleville 2030")
    # عرض الصورة الشخصية والترحيب المتفق عليه
    st.image("https://lh3.googleusercontent.com/u/0/d/1702IVuPmDCISvkfvp dTwYJ5_aDPrvcQU", width=100)
    st.markdown("### **Bonjour Mon Ami**") 
    st.write("---")
    st.info("Magazine Project Dashboard")

# 3. العنوان الرئيسي (المقولة الفرنسية)
st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-style: italic; color: #1e293b;">
        "Peut-être n'es-tu pas né sur cette terre, mais tu naitras là où tu apprendras."
        </h1>
    </div>
    """, unsafe_allow_html=True)

# 4. جلب البيانات من رابط جوجل شيت (CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RMpE1HR_rsgy9luptAHgD0DyTpD1uTYBTbTKNLOWYbI/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    try:
        # قراءة البيانات مع التعامل مع احتمالية وجود مسافات في أسماء الأعمدة
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

df = load_data()

# 5. عرض الإحصائيات البسيطة
if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Mots", len(df))
    # حساب الأنواع بناءً على عمود Type
    if 'Type' in df.columns:
        verbes = len(df[df['Type'].str.contains('Verbe', na=False, case=False)])
        noms = len(df[df['Type'].str.contains('Nom', na=False, case=False)])
        col2.metric("Verbes", verbes)
        col3.metric("Noms", noms)

    # 6. محرك البحث والجدول (تم إصلاح خطأ BadgeColumn)
    search = st.text_input("🔍 Rechercher un mot...")
    
    if search:
        df_display = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    else:
        df_display = df

    # استخدام عرض الجدول العادي لتجنب أخطاء التوافق
    st.dataframe(df_display, use_container_width=True, hide_index=True)

else:
    st.warning("⚠️ لا توجد بيانات. تأكد من أن جدول الإكسل يحتوي على بيانات صحيحة.")
