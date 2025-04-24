import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import time


#to run this script use the following:
#python -m streamlit run main.py

st.set_page_config(page_title="Student Loan Tracker", page_icon= "💵", layout="wide")

#TODO: Upload and store Loan Details {Original Balance, Current Balance, Interest Rate (Decimal)}
#TODO: Calculate monthly interest growth for a student loan using the Simple Interest Formula
#TODO: Plot out what payment life would look like only making the monthly payment.

def load_transactions(file):
    df = pd.read_csv(file)
    #EdFinancial has a trailing column, need to check for it and remove
    if "Unnamed" in df.columns[-1]:
        df = df.iloc[: , :-1]

    #st.write(df)
    return df

def main():
    st.title("Student Loan Tracker")

    uploaded_file = st.file_uploader("Upload your Account History CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            #Get Unique loan names
            loans = list(set(df['LoanName']))

            #Create a dataframe for each loan
            df_loan_dict = {name: df.loc[df['LoanName'] == name] for name in loans}

            #TODO: Create tabs dynamically, for now assume 4
            tab1, tab2, tab3, tab4 = st.tabs(loans)
            with tab1:
                    st.write(df_loan_dict[loans[0]])
            with tab2:
                    st.write(df_loan_dict[loans[1]])
            with tab3:
                    st.write(df_loan_dict[loans[2]])
            with tab4:
                    st.write(df_loan_dict[loans[3]])


main()