import streamlit as st
import pandas as pd

# إعداد الصفحة وتنسيق الأبعاد
st.set_page_config(page_title="Mina's Belleville 2030", page_icon="🏗️", layout="wide")

# تصميم المربعات المنفصلة (CSS) - الأكشن اللي طلبته
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-card {
        background-color: #161b22;
        border: 2px solid #58a6ff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-label { font-size: 18px; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .metric-value { font-size: 38px; color: #ffffff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ربط ملف جوجل شيت (الرابط اللي بعتهولي)
sheet_id = "1-iAlhlDViZ_dNIjRfv6PRTEA8RPI_YzSgwCvZGrlYeA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def load_data():
    try:
        # استيراد البيانات وتجنب التخزين المؤقت لسرعة التحديث
        return pd.read_csv(sheet_url)
    except:
        return pd.DataFrame(columns=["Mots", "Type", "المعنى"])

df = load_data()

# واجهة المستخدم
st.title("Bonjour Mina ☕")
st.markdown("### 🇫🇷 Belleville 2030: Journal d'un Ingénieur")
st.divider()

# حساب العدادات بناءً على اختصاراتك (N, v, adj)
if not df.empty:
    mots_count = len(df)
    noms_count = len(df[df['Type'].str.strip() == 'N']) if 'Type' in df.columns else 0
    verbes_count = len(df[df['Type'].str.strip() == 'v']) if 'Type' in df.columns else 0
    adj_count = len(df[df['Type'].str.strip() == 'adj']) if 'Type' in df.columns else 0
else:
    mots_count = noms_count = verbes_count = adj_count = 0

# عرض المربعات في صف واحد منفصل
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">📊 Mots</div><div class="metric-value">{mots_count}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🏛️ Noms</div><div class="metric-value">{noms_count}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🚀 Verbes</div><div class="metric-value">{verbes_count}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🎨 Adjectifs</div><div class="metric-value">{adj_count}</div></div>', unsafe_allow_html=True)

st.divider()

# البحث الذكي
search_query = st.text_input("🔍 Rechercher (ابحث عن كلمة، نوع، أو معنى)...")

if search_query:
    # البحث في كل الخانات
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.subheader("Ma Liste Actuelle (قائمة الكلمات)")
    st.dataframe(df, use_container_width=True)

# زر تحديث البيانات
if st.sidebar.button("🔄 Actualiser"):
    st.rerun()
