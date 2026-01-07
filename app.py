import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Belleville 2030", layout="wide")

# 2. كود التنسيق الجمالي (CSS) - تم إصلاحه بالكامل
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
    <style>
    /* تنسيق الشعار الفرنسي */
    .motto-container {
        text-align: center;
        padding: 40px;
        background: #ffffff;
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    .motto-french {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem !important;
        color: #1e293b;
        font-style: italic;
    }

    /* تنسيق الزراير الملونة والكبيرة */
    div.stButton > button {
        width: 100%;
        min-height: 150px !important;
        border-radius: 20px !important;
        border: none !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
    }
    
    /* ألوان مخصصة لكل زرار زي الصورة الأصلية */
    /* زر Total */
    div.stButton > button[kind="secondary"] { background: #24bf57 !important; color: white !important; }
    /* زر Noms */
    div.stButton > button:nth-child(1) { border-bottom: 5px solid #2596be !important; }

    div.stButton > button:hover {
        transform: translateY(-10px) !important;
        filter: brightness(1.1);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.title("Belleville 2030")
    st.image("https://lh3.googleusercontent.com/u/0/d/1702IVuPmDCISvkfvpdtWyJ5_aDPrvcQU", width=100)
    st.markdown("### **Bonjour Mon Ami**")
    st.write("---")

# 4. الشعار الفرنسي الصافي (بدون عربي)
st.markdown("""
    <div class="motto-container">
        <div class="motto-french">"Peut-être n'es-tu pas né sur cette terre, mais tu naitras là où tu apprendras."</div>
    </div>
    """, unsafe_allow_html=True)

# 5. البيانات
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RMpE1HR_rsgy9luptAHgD0DyTpD1uTYBTbTKNLOWYbI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try: return pd.read_csv(SHEET_URL)
    except: return pd.DataFrame()

df = load_data()

if not df.empty:
    if 'filter' not in st.session_state: st.session_state.filter = 'Total'

    # حساب الأرقام
    total_v = len(df)
    noms_v = len(df[df['Type'].str.contains('Nom', na=False, case=False)])
    verbes_v = len(df[df['Type'].str.contains('Verbe', na=False, case=False)])
    adj_v = len(df[df['Type'].str.contains('Adjectif', na=False, case=False)])

    # 6. توزيع الزراير الملونة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"Total\n\n{total_v}", key="total_btn"): st.session_state.filter = 'Total'
    with col2:
        if st.button(f"Noms\n\n{noms_v}", key="noms_btn"): st.session_state.filter = 'Nom'
    with col3:
        if st.button(f"Verbes\n\n{verbes_v}", key="verbes_btn"): st.session_state.filter = 'Verbe'
    with col4:
        if st.button(f"Adjectifs\n\n{adj_v}", key="adj_btn"): st.session_state.filter = 'Adjectif'

    # 7. الفلترة والجدول الملون
    st.subheader(f"Liste: {st.session_state.filter}")
    
    df_f = df if st.session_state.filter == 'Total' else df[df['Type'].str.contains(st.session_state.filter, na=False, case=False)]
    
    search = st.text_input("🔍 Rechercher un mot...")
    if search:
        df_f = df_f[df_f.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    def style_types(val):
        color_map = {
            'verbe': 'background-color: #dcfce7; color: #166534',
            'nom': 'background-color: #e0f2fe; color: #075985',
            'adjectif': 'background-color: #f3e8ff; color: #6b21a8'
        }
        return f"{color_map.get(str(val).lower(), '')}; font-weight: bold; border-radius: 10px;"

    st.table(df_f.style.applymap(style_types, subset=['Type']))
