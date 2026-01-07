import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Belleville 2030", layout="wide")

# 2. تنسيق CSS للتفاعل والألوان
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 120px;
        background-color: white;
        color: #1e293b;
        border-radius: 15px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #24bf57 0%, #1a9344 100%);
        color: white !important;
        transform: translateY(-5px);
    }
    .quote-box {
        text-align: center;
        padding: 15px;
        background: #f8fafc;
        border-radius: 10px;
        margin-bottom: 25px;
        border-left: 5px solid #24bf57;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.title("Belleville 2030")
    st.image("https://lh3.googleusercontent.com/u/0/d/1702IVuPmDCISvkfvpdTwYJ5_aDPrvcQU", width=80)
    st.markdown("### **Bonjour Mon Ami**")
    st.write("---")

# 4. المقولة الفلسفية
st.markdown('<div class="quote-box"><h3 style="font-style: italic; margin:0;">"Peut-être n\'es-tu pas né sur cette terre, mais tu naitras là où tu apprendras."</h3></div>', unsafe_allow_html=True)

# 5. جلب البيانات
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RMpE1HR_rsgy9luptAHgD0DyTpD1uTYBTbTKNLOWYbI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try: return pd.read_csv(SHEET_URL)
    except: return pd.DataFrame()

df = load_data()

if not df.empty:
    # تهيئة حالة الفلتر في الجلسة (Session State)
    if 'filter' not in st.session_state:
        st.session_state.filter = 'Total'

    # حساب الأرقام
    total_val = len(df)
    noms_val = len(df[df['Type'].str.contains('Nom', na=False, case=False)])
    verbes_val = len(df[df['Type'].str.contains('Verbe', na=False, case=False)])
    adj_val = len(df[df['Type'].str.contains('Adjectif', na=False, case=False)])

    # 6. توزيع الكروت كأزرار تفاعلية للفلترة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"Total\n{total_val}"): st.session_state.filter = 'Total'
    with col2:
        if st.button(f"Noms\n{noms_val}"): st.session_state.filter = 'Nom'
    with col3:
        if st.button(f"Verbes\n{verbes_val}"): st.session_state.filter = 'Verbe'
    with col4:
        if st.button(f"Adjectifs\n{adj_val}"): st.session_state.filter = 'Adjectif'

    # 7. تطبيق الفلترة بناءً على الزر المضغوط
    if st.session_state.filter == 'Total':
        df_filtered = df
    else:
        df_filtered = df[df['Type'].str.contains(st.session_state.filter, na=False, case=False)]

    st.write(f"### Liste: {st.session_state.filter}")
    
    # محرك البحث الإضافي
    search = st.text_input("🔍 Rechercher...")
    if search:
        df_filtered = df_filtered[df_filtered.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    # 8. تلوين أنواع الكلمات في الجدول
    def style_types(val):
        color_map = {
            'verbe': 'background-color: #dcfce7; color: #166534',
            'nom': 'background-color: #e0f2fe; color: #075985',
            'adjectif': 'background-color: #f3e8ff; color: #6b21a8'
        }
        style = color_map.get(str(val).lower(), '')
        return f'{style}; font-weight: bold; border-radius: 8px;'

    st.table(df_filtered.style.applymap(style_types, subset=['Type']))
