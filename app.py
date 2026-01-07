import streamlit as st
import pandas as pd

# 1. الترحيب (Bonjour Mina)
st.set_page_config(page_title="Mina's Belleville Project", page_icon="🏗️")
st.title("Bonjour Mina ☕")
st.info("أهلاً بك في تطبيق مجلة بيلفيل - رؤية هندسية وفلسفية")

# 2. قاعدة البيانات المبدئية
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"الكلمة": "Belleville", "النوع": "اسم", "المعنى": "حي في باريس"},
        {"الكلمة": "Architecture", "النوع": "اسم", "المعنى": "عمارة"},
        {"الكلمة": "Construire", "النوع": "فعل", "المعنى": "يبني"}
    ])

df = st.session_state.data

# 3. محرك البحث
search = st.text_input("🔍 ابحث عن كلمة أو فعل...")

# 4. العدادات (Dashboard)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("إجمالي الكلمات", len(df))
    if st.button("عرض قائمة الكلمات"):
        st.write(df)

with col2:
    nouns = df[df['النوع'] == 'اسم']
    st.metric("عدد الأسماء", len(nouns))
    if st.button("عرض قائمة الأسماء"):
        st.table(nouns)

with col3:
    verbs = df[df['النوع'] == 'فعل']
    st.metric("عدد الأفعال", len(verbs))
    if st.button("عرض قائمة الأفعال"):
        st.table(verbs)

# نتائج البحث
if search:
    res = df[df['الكلمة'].str.contains(search, case=False) | df['المعنى'].str.contains(search)]
    st.success(f"نتائج البحث عن: {search}")
    st.write(res)
    
