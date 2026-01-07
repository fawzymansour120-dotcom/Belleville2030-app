import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Belleville 2030", layout="wide")

# 2. تنسيق CSS مخصص للزراير (الكروت) والنص الفلسفي
st.markdown("""
    <style>
    /* تنسيق النص الفلسفي */
    .quote-text {
        font-family: 'Georgia', serif;
        font-style: italic;
        color: #1e293b;
        text-align: center;
        font-size: 1.4rem !important;
        margin: 20px 0;
        border-left: 5px solid #24bf57;
        padding: 10px;
        background-color: #f8fafc;
    }
    /* تنسيق الكروت (الزراير) */
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-bottom: 5px solid #2596be;
    }
    .stat-value { font-size: 2rem; font-weight: bold; color: #1e293b; }
    .stat-label { color: #64748b; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("Belleville 2030")
    st.image("https://lh3.googleusercontent.com/u/0/d/1702IVuPmDCISvkfvpdTwYJ5_aDPrvcQU", width=80)
    st.markdown("### **Bonjour Mon Ami**")
    st.write("---")
    st.caption("Magazine Project Dashboard")

# 4. النص الفلسفي (بشكل أصغر وأشيك)
st.markdown('<div class="quote-text">"Peut-être n\'es-tu pas né sur cette terre, mais tu naitras là où tu apprendras."</div>', unsafe_allow_html=True)

# 5. جلب البيانات
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RMpE1HR_rsgy9luptAHgD0DyTpD1uTYBTbTKNLOWYbI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        return pd.DataFrame()

df = load_data()

# 6. عرض الكروت (Statistiques) زي الصورة اللي أرفقتها
if not df.empty:
    mots_total = len(df)
    verbes = len(df[df['Type'].str.contains('Verbe', na=False, case=False)])
    noms = len(df[df['Type'].str.contains('Nom', na=False, case=False)])
    adjectifs = len(df[df['Type'].str.contains('Adjectif', na=False, case=False)])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card" style="border-bottom-color: #24bf57;"><div class="stat-label">Total</div><div class="stat-value">{mots_total}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Noms</div><div class="stat-value">{noms}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Verbes</div><div class="stat-value">{verbes}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card" style="border-bottom-color: #a855f7;"><div class="stat-label">Adjectifs</div><div class="stat-value">{adjectifs}</div></div>', unsafe_allow_html=True)

    st.write("### Liste des mots")
    search = st.text_input("🔍 Rechercher un mot...")
    
    if search:
        df_display = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    else:
        df_display = df

    # 7. تلوين أنواع الكلمات في الجدول
    def style_types(val):
        if str(val).lower() == 'verbe': color = 'background-color: #dcfce7; color: #166534'
        elif str(val).lower() == 'nom': color = 'background-color: #e0f2fe; color: #075985'
        elif str(val).lower() == 'adjectif': color = 'background-color: #f3e8ff; color: #6b21a8'
        else: color = ''
        return f'{color}; font-weight: bold; border-radius: 10px;'

    st.table(df_display.style.applymap(style_types, subset=['Type']))

else:
    st.warning("⚠️ الجدول فارغ، تأكد من ربط Google Sheets.")
