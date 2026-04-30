import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# --- Configuration ---
st.set_page_config(page_title="User Management System", layout="wide")

# --- Initialize Session State (แทน Database) ---
if "fake_db" not in st.session_state:
    st.session_state.fake_db = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "created_at": "2024-01-01"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "created_at": "2024-01-02"},
    ]

# --- Helper Functions (Logic เดียวกับ API) ---
def add_user(name, email):
    new_id = max([u["id"] for u in st.session_state.fake_db], default=0) + 1
    new_user = {
        "id": new_id,
        "name": name,
        "email": email,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    st.session_state.fake_db.append(new_user)

def delete_user(user_id):
    st.session_state.fake_db = [u for u in st.session_state.fake_db if u["id"] != user_id]

# --- UI Layout ---
st.title("👤 User Management System (Local State)")
st.info("ระบบนี้รันบน Streamlit โดยตรง ข้อมูลจะเก็บอยู่ใน Session ชั่วคราว")

# Sidebar: สำหรับเพิ่มข้อมูล
st.sidebar.header("Add New User")
with st.sidebar.form("add_user_form", clear_on_submit=True):
    name_input = st.text_input("Full Name")
    email_input = st.text_input("Email Address")
    submit_btn = st.form_submit_button("Create User")

    if submit_btn:
        if name_input and email_input:
            add_user(name_input, email_input)
            st.sidebar.success(f"User {name_input} added!")
            st.rerun()
        else:
            st.sidebar.error("Please fill in all fields.")

# Main Screen: แสดงผลและจัดการ
if st.session_state.fake_db:
    df = pd.DataFrame(st.session_state.fake_db)
    
    # แสดงตารางข้อมูล
    st.subheader("Current Users")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ส่วนการลบข้อมูล
    st.divider()
    st.subheader("Administrative Actions")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        target_id = st.selectbox("Select User ID to delete", 
                               options=[u["id"] for u in st.session_state.fake_db],
                               format_func=lambda x: f"ID: {x} - {next(u['name'] for u in st.session_state.fake_db if u['id'] == x)}")
    
    with col2:
        st.write(" ") # สร้างที่ว่างให้ปุ่มตรงกัน
        if st.button("Confirm Delete", type="primary", use_container_width=True):
            delete_user(target_id)
            st.toast(f"Deleted User ID {target_id}")
            st.rerun()
else:
    st.warning("No users found. Please add a new user from the sidebar.")
