
import streamlit as st
import pandas as pd
import os
import random

st.set_page_config(page_title="Group Assignment by Class", layout="centered")

st.title("Student Group Assignment")
st.markdown("Enter your **Class Code** and your **Registration Number**. You will be randomly assigned to one of 6 groups.")

# Step 1: Input Class Code
class_code = st.text_input("Enter Class Code (e.g., MScDDA2025)", max_chars=20)

if class_code:
    # Create a folder to store class-specific CSVs
    if not os.path.exists("class_data"):
        os.makedirs("class_data")

    # Define class-specific file
    data_file = os.path.join("class_data", f"group_data_{class_code}.csv")

    # Load or create data file
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
    else:
        df = pd.DataFrame(columns=["Registration Number", "Group"])

    group_limits = 6
    groups = ["Atlas", "Eureka", "Nova", "Zenith", "Pulse", "Momentum"]
    group_counts = df["Group"].value_counts().to_dict()
    available_groups = [g for g in groups if group_counts.get(g, 0) < group_limits]

    # Step 4: Student registration number input
    with st.form("assign_form"):
        reg_number = st.text_input("Enter your Registration Number")
        submitted = st.form_submit_button("Submit")

        if submitted:
            reg_number = reg_number.strip()
            if not reg_number:
                st.error("Please enter your registration number.")
            elif reg_number in df["Registration Number"].values:
                assigned_group = df[df["Registration Number"] == reg_number]["Group"].values[0]
                st.warning(f"{reg_number}, you have already been assigned to {assigned_group}.")
            elif not available_groups:
                st.error("All groups are full for this class. Please contact the instructor.")
            else:
                group = random.choice(available_groups)
                df.loc[len(df)] = [reg_number, group]
                df.to_csv(data_file, index=False)
                st.success(f"{reg_number}, you have been assigned to {group} for class {class_code}.")
