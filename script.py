import streamlit as st
import pandas as pd
import datetime
from sqlalchemy import text

# Retrieve database credentials from secrets
db_secrets = st.secrets["connections"]["shifts"]

# Establish connection
conn = st.connection(name="shifts", type="sql", url=f"{db_secrets['dialect']}://{db_secrets['username']}:{db_secrets['password']}@{db_secrets['host']}:{db_secrets['port']}/{db_secrets['database']}")

# Function to initialize the database
def init_db():
    with conn.session as session:
        session.execute(text('''
            CREATE TABLE IF NOT EXISTS shifts (
                id SERIAL PRIMARY KEY,
                date TEXT, 
                start_time TEXT, 
                end_time TEXT, 
                break INTEGER, 
                daily_rate REAL, 
                total_hours REAL, 
                amount_earned REAL,
                problems TEXT
            )''')
        )
        session.commit()

# Function to load shift data
def load_data():
    return conn.query("SELECT date, start_time, end_time, break, daily_rate, total_hours, amount_earned, problems FROM shifts;", ttl="10m")

# Function to add a new shift
def add_shift(date, start_time, end_time, break_time, daily_rate, total_hours, amount_earned, problems):
    with conn.session as session:
        session.execute(text("""
            INSERT INTO shifts (date, start_time, end_time, break, daily_rate, total_hours, amount_earned, problems)
            VALUES (:date, :start_time, :end_time, :break_time, :daily_rate, :total_hours, :amount_earned, :problems)
        """), {
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "break_time": break_time,
            "daily_rate": daily_rate,
            "total_hours": total_hours,
            "amount_earned": amount_earned,
            "problems": problems
        })
        session.commit()

# Initialize database
init_db()
data = load_data()

# Streamlit UI
st.title("Shift Work Tracker")

# Input fields for adding a new shift
with st.form("shift_form"):
    date = st.date_input("Date", datetime.date.today())
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")
    break_time = st.number_input("Break (minutes)", min_value=0, format="%d")
    daily_rate = st.number_input("Daily Rate ($)", min_value=0.0, format="%.2f")
    problems = st.text_area("Problems (if any)")
    
    submitted = st.form_submit_button("Add Shift")
    
    if submitted:
        # Calculate total hours worked
        total_hours = max((datetime.datetime.combine(date, end_time) - datetime.datetime.combine(date, start_time)).seconds / 3600 - (break_time / 60), 0)
        amount_earned = daily_rate
        
        add_shift(date.strftime("%Y-%m-%d"), str(start_time), str(end_time), break_time, daily_rate, total_hours, amount_earned, problems)
        st.success("Shift added successfully!")
        data = load_data()

# Display stored shifts
st.write("### Logged Shifts")
st.dataframe(data)

# Summary statistics
if not data.empty:
    total_hours = data["total_hours"].sum()
    total_earned = data["amount_earned"].sum()
    st.metric("Total Hours Worked", f"{total_hours:.2f} hours")
    st.metric("Total Amount Receivable", f"${total_earned:.2f}")
else:
    st.write("No shifts logged yet.")
