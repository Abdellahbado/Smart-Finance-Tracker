from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

EXPENSE_INCOME_CSV = "data/income_expenses.csv"


def update_recurring_transactions(df):
    today = datetime.now().date()
    updated_df = df.copy()
    new_transactions = []

    for index, row in df.iterrows():
        if row["Frequency"] != "One-time":
            last_date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
            if row["Frequency"] == "Daily":
                days_to_add = (today - last_date).days
            elif row["Frequency"] == "Weekly":
                days_to_add = ((today - last_date).days // 7) * 7
            elif row["Frequency"] == "Monthly":
                months_to_add = (
                    (today.year - last_date.year) * 12 + today.month - last_date.month
                )
                days_to_add = months_to_add * 30  # Approximation
            elif row["Frequency"] == "Yearly":
                years_to_add = today.year - last_date.year
                days_to_add = years_to_add * 365  # Approximation

            if days_to_add > 0:
                for i in range(1, days_to_add + 1):
                    new_date = last_date + timedelta(days=i)
                    new_transaction = row.copy()
                    new_transaction["Date"] = new_date.strftime("%Y-%m-%d")
                    new_transactions.append(new_transaction)

                # Update the last occurrence date
                updated_df.at[index, "Date"] = today.strftime("%Y-%m-%d")

    if new_transactions:
        updated_df = pd.concat(
            [updated_df, pd.DataFrame(new_transactions)], ignore_index=True
        )

    return updated_df


st.title("Income and Expenses")

# Load existing data
try:
    df = pd.read_csv(EXPENSE_INCOME_CSV)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime(
        "%Y-%m-%d"
    )  # Ensure consistent date format
    df = update_recurring_transactions(df)
    df.to_csv(EXPENSE_INCOME_CSV, index=False)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Type", "Amount", "Frequency", "Description"])

# Input form
with st.form("income_expenses_form"):
    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date", value=datetime.today())
        type_ = st.selectbox("Type", ["Income", "Expense"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")

    with col2:
        frequency = st.selectbox(
            "Frequency", ["One-time", "Daily", "Weekly", "Monthly", "Yearly"]
        )
        description = st.text_input("Description")

    submitted = st.form_submit_button("Add Entry")

if submitted:
    new_row = {
        "Date": date.strftime("%Y-%m-%d"),
        "Type": type_,
        "Amount": amount,
        "Frequency": frequency,
        "Description": description,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(EXPENSE_INCOME_CSV, index=False)
    st.success("Entry added successfully!")

# Display summary
st.subheader("Summary")
total_income = df[df["Type"] == "Income"]["Amount"].sum()
total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:.2f}")
col2.metric("Total Expenses", f"${total_expense:.2f}")
col3.metric("Balance", f"${balance:.2f}")

# Display data
# Display data with delete option
st.subheader("All Entries")
for index, row in df.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
    col1.write(row["Date"])
    col2.write(row["Type"])
    col3.write(f"${row['Amount']:.2f}")
    col4.write(row["Frequency"])
    col5.write(row["Description"])
    if col6.button("Delete", key=f"del_{index}"):
        df = df.drop(index)
        df.to_csv(EXPENSE_INCOME_CSV, index=False)
        st.success("Entry deleted successfully!")
        st.rerun()

# Remove the previous st.dataframe(df) line if you're using this display method

# Filter and display
st.subheader("Filtered View")
filter_type = st.selectbox("Filter by Type", ["All", "Income", "Expense"])
filter_frequency = st.selectbox(
    "Filter by Frequency", ["All", "One-time", "Daily", "Weekly", "Monthly", "Yearly"]
)

filtered_df = df
