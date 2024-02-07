import streamlit as st 
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime 

# Display Title and Description
st.title("Finance Transactions Editor")
st.markdown("Enter transaction below")

#Establish Google Sheets connection
conn = st.connection("gsheets", type = GSheetsConnection)

existing_data = conn.read(worksheet="data",usecols=list(range(12)),ttl=5) # read spreasheet into df
existing_data = existing_data.dropna(how="all") # drop any empty rows

# st.dataframe(existing_data)

# List of Transaction Types and Categories

TRANSACTION_TYPES = [
    "debit",
    "credit"
]

CATEGORIES = [
    "Groceries",
    "Gas & Fuel",
    "Amazon",
    "Shaw Mobile",
    "Internet",
    "Utilities",
    "Property Tax",
    "Netflix",
    "Spotify"
]

ACCOUNTS = [
    "PC MASTERCARD",
    "MASTERCARD CAD",
    "(Cory) PERSONAL CHEQUING ACCOUNT CAD"
]

LABELS = [
    "Reimbursement",
    "Vacation",
    "Kira",
    ""
]

#Onboarding New Transaction Form
with st.form(key="trans_form"):
    trans_date = st.date_input(label = "Date*")
    description = st.text_input(label="Description*")
    amount = st.slider("Amount*",0,100,5)
    trans_type = st.selectbox("Transaction Type*", options = TRANSACTION_TYPES, index = None)
    category = st.selectbox("Category",options = CATEGORIES,index = None)
    account_name = st.selectbox("Account Name", options = ACCOUNTS, index = None)
    label = st.multiselect("Labels", options = LABELS)
    notes = st.text_area(label = "Notes")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label = "submit Transaction")

    # If submit button pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not trans_date or not amount or not trans_type:
            st.warning("Ensure all mandatory fields are filled")
            st.stop()
        else:
            # Create a new row of transaction data
            transaction_data = pd.DataFrame(
                [
                    {
                    "date":trans_date.strftime("%m-%d-%Y"),
                    "month":trans_date.month,
                    "day":trans_date.day,
                    "year":trans_date.year,
                    "description":description,
                    "original description":description,
                    "amount":amount,
                    "transaction type":trans_type,
                    "category":category,
                    "account name":account_name,
                    "labels":", ".join(label),
                    "notes":notes
                    }
                ]
            )

            # Add the new transaction data to the existing data
            updated_df = pd.concat([existing_data, transaction_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="data", data = updated_df)

            st.success("Transaction data successfully submitted")