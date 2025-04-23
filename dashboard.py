import streamlit as st
import pandas as pd
from database import fetch_events, fetch_event_counts_per_day
from datetime import datetime

st.set_page_config(layout="wide")

st.title("📅 My Event Dashboard")

# Display all events
st.subheader("Upcoming Events")
events = fetch_events()
df = pd.DataFrame(events, columns=["ID", "Title", "Date", "Priority", "Category"])

# Add days_left based on current time
df["Days Left"] = df["Date"].apply(lambda d: (datetime.strptime(d, "%Y-%m-%d %H:%M") - datetime.today()).days)

df = df[["ID", "Title", "Date", "Days Left", "Priority", "Category"]]

# Category Filter Dropdown
categories = df['Category'].unique().tolist()
categories.insert(0, 'All')  # Adding 'All' option to view everything
selected_category = st.selectbox("Filter by Category", categories)

# Filter events based on the selected category
filtered_df = df.copy()
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# Display filtered events
st.dataframe(filtered_df.drop("ID", axis=1), use_container_width=True)

# Busy level bar chart
st.subheader("📊 Busy Level by Day")
busy_data = fetch_event_counts_per_day()
if busy_data:
    busy_df = pd.DataFrame(busy_data, columns=["Date", "Event Count"])
    st.bar_chart(busy_df.set_index("Date"))
else:
    st.info("No data available to show busy level.")

# Category distribution bar chart (Unfiltered)
st.subheader("📊 Event Count by Category")
category_counts = df['Category'].value_counts()
if not category_counts.empty:
    category_df = pd.DataFrame(category_counts).reset_index()
    category_df.columns = ['Category', 'Count']
    st.bar_chart(category_df.set_index('Category'))
else:
    st.info("No events available.")