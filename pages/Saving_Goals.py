import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Constants for CSV file paths
EXPENSE_INCOME_CSV = "data/income_expenses.csv"
SAVING_GOALS_CSV = "data/saving_goals.csv"

st.title("Saving Goals")

# Load existing saving goals data
try:
    savings_df = pd.read_csv(SAVING_GOALS_CSV)
except FileNotFoundError:
    savings_df = pd.DataFrame(
        columns=[
            "Goal",
            "Target Amount",
            "Current Amount",
            "Deadline",
            "Monthly Contribution",
        ]
    )

# Load income and expenses data
try:
    income_expenses_df = pd.read_csv(EXPENSE_INCOME_CSV)
    total_income = income_expenses_df[income_expenses_df["Type"] == "Income"][
        "Amount"
    ].sum()
    total_expenses = income_expenses_df[income_expenses_df["Type"] == "Expense"][
        "Amount"
    ].sum()
    current_balance = total_income - total_expenses
except FileNotFoundError:
    current_balance = 0

st.subheader("Current Balance")
st.metric("Balance", f"${current_balance:.2f}")

# Input form for new saving goal
with st.form("saving_goals_form"):
    goal = st.text_input("Goal")
    if not goal:
        goal = "Unknown"
    target_amount = st.number_input("Target Amount", min_value=0.0, format="%.2f")
    current_amount = st.number_input("Current Amount", min_value=0.0, format="%.2f")
    deadline = st.date_input("Deadline")
    frequency = st.selectbox("Frequency", ["One-time", "Monthly", "Yearly"])

    # Calculate monthly contribution
    days_until_deadline = (deadline - datetime.now().date()).days
    months_until_deadline = max(days_until_deadline / 30, 1)  # Ensure at least 1 month
    amount_needed = target_amount - current_amount
    monthly_contribution = (
        amount_needed / months_until_deadline if months_until_deadline > 0 else 0
    )

    st.write(f"Suggested monthly contribution: ${monthly_contribution:.2f}")

    submitted = st.form_submit_button("Add Saving Goal")

if submitted:
    new_row = {
        "Goal": goal,
        "Target Amount": target_amount,
        "Current Amount": current_amount,
        "Deadline": deadline,
        "Frequency": frequency,
        "Monthly Contribution": monthly_contribution,
    }
    savings_df = pd.concat([savings_df, pd.DataFrame([new_row])], ignore_index=True)
    savings_df.to_csv(SAVING_GOALS_CSV, index=False)
    st.success("Saving goal added successfully!")

# Display and update saving goals
st.subheader("Your Saving Goals")
for index, row in savings_df.iterrows():
    with st.expander(f"Goal: {row['Goal']}"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"Target: ${row['Target Amount']:.2f}")
            st.write(f"Current: ${row['Current Amount']:.2f}")

        with col2:
            st.write(f"Deadline: {row['Deadline']}")
            st.write(f"Frequency: {row['Frequency']}")
            st.write(f"Monthly Contribution: ${row['Monthly Contribution']:.2f}")

        with col3:
            progress = min(row["Current Amount"] / row["Target Amount"], 1)
            st.progress(progress)
            st.write(f"Progress: {progress:.2%}")

        # Update current amount
        new_amount = st.number_input(
            "Update current amount",
            min_value=0.0,
            value=float(row["Current Amount"]),
            key=f"update_{index}",
        )

        if st.button("Update", key=f"update_button_{index}"):
            savings_df.at[index, "Current Amount"] = new_amount
            savings_df.to_csv(SAVING_GOALS_CSV, index=False)
            st.success("Amount updated successfully!")
            st.experimental_rerun()

        # Check if goal is reached
        if row["Current Amount"] >= row["Target Amount"]:
            st.success(
                f"Congratulations! You've reached your saving goal for {row['Goal']}!"
            )

        # Check if current balance meets the goal
        if current_balance >= row["Target Amount"]:
            st.info(
                f"Your current balance meets the target for {row['Goal']}. Consider allocating funds to this goal!"
            )

# Overall savings progress
total_target = savings_df["Target Amount"].sum()
total_current = savings_df["Current Amount"].sum()
overall_progress = min(total_current / total_target, 1.0) if total_target > 0 else 0
print(f"Overall savings progress: {overall_progress}")
st.subheader("Overall Savings Progress")
st.progress(overall_progress)
st.write(f"Total Progress: {overall_progress:.2%}")

# Download CSV
st.download_button(
    label="Download saving goals as CSV",
    data=savings_df.to_csv(index=False).encode("utf-8"),
    file_name="saving_goals.csv",
    mime="text/csv",
)
