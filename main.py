import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


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

def calculateMonthlyInterest(balance, ir):
      daily_interest = (balance * ir) / 365.25
      return round(daily_interest * 30, 2)

def calculatePayoff(balance, ir, monthly_payment, total_interest):
      count = 1
      while balance > 0.0:
            monthly_interest = calculateMonthlyInterest(balance, ir)
            total_interest = total_interest - monthly_interest
            balance = balance + monthly_interest - monthly_payment
            date_month = (datetime.now() + relativedelta(months=count)).strftime('%m-%Y')
            count +=1
            st.session_state.payoff_loan_df = pd.concat(
                  [pd.DataFrame([[balance, monthly_payment, monthly_interest, date_month, total_interest]], columns=st.session_state.payoff_loan_df.columns), st.session_state.payoff_loan_df], ignore_index=True)


      return
      

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
                    st.session_state.loan_df = df_loan_dict[loans[0]]
                    #totalPrincipalPaid = loan_dict[loan_dict['Principal'] < 0.0].sum()
                    edited_df = st.dataframe(
                    st.session_state.loan_df[["Date", "LoanName", "Total", "UnpaidPrincipalBalanceValue"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="MM/DD/YYYY"),
                        "Payment Amount": st.column_config.NumberColumn("Total", format="%.2f USD"),
                        "Outstanding Balance": st.column_config.NumberColumn("UnpaidPrincipalBalanceValue", format="%.2f USD")
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )
                    #st.write(loan_dict)
                    #st.write(totalPrincipalPaid)

                    st.subheader('Loan Payment Summary')
                    interest_spend = st.session_state.loan_df["Interest"].sum()
                    st.write(f"You have spent ${interest_spend} USD on Interest")

                    st.subheader('Loan Total Graph')
                    plot_loan_graph(st.session_state.loan_df)

                    st.subheader('Calculate Payoff')
                    interest_rate = st.number_input("Enter your Interest Rate in decimal format (2.5% = .025)", format="%0.3f")
                    monthly_payment = st.number_input("Enter your desired Monthly Payment. If less than minimum, will error.", format="%0.2f")
                    calculate_button = st.button("Calculate Payoff Schedule")

                    if interest_rate and monthly_payment and calculate_button:
                        starting_balance = st.session_state.loan_df["UnpaidPrincipalBalanceValue"].values[0];
                        current_interest = calculateMonthlyInterest(starting_balance, interest_rate)

                        #Check if Current Monthly covers monthly interest
                        if float(monthly_payment) > current_interest:
                              st.success(f"Calculating payoff schedule")
                              #time.sleep(4)
                              d = {'Balance': [starting_balance], 'Monthly Payment': [monthly_payment], 'Monthly Interest': [current_interest], 'Month': [time.strftime("%m-%Y")], 'Total Interest Paid': [interest_spend]}
                              st.session_state.payoff_loan_df = pd.DataFrame(data=d)
                              calculatePayoff(starting_balance, interest_rate, monthly_payment, interest_spend)
                              st.write(st.session_state.payoff_loan_df)
                        else:
                              time.sleep(1)
                              st.warning(f"Monthly Payment {monthly_payment} is not enough to cover monthly accruing interest {current_interest}. Please enter a higher monthly payment")
                              time.sleep(5)
                              st.rerun()
                              

                    

            with tab2:
                    st.write(df_loan_dict[loans[1]])
            with tab3:
                    st.write(df_loan_dict[loans[2]])
            with tab4:
                    st.write(df_loan_dict[loans[3]])


main()