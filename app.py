import streamlit as st
import pandas as pd

# إعداد الصفحة وتصميمها بشكل هندسي شيك
st.set_page_config(page_title="Mina's Belleville", page_icon="🏗️", layout="wide")

# تصميم CSS للمربعات (المنفصلة)
st.markdown("""
    <style>
    .metric-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #1e1e1e;
        border: 2px solid #4f8bf9;
        border-radius: 15px;
        padding: 20px;
        width: 30%;
        text-align: center;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.4);
    }
    .metric-label { font-size: 18px; color: #4f8bf9; font-weight: bold; margin-bottom: 10px; }
    .metric-value { font-size: 40px; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# رابط جوجل شيت
sheet_id = "1-iAlhlDViZ_dNIjRfv6PRTEA8RPI_YzSgwCvZGrlYeA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def load_data():
    try:
        return pd.read_csv(sheet_url)
    except:
        return pd.DataFrame(columns=["الكلمة", "النوع", "المعنى"])

df = load_data()

# العنوان
st.title("Bonjour Mina ☕")
st.markdown("#### Projet de Belleville 2030 - Vision Architecturale")
st.divider()

# العدادات في مربعات منفصلة (Cards)
n_mots = len(df)
n_noms = len(df[df['النوع'].str.contains('اسم', na=False)]) if not df.empty else 0
n_verbes = len(df[df['النوع'].str.contains('فعل', na=False)]) if not df.empty else 0

st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">📊 Mots (الكلمات)</div>
            <div class="metric-value">{n_mots}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🏛️ Noms (الأسماء)</div>
            <div class="metric-value">{n_noms}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🚀 Verbes (الأفعال)</div>
            <div class="metric-value">{n_verbes}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# البحث
search = st.text_input("🔍 Rechercher une expression... (ابحث هنا)")

if search:
    res = df[df['الكلمة'].str.contains(search, case=False, na=False) | 
             df['المعنى'].str.contains(search, case=False, na=False)]
    st.dataframe(res, use_container_width=True)
else:
    st.subheader("Ma Liste (قائمة كلماتي)")
    st.dataframe(df, use_container_width=True)

# زر التحديث في الجنب
if st.sidebar.button("🔄 Actualiser"):
    st.rerun()
