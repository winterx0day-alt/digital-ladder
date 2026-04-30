import streamlit as st
import pandas as pd

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Thai Digital Savings Comparison", layout="wide", page_icon="💰")

# --- 2. DATABASE: LATEST INTEREST RATES (2026 DATA) ---
# Note: In a production app, you would fetch this from an API or Web Scraper 
savings_data = [
    {"Bank": "Dime! (KKP)", "Account": "Save", "Rate": "3.00%", "Limit": "Up to 30,000 THB", "Min_Rate": 3.0},
    {"Bank": "LHB You (LH Bank)", "Account": "Digital Savings", "Rate": "6.00%", "Limit": "Up to 10,000 THB", "Min_Rate": 6.0},
    {"Bank": "CIMB Thai", "Account": "Chill D", "Rate": "2.88%", "Limit": "Up to 100,000 THB", "Min_Rate": 2.88},
    {"Bank": "Kept (by Krungsri)", "Account": "Grow", "Rate": "2.22%", "Limit": "Up to 5,000,000 THB", "Min_Rate": 2.22},
    {"Bank": "Alpha X (SCBX)", "Account": "Privilege", "Rate": "2.50%", "Limit": "Up to 500,000 THB", "Min_Rate": 2.50},
    {"Bank": "UOB", "Account": "TMRW", "Rate": "2.00%", "Limit": "Variable", "Min_Rate": 2.0},
]

df = pd.DataFrame(savings_data)

# --- 3. UI: SIDEBAR CALCULATOR ---
st.sidebar.header("📊 Your Savings Goal")
user_savings = st.sidebar.number_input("Enter your savings amount (THB)", min_value=0, value=50000, step=1000)
st.sidebar.caption("The tool will calculate annual interest based on your input.")

# --- 4. MAIN DASHBOARD ---
st.title("💰 Thai High-Interest Digital Savings Comparison")
st.write("Compare the best digital accounts in Thailand and see which one fits your balance best.")

# --- 5. VISUALIZATION: COMPARISON TABLE ---
st.subheader("🏦 Top High-Interest Accounts")

# Sort data by interest rate
df_sorted = df.sort_values(by="Min_Rate", ascending=False)

# Add a column for projected annual return
df_sorted["Est. Annual Interest (THB)"] = (user_savings * df_sorted["Min_Rate"]) / 100

# Display the dataframe with high-interest highlighting
st.dataframe(
    df_sorted.drop(columns=["Min_Rate"]), 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "Rate": st.column_config.TextColumn("Interest Rate", help="Maximum available rate"),
        "Est. Annual Interest (THB)": st.column_config.NumberColumn(format="฿ %.2f")
    }
)

# --- 6. RECOMMENDATION LOGIC ---
st.divider()
st.subheader("💡 Analysis & Recommendation")

best_bank = df_sorted.iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.metric("Highest Rate Available", f"{best_bank['Rate']}", f"at {best_bank['Bank']}")
    st.write(f"Based on your savings of **฿{user_savings:,.2f}**, the highest theoretical return is with **{best_bank['Bank']}**.")

with col2:
    st.info("""
    **Things to consider:**
    * **Tiered Rates:** Many banks like LH Bank offer 6%, but only for the first 10,000 THB.
    * **Withdrawal Limits:** Check if the account allows unlimited free transfers.
    * **Minimum Balance:** Some accounts require a minimum balance to maintain the rate.
    """)

# --- 7. FOOTER ---
st.caption("Disclaimer: Rates are updated for 2026. Always check the official bank app for real-time terms and conditions.")
