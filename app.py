import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Ola Ride Insights", layout="wide")

# 2. Database Connection Function
def get_data(query):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="server@123",
            database="ola_project"
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        return None

# Pre-load data to seamlessly identify exact table column names
raw_data = get_data("SELECT * FROM cleaned_ola_data LIMIT 10;")

# 3. Sidebar Navigation
st.sidebar.title("🚖 Navigation")
page = st.sidebar.selectbox("Go to Page:", [
    "🏠 Home", 
    "📊 Executive Summary", 
    "💰 Revenue Analysis", 
    "💡 SQL Business Insights",
    "📁 View Raw Data"
])

# ----------------- PAGE 1: HOME -----------------
if page == "🏠 Home":
    st.title("🚖 Ola Ride Insights Project")
    
    # Replaced the typewriter image with a premium visual welcoming container
    st.markdown("""
    <div style="background-color:#1E1E1E; padding:30px; border-radius:15px; border-left: 8px solid #FFD700; margin-bottom: 25px;">
        <h2 style="color:white; margin-top:0;">Welcome to the Ola Mobility Analytics Hub</h2>
        <p style="color:#B0B0B0; font-size:16px;">
            An interactive performance application processing operational data to extract deep vehicle, revenue, and customer lifecycle insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Project Overview:")
    st.write("In this project, we have collected Ola rides data and performed Data Cleaning, SQL Analysis, and Visualization.")
    
    # Adding clean status tracking metrics for visual appeal
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Analysis Scope", value="100,000+ Rides")
    with col2:
        st.metric(label="Database Engine", value="MySQL 8.0")
    with col3:
        st.metric(label="Reporting Tools", value="Power BI & Streamlit")
        
    st.write("")
    st.write("* **Power BI Dashboard:** Formulated for high-level business reporting.")
    st.write("* **SQL Analysis:** Built to instantly address 10 critical business questions.")
    st.write("* **Interactive Charts:** Interactive data breakdowns for deeper observations.")
    st.info("👈 Please select a view from the sidebar navigation menu.")

# ----------------- PAGE 2: EXECUTIVE SUMMARY -----------------
elif page == "📊 Executive Summary":
    st.title("📊 Executive Dashboard")
    st.write("This dashboard analyzes absolute ride volumes and overall booking status performance metrics.")
    st.image("Dashboard 1.png", use_container_width=True)

# ----------------- PAGE 3: REVENUE ANALYSIS -----------------
elif page == "💰 Revenue Analysis":
    st.title("💰 Revenue & Vehicle Analysis")
    st.write("Detailed revenue breakdowns structured across distinct vehicle segments.")
    st.image("Dashboard 2.png", use_container_width=True)

# ----------------- PAGE 4: SQL BUSINESS INSIGHTS -----------------
elif page == "💡 SQL Business Insights":
    st.title("💡 Key Business Questions (SQL Results)")
    
    if raw_data is None:
        st.error("Database connection failed. Please verify your connection credentials and database schema.")
    else:
        # Robust Dynamic Column Mapping System
        cols = {c.lower().replace(" ", "_"): c for c in raw_data.columns}
        
        status_col = cols.get('booking_status', raw_data.columns[0])
        v_type_col = cols.get('vehicle_type', raw_data.columns[0])
        cust_id_col = cols.get('customer_id', raw_data.columns[0])
        pay_col = cols.get('payment_method', raw_data.columns[0])
        booking_id_col = cols.get('booking_id', raw_data.columns[0])
        dist_col = next((c for c in raw_data.columns if 'dist' in c.lower()), raw_data.columns[0])
        reason_col = next((c for c in raw_data.columns if 'reason' in c.lower() or 'cancel' in c.lower()), raw_data.columns[0])
        d_rating_col = next((c for c in raw_data.columns if 'driver_rat' in c.lower()), raw_data.columns[0])
        c_rating_col = next((c for c in raw_data.columns if 'cust' in c.lower() and 'rat' in c.lower()), raw_data.columns[0])
        val_col = next((c for c in raw_data.columns if 'value' in c.lower() or 'revenue' in c.lower()), raw_data.columns[0])

        question = st.selectbox("Choose a Question:", [
            "1. Successful Bookings",
            "2. Average Ride Distance per Vehicle",
            "3. Total Cancelled Rides (Customer)",
            "4. Top 5 High-Booking Customers",
            "5. Driver Cancellations (Car/Personal Issues)",
            "6. Max/Min Driver Ratings (Prime Sedan)",
            "7. Rides using UPI Payment",
            "8. Avg Customer Rating per Vehicle",
            "9. Total Revenue (Successful Rides)",
            "10. Incomplete Rides & Reasons"
        ])
        
        # Mapping Questions directly to SQL queries utilizing dynamically identified schema columns
        if "1." in question: query = f"SELECT * FROM cleaned_ola_data WHERE {status_col} LIKE '%Success%';"
        elif "2." in question: query = f"SELECT {v_type_col}, AVG({dist_col}) as Avg_Dist FROM cleaned_ola_data GROUP BY {v_type_col};"
        elif "3." in question: query = f"SELECT COUNT(*) as Total FROM cleaned_ola_data WHERE {status_col} LIKE '%Cancel%Customer%';"
        elif "4." in question: query = f"SELECT {cust_id_col}, COUNT(*) as Rides FROM cleaned_ola_data GROUP BY {cust_id_col} ORDER BY Rides DESC LIMIT 5;"
        elif "5." in question: query = f"SELECT COUNT(*) as Total FROM cleaned_ola_data WHERE {status_col} LIKE '%Cancel%Driver%' AND ({reason_col} LIKE '%Personal%' OR {reason_col} LIKE '%Car%' OR {reason_col} LIKE '%Break%');"
        elif "6." in question: query = f"SELECT MAX({d_rating_col}) as Max_Rating, MIN({d_rating_col}) as Min_Rating FROM cleaned_ola_data WHERE {v_type_col} LIKE '%Prime Sedan%';"
        elif "7." in question: query = f"SELECT * FROM cleaned_ola_data WHERE {pay_col} LIKE '%UPI%';"
        elif "8." in question: query = f"SELECT {v_type_col}, AVG({c_rating_col}) as Avg_Rating FROM cleaned_ola_data GROUP BY {v_type_col};"
        elif "9." in question: query = f"SELECT SUM({val_col}) as Total_Revenue FROM cleaned_ola_data WHERE {status_col} LIKE '%Success%';"
        elif "10." in question: query = f"SELECT {booking_id_col}, {status_col}, {reason_col} FROM cleaned_ola_data WHERE {status_col} NOT LIKE '%Success%';"

        data = get_data(query)
        if data is not None:
            st.dataframe(data)
            # Conditional graph rendering based on chosen insight parameters
            if "2." in question or "8." in question:
                st.plotly_chart(px.bar(data, x=data.columns[0], y=data.columns[1], title=question))
            elif "4." in question:
                st.plotly_chart(px.pie(data, values='Rides', names=cust_id_col, title="Top 5 Customers"))

# ----------------- PAGE 5: VIEW RAW DATA -----------------
elif page == "📁 View Raw Data":
    st.title("📁 Cleaned Dataset Explorer")
    st.write("Displaying the initial 100 observations fetched directly from your table layout:")
    full_data = get_data("SELECT * FROM cleaned_ola_data LIMIT 100;")
    if full_data is not None:
        st.dataframe(full_data)
        st.download_button("Download as CSV", full_data.to_csv(index=False), "ola_data.csv")