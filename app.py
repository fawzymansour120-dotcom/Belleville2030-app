import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="Belleville 2030", layout="wide")

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("Belleville 2030")
    # صورة البروفايل مع أيقونة التعديل والترحيب الشخصي
    st.image("https://lh3.googleusercontent.com/u/0/d/1702IVuPmDCISvkfvp dTwYJ5_aDPrvcQU", width=80)
    st.markdown("### **Bonjour Mon Ami**") 
    st.write("---")
    st.write("Magazine Project Dashboard")

# 3. العنوان الرئيسي (المقولة الفلسفية)
st.markdown("""
    <h2 style='font-style: italic; color: #1e293b; text-align: center;'>
    "Peut-être n'es-tu pas né sur cette terre, mais tu naitras là où tu apprendras."
    </h2>
    """, unsafe_allow_html=True)

# 4. جلب البيانات من رابط جوجل شيت (CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RMpE1HR_rsgy9luptAHgD0DyTpD1uTYBTbTKNLOWYbI/export?format=csv"

@st.cache_data(ttl=600) # تحديث البيانات كل 10 دقائق
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # التأكد من مطابقة أسماء الأعمدة لجدولك
        return df
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return pd.DataFrame()

df = load_data()

# 5. عرض الإحصائيات (Statistiques)
if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Mots", len(df))
    col2.metric("Verbes", len(df[df['Type'].str.contains('Verbe', na=False, case=False)]))
    col3.metric("Noms", len(df[df['Type'].str.contains('Nom', na=False, case=False)]))

    # 6. محرك البحث والجدول
    search = st.text_input("🔍 Rechercher un mot...")
    
    if search:
        df_display = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    else:
        df_display = df

    st.dataframe(
        df_display,
        column_config={
            "Mot": "Mot (Word)",
            "Type": st.column_config.BadgeColumn("Type"),
            "Traduction": "Traduction (Arabic)",
            "Contexte": "Contexte (Example)"
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.warning("⚠️ لا توجد بيانات حالياً. تأكد من إدخال كلمات في جدول الإكسل.")
