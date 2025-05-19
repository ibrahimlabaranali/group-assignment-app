import streamlit as st
import pandas as pd
import os
import random
import glob

st.set_page_config(page_title="Group Assignment by Class Group", layout="centered")

st.title("DDA Presentation Group Assignment")
st.markdown(
    "Select your **Class Group (A–E)** and enter your **Registration Number**. "
    "You will be randomly assigned to one of 5 uniquely named project groups."
)

# Step 1: Select Class Group
class_group = st.selectbox("Select your Class Group", ["A", "B", "C", "D", "E"])

# Unique group names
group_names = ["Atlas", "Eureka", "Nova", "Zenith", "Momentum"]
group_limit = 5

# Directory to store CSVs
data_dir = "class_data"
os.makedirs(data_dir, exist_ok=True)

# File for selected class group
data_file = os.path.join(data_dir, f"group_data_Class_{class_group}.csv")

# Load or initialize class data
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame(columns=["Registration Number", "Group"])

group_counts = df["Group"].value_counts().to_dict()
available_groups = [g for g in group_names if group_counts.get(g, 0) < group_limit]

# Student registration form
with st.form("assign_form"):
    reg_number = st.text_input("Enter your Registration Number")
    submitted = st.form_submit_button("Submit")

    if submitted:
        reg_number = reg_number.strip()
        if not reg_number:
            st.error("Please enter your registration number.")
        elif reg_number in df["Registration Number"].values:
            assigned_group = df[df["Registration Number"] == reg_number]["Group"].values[0]
            st.warning(f"{reg_number}, you have already been assigned to **{assigned_group}**.")
        elif not available_groups:
            st.error("All project groups are full for this class group. Please contact the instructor.")
        else:
            group = random.choice(available_groups)
            df.loc[len(df)] = [reg_number, group]
            df.to_csv(data_file, index=False)
            st.success(f"{reg_number}, you have been assigned to **{group}** for Class Group {class_group}.")

# Display current class assignments
if not df.empty:
    st.markdown(f"### 📋 Current Assignments for Class Group {class_group}")
    st.dataframe(df)

# 🔒 Instructor-only reset tool (password protected)
with st.expander("🔐 Instructor Login"):
    password = st.text_input("Enter instructor password", type="password")
    if password == "admin123":  # ← You can change this password
        st.success("Access granted. You are logged in as instructor.")
        if st.button("⚠ Reset ALL class group assignments (delete all files)"):
            for file in glob.glob(os.path.join(data_dir, "group_data_Class_*.csv")):
                os.remove(file)
            st.success("✅ All class group assignment files have been deleted.")
    elif password:
        st.error("Incorrect password.")
