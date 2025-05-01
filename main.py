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

def clean_currency(x):
      if isinstance(x,str):
            if(x == "Unavailable"):
                  return 0
            return(x.replace('$','').replace(',',''))
      return(x)

def load_transactions(file):
    df = pd.read_csv(file)
    #EdFinancial has a trailing column, need to check for it and remove
    if "Unnamed" in df.columns[-1]:
        df = df.iloc[: , :-1]

    #st.write(df)
    #Convert all dates to Pandas Datetime
    df["Date"] = pd.to_datetime(df["Date"])

    #Conver all numbers to float value
    df["Principal"] = df["Principal"].apply(clean_currency).astype('float')
    df["Interest"] = df["Interest"].apply(clean_currency).astype('float')
    df["Fees"] = df["Fees"].apply(clean_currency).astype('float')
    df["Total"] = df["Total"].apply(clean_currency).astype('float')
    df["UnpaidPrincipalBalanceValue"] = df["UnpaidPrincipalBalanceValue"].apply(clean_currency).astype('float')
    return df

def plot_loan_graph(loan_df):
      #Remove any "unknown values" from dataframe

      #Sort the dataframe by ascending date
      loan_df = loan_df.sort_values(
                          by="Date",
                          ascending=True
                    )
      fig = px.line(
            loan_df,
            x="Date",
            y="UnpaidPrincipalBalanceValue"
        )
      st.plotly_chart(fig, use_container_width=True)
      
      

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
                    loan_dict = df_loan_dict[loans[0]]
                    #totalPrincipalPaid = loan_dict[loan_dict['Principal'] < 0.0].sum()
                    st.write(loan_dict)
                    #st.write(totalPrincipalPaid)

                    st.subheader('Loan Total Graph')
                    plot_loan_graph(loan_dict)

                    st.subheader('Loan Payment Summary')

            with tab2:
                    st.write(df_loan_dict[loans[1]])
            with tab3:
                    st.write(df_loan_dict[loans[2]])
            with tab4:
                    st.write(df_loan_dict[loans[3]])


main()