import streamlit as st
import pandas as pd

# 1. إعداد الصفحة وتصميم هندسي شيك
st.set_page_config(page_title="Mina's Belleville 2030", page_icon="🏗️", layout="wide")

# تصميم المربعات (CSS)
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e1e1e;
        border: 2px solid #4f8bf9;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.3);
    }
    .metric-label { font-size: 18px; color: #4f8bf9; font-weight: bold; }
    .metric-value { font-size: 35px; color: white; font-weight: bold; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط جوجل شيت (الرابط الخاص بك)
sheet_id = "1-iAlhlDViZ_dNIjRfv6PRTEA8RPI_YzSgwCvZGrlYeA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def load_data():
    try:
        # إلغاء التخزين المؤقت لضمان تحديث البيانات فوراً
        return pd.read_csv(sheet_url)
    except:
        return pd.DataFrame(columns=["Mots", "Type", "المعنى"])

df = load_data()

# 3. واجهة التطبيق
st.title("Bonjour Mina ☕")
st.markdown("#### Magazine Belleville - Progrès Linguistique")
st.divider()

# 4. حساب العدادات بناءً على الرموز في الشيت (N, v, adj)
total_mots = len(df)
# البحث عن حرف N (اسم) أو v (فعل) أو adj (صفة) في عمود Type
n_noms = len(df[df['Type'].str.contains('N', case=False, na=False)]) if not df.empty else 0
n_verbes = len(df[df['Type'].str.contains('v', case=False, na=False)]) if not df.empty else 0
n_adj = len(df[df['Type'].str.contains('adj', case=False, na=False)]) if not df.empty else 0

# عرض المربعات في 4 أعمدة (إضافة الصفات)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">📊 Mots</div><div class="metric-value">{total_mots}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🏛️ Noms (N)</div><div class="metric-value">{n_noms}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🚀 Verbes (v)</div><div class="metric-value">{n_verbes}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">🎨 Adjectifs</div><div class="metric-value">{n_adj}</div></div>', unsafe_allow_html=True)

st.divider()

# 5. محرك البحث والجدول
search = st.text_input("🔍 Rechercher une expression... (ابحث عن كلمة)")

if search:
    # البحث في كل الأعمدة
    mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
    st.table(df[mask])
else:
    st.subheader("Dictionnaire personnel (قاموسك الشخصي)")
    st.dataframe(df, use_container_width=True)

# زر تحديث في القائمة الجانبية
if st.sidebar.button("🔄 Actualiser (تحديث)"):
    st.rerun()
