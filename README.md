# Ryan's Student Loan Tracker App

This application is meant to help new and exisiting students figure out what they are getting themselves into with Student Loans. Insert your Loan Details and your anticipated monthly payment to get a visual of how long it will take to pay off. 

# How It's Made

Tech Used: Python, Streamlit, Pandas, Numpy

This whole project is based on Tech With Tim's YouTube video "[How To Automate Your Finances with Python - Full Tutorial (Pandas, Sreamlit, Plotly, & More)](https://youtu.be/wqBlmAWqa6A?si=kShSN9sU3wSzgw4N)". The original main.py located in archive/main.py will reflect a very similar file to what is shown in the video. Run it to see my take on his original idea.

I have built this specifically for Edfinancial Loan Statments. Eventually it would be nice to have it be able to take in any statement given a specific format. 

# Lessons Learned
Through the use of st element keys, I was able to consolidate the Tab Display code into a single function call and pass the unique loan dataframe I want to display and a unique key value. Because of this, I am able to load each tab with full functionaliy. 