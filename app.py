import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Belleville 2030", layout="wide")

# 2. تنسيق CSS متطور (للخط الفرنسي، الأزرار الكبيرة، والتأثيرات)
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&family=Great+Vibes&display=swap" rel="stylesheet">
    <style>
    /* تنسيق الشعار (المقولة الفلسفية) بخط فرنسي */
    .motto-container {
        text-align: center;
        padding: 30px;
        background: linear-gradient(to right, #ffffff, #f8fafc, #ffffff);
        border-radius: 20px;
        margin-bottom: 35px;
        border-top: 3px solid #24bf57;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .motto-french {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem !important;
        color: #1e293b;
        font-style: italic;
        margin-bottom: 10px;
    }
    .motto-arabic {
        font-family: 'Arial', sans-serif;
        font-size: 1.4rem;
        color: #64748b;
        direction: rtl;
    }

    /* تكبير وتحسين الأزرار (الزراير) */
    div.stButton > button {
        width: 100%;
        min-height: 160px !important; /* تكبير الزرار */
        background-color: white !important;
        color: #1e293b !important;
        border-radius: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    
    /* تأثير الوقوف على الزرار (Hover) */
    div.stButton > button:hover {
        background: linear-gradient(135deg, #24bf57 0%, #1a9344 100%) !important;
        color: white !important;
        transform: translateY(-8px) !important;
        box-shadow: 0 15px 25px rgba(36, 191, 87, 0.2) !important;
    }
    
    /* تنسيق النص جوه الزرار */
    .btn-label { font-size: 1.2rem; font-weight: 500; opacity: 0.8; }
    .btn-value { font-size: 2.8rem; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("Belleville 2030")
    st.image("https://lh3.googleusercontent.com/u/0/d/1702IVuPmDCISvkfvpdTwYJ5_aDPrvcQU", width=90)
    st.markdown("### **Bonjour Mon Ami**")
    st.write("---")

# 4. الشعار (Motto) - المقولة بخط فرنسي وترجمتك
st.markdown("""
    <div class="motto-container">
        <div class="motto-french">"Peut-être n'es-tu pas né sur cette terre, mais tu naitras là où tu apprendras."</div>
        <div class="motto-arabic">"ربما لم أولد هنا، ولكن حيث أرض المعرفة تكون أرض الميلاد"</div>
    </div>
    """, unsafe_allow_html=True)

# 5. تحميل البيانات من Google Sheets
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

    # 6. الأزرار الكبيرة (الزراير)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"Total\n\n{total_v}"): st.session_state.filter = 'Total'
    with col2:
        if st.button(f"Noms\n\n{noms_v}"): st.session_state.filter = 'Nom'
    with col3:
        if st.button(f"Verbes\n\n{verbes_v}"): st.session_state.filter = 'Verbe'
    with col4:
        if st.button(f"Adjectifs\n\n{adj_v}"): st.session_state.filter = 'Adjectif'

    # 7. الفلترة والجدول
    st.write(f"### Liste: {st.session_state.filter}")
    df_f = df if st.session_state.filter == 'Total' else df[df['Type'].str.contains(st.session_state.filter, na=False, case=False)]
    
    search = st.text_input("🔍 Rechercher...")
    if search:
        df_f = df_f[df_f.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    # تلوين الجدول
    def style_types(val):
        color_map = {'verbe': 'background-color: #dcfce7; color: #166534', 'nom': 'background-color: #e0f2fe; color: #075985', 'adjectif': 'background-color: #f3e8ff; color: #6b21a8'}
        return f"{color_map.get(str(val).lower(), '')}; font-weight: bold; border-radius: 8px;"

    st.table(df_f.style.applymap(style_types, subset=['Type']))
