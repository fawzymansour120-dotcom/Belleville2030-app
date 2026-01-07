import streamlit as st
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="Belleville 2030", page_icon="🏗️", layout="wide")

# 2. التنسيق الجمالي (CSS)
BG_COLOR = "#121212"
VIBRANT_BLUE = "#007bff" # أزرق زاهي للدخول
BLUE_DARK = "#1a2a3a"    # أزرق غامق للزراير
GREEN_ACTIVE = "#28a745" # أخضر زاهي للنشط
GOLD_COLOR = "#d4af37"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_COLOR}; }}
    
    /* تصميم زر الدخول الزاهي */
    div.stButton > button[kind="primary"] {{
        background: {VIBRANT_BLUE};
        color: white !important;
        border: none;
        font-weight: bold;
        font-size: 20px;
        border-radius: 30px;
        padding: 10px 20px;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
        transition: 0.3s;
        width: 100%;
    }}
    div.stButton > button[kind="primary"]:hover {{
        background: #0056b3;
        box-shadow: 0 6px 20px rgba(0, 123, 255, 0.6);
        transform: scale(1.02);
    }}

    /* تصميم الزراير الأربعة */
    div.stButton > button {{
        width: 100
