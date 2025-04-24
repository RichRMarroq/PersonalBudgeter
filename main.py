import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import time

#to run this script use the following:
#python -m streamlit run main.py

st.set_page_config(page_title="Simple Finance App", page_icon= "💵", layout="wide")

category_file = "categories.json"

if "categories" not in st.session_state:
    #If state is not used, everytime the script is reran, the values are reset.
    st.session_state.categories = {
        "Uncategorized": []
    }

#Pull existing categories and their definitions from saved file.
if os.path.exists(category_file):
    with open(category_file, "r") as f:
        st.session_state.categories = json.load(f)

def save_categories():
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f)

def categorize_transactions(df):
    df["Category"] = "Uncategorized"

    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue

        lowered_keywords = [keyword.lower().strip() for keyword in keywords]

        for idx, row in df.iterrows():
            details = row["Description"].lower().strip()
            if details in lowered_keywords:
                df.at[idx, "Category"] = category
    return df

def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.colums = [col.strip() for col in df.columns]
        #Not needed as my csv already provides float value Amounts.
        #df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

        #st.write(df)
        return categorize_transactions(df)
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def add_keyword_to_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    
    return False

def main():
    st.title("Macaroni Finance Dashboard")

    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            spending_df = df[df["Amount"] < 0.0]
            income_df = df[df["Amount"] > 0.0] 

            st.session_state.spending_df = spending_df.copy()

            tab1, tab2 = st.tabs(["Spending", "Income"])
            with tab1:
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")

                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.success(f"Added a new category: {new_category}")
                        time.sleep(4)
                        st.rerun()
                    else:
                        time.sleep(1)
                        st.warning(f"Category {new_category} already exists")
                        st.rerun()

                st.subheader("Your Spending")
                edited_df = st.data_editor(
                    st.session_state.spending_df[["Date", "Description", "Amount", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f USD"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )

                save_button = st.button("Apply Changes", type="primary")
                if save_button:
                    for idx, row in edited_df.iterrows():
                        new_category = row["Category"]
                        if row["Category"] == st.session_state.spending_df.at[idx, "Category"]:
                            continue

                        details = row["Description"]
                        st.session_state.spending_df.at[idx, "Category"] = new_category
                        add_keyword_to_category(new_category, details)
                st.subheader('Expense Summary')
                category_totals = st.session_state.spending_df.groupby("Category")["Amount"].sum().reset_index()

                category_totals = category_totals.sort_values("Amount", ascending=False)

                st.dataframe(
                    category_totals,
                    column_config={
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f USD")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            

                fig = px.pie(
                    category_totals,
                    values="Amount",
                    names="Category",
                    title="Expenses by Category"
                )

                st.plotly_chart(fig, use_container_width=True)
            with tab2:
                st.write(income_df)


main()