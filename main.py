import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. SETUP & SESSION STATE (แทน In-memory DB) ---
st.set_page_config(page_title="User Management", layout="wide")

if "fake_db" not in st.session_state:
    st.session_state.fake_db = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com", "created_at": "2024-01-01"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com", "created_at": "2024-01-02"},
    }
if "next_id" not in st.session_state:
    st.session_state.next_id = 3

# --- 2. LOGIC FUNCTIONS (แปลงจาก API Routes) ---
def create_user(name, email):
    new_id = st.session_state.next_id
    user = {
        "id": new_id,
        "name": name,
        "email": email,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    st.session_state.fake_db[new_id] = user
    st.session_state.next_id += 1
    st.success(f"Created user: {name}")

def delete_user(user_id):
    if user_id in st.session_state.fake_db:
        del st.session_state.fake_db[user_id]
        st.toast(f"Deleted User ID {user_id}")
    else:
        st.error("User not found")

# --- 3. STREAMLIT UI ---
st.title("👤 User Management System")

# ส่วนที่ 1: เพิ่ม User (แทน POST /users)
with st.expander("➕ Add New User", expanded=True):
    with st.form("create_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        new_name = col1.text_input("Name")
        new_email = col2.text_input("Email")
        submit = st.form_submit_button("Create")
        
        if submit:
            if new_name and new_email:
                create_user(new_name, new_email)
                st.rerun()
            else:
                st.warning("Please fill all fields")

# ส่วนที่ 2: แสดงข้อมูลและลบ (แทน GET /users และ DELETE /users)
st.subheader("📋 User List")
if st.session_state.fake_db:
    # แปลง dict เป็น DataFrame เพื่อแสดงตาราง
    df = pd.DataFrame(list(st.session_state.fake_db.values()))
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ส่วนลบข้อมูล
    st.divider()
    delete_id = st.number_input("Enter ID to delete", min_value=1, step=1)
    if st.button("Delete User", type="primary"):
        delete_user(delete_id)
        st.rerun()
else:
    st.info("No users found.")
