import streamlit as st
import pandas as pd

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Belleville 2030", page_icon="🏗️", layout="wide")

# 2. منطق التبديل بين الـ Dark و Light Mode
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# الألوان اللي انت اخترتها يا هندسة
MY_BLUE = "#2596be" # لون الزراير العادي
MY_GREEN = "#24bf57" # لون الزر النشط بعد الضغط

# 3. واجهة التنسيق (CSS)
if st.session_state.theme == 'light':
    bg_color = "#FFFFFF"
    text_color = "#121212"
    border_color = "#dee2e6"
else:
    bg_color = "#121212"
    text_color = "#FFFFFF"
    border_color = "#333333"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    h1, h2, p, span {{ color: {text_color} !important; }}
    
    /* تنسيق أزرار الفلتر الأربعة (استخدام اللون الأزرق اللي اخترته) */
    .stButton > button {{
        height: 110px !important;
        background-color: {MY_BLUE} !important;
        color: white
