import pandas as pd
import streamlit as st
from datavisulation import DataVisualization

db_config = {
    "user": "root",
    "password": 12345,
    "host": "localhost",
    "database": "phonepay"
}

visualizer = DataVisualization(db_config)

def transaction_value_by_state():
    st.header("PhonePe Transaction Value by State")
    years = visualizer.fetch_data("SELECT DISTINCT year FROM aggregated_transaction_data ORDER BY year")['year'].astype(str).tolist()
    quarters = visualizer.fetch_data("SELECT DISTINCT quarter FROM aggregated_transaction_data ORDER BY quarter")['quarter'].astype(str).tolist()
    categories = visualizer.fetch_data("SELECT DISTINCT Transaction_type FROM aggregated_transaction_data ORDER BY Transaction_type")['Transaction_type'].astype(str).tolist()

    selected_year = st.selectbox("Select Year", ["All"] + years)
    selected_quarter = st.selectbox("Select Quarter", ["All"] + quarters)
    selected_category = st.selectbox("Select Payment Category", ["All"] + categories)

    where_clauses = []
    if selected_year != "All":
        where_clauses.append(f"year = {selected_year}")
    if selected_quarter != "All":
        where_clauses.append(f"quarter = {selected_quarter}")
    if selected_category != "All":
        where_clauses.append(f"Transaction_type = '{selected_category}'")

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    query = f"""
    SELECT state, SUM(Transaction_amount) as Total_Amount
    FROM aggregated_transaction_data
    {where_sql}
    GROUP BY state ORDER BY state
    """
    filtered_data = visualizer.fetch_data(query)
    if filtered_data.empty:
        st.warning("No data available for the selected filters. Please try a different combination.")
    else:
        title = 'Total Transaction Amount by State'
        if where_clauses:
            title = f"Transaction Amount for "
            if selected_year != "All":
                title += f"{selected_year} "
            if selected_quarter != "All":
                title += f"Q{selected_quarter} "
            if selected_category != "All":
                title += f"({selected_category})"
        fig = visualizer.visualize_data_amount_by_state(filtered_data, title=title.strip())
        st.plotly_chart(fig, use_container_width=True)

# Call Scenario 1 function
transaction_value_by_state()


import streamlit as st

def device_dominance_user_engagement():
    st.header("📱 Device Dominance & User Engagement")
    st.info("Analyze how different device brands perform across regions and identify underutilized segments.")

    # 1. Fetch filter options from the database
    brands = visualizer.fetch_data("SELECT DISTINCT brand FROM aggregated_user_data ORDER BY brand")['brand'].tolist()
    states = visualizer.fetch_data("SELECT DISTINCT State FROM aggregated_user_data ORDER BY State")['State'].tolist()
    years = visualizer.fetch_data("SELECT DISTINCT Year FROM aggregated_user_data ORDER BY Year")['Year'].astype(str).tolist()

    # 2. Sidebar/Top filters for Scenario 2
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_brand = st.selectbox("Device Brand", ["All"] + brands)
    with col2:
        selected_state = st.selectbox("State", ["All"] + states)
    with col3:
        selected_year = st.selectbox("Year", ["All"] + years)

    # 3. Build the SQL Query dynamically
    where_clauses = []
    if selected_brand != "All": where_clauses.append(f"brand = '{selected_brand}'")
    if selected_state != "All": where_clauses.append(f"State = '{selected_state}'")
    if selected_year != "All": where_clauses.append(f"Year = {selected_year}")
    
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = f"""
        SELECT brand, SUM(registeredUsers) as Registered_Users, SUM(appOpens) as App_Opens
        FROM aggregated_user_data
        {where_sql}
        GROUP BY brand
    """
    
    data = visualizer.fetch_data(query)

    if not data.empty:
        # 4. Show the main visualization (Bar Chart)
        fig = visualizer.visualize_device_engagement(data, title="Registered Users vs App Opens")
        st.plotly_chart(fig, use_container_width=True)

        # 5. Business Insight: Find Underutilized Devices
        # Threshold: App opens are less than 50% of registrations
        underutilized = data[data["App_Opens"] < (0.5 * data["Registered_Users"])]
        
        if not underutilized.empty:
            st.warning("⚠️ **Underutilized Devices Detected**")
            st.write("These brands have high registrations but low engagement:")
            st.table(underutilized)
    else:
        st.warning("No data found for the selected filters.")

def insurance_penetration_analysis():
    st.header("🛡️ Insurance Penetration and Growth Potential Analysis")
    st.info("Analyzing where PhonePe users are (and aren't) adopting insurance products.")

    # 1. Get filter options from the database
    # Note: Using the insurance table for years to ensure data exists for comparison
    years_df = visualizer.fetch_data("SELECT DISTINCT Year FROM aggregated_insurance_data ORDER BY Year")
    years = years_df['Year'].astype(str).tolist()
    
    if not years:
        st.error("No insurance data found in the database.")
        return

    selected_year = st.selectbox("Select Year for Analysis", years)

    # 2. SQL Query: Join Insurance Transactions with Total Registered Users
    # We use a JOIN to compare adoption (transactions) against the total user base (registered users)
    query = f"""
        SELECT 
            i.State, 
            SUM(i.Transaction_count) as Total_Insurance_Transactions,
            SUM(i.Transaction_amount) as Total_Insurance_Amount,
            MAX(u.registeredUsers) as Total_Registered_Users
        FROM aggregated_insurance_data i
        JOIN aggregated_user_data u ON i.State = u.State AND i.Year = u.Year
        WHERE i.Year = {selected_year}
        GROUP BY i.State
        ORDER BY Total_Insurance_Transactions DESC
    """
    
    data = visualizer.fetch_data(query)

    if not data.empty:
        # 3. FIX: Convert Decimal/Object types to Numeric (Float) to prevent math errors
        data["Total_Insurance_Transactions"] = pd.to_numeric(data["Total_Insurance_Transactions"], errors='coerce')
        data["Total_Registered_Users"] = pd.to_numeric(data["Total_Registered_Users"], errors='coerce')
        data["Total_Insurance_Amount"] = pd.to_numeric(data["Total_Insurance_Amount"], errors='coerce')

        # 4. Calculate Penetration Rate (%)
        # This tells us what percentage of the user base is actually using insurance
        data["Penetration_Rate"] = (data["Total_Insurance_Transactions"] / data["Total_Registered_Users"]) * 100
        
        # 5. Visualization: Call the visualizer (make sure you added this to datavisulation.py)
        # If you haven't updated datavisulation.py yet, you can use px.scatter here directly.
        fig = visualizer.visualize_insurance_penetration(
            data, 
            title=f"Insurance Penetration vs. User Base by State ({selected_year})"
        )
        st.plotly_chart(fig, use_container_width=True)

        # 6. Business Insight: Identify "High Growth Potential" States
        # Logic: States with a High User Base but Low Penetration
        avg_users = data["Total_Registered_Users"].mean()
        avg_penetration = data["Penetration_Rate"].mean()

        untapped = data[
            (data["Total_Registered_Users"] > avg_users) & 
            (data["Penetration_Rate"] < avg_penetration)
        ].copy()

        st.divider()
        st.subheader("📍 Targeted Growth Opportunities")
        
        if not untapped.empty:
            st.warning(f"The following states have a **large user base** but **low insurance adoption**. Target these for marketing in {selected_year}:")
            
            # Format numbers for better readability in the table
            untapped["Penetration_Rate"] = untapped["Penetration_Rate"].map("{:.2f}%".format)
            untapped["Total_Registered_Users"] = untapped["Total_Registered_Users"].apply(lambda x: f"{x:,.0f}")
            
            st.table(untapped[["State", "Total_Registered_Users", "Penetration_Rate"]])
        else:
            st.success("Insurance adoption is well-distributed relative to the user base across all states.")
            
    else:
        st.warning(f"No matching insurance/user data found for the year {selected_year}.")

def market_expansion_analysis():
    st.header("📈 Transaction Analysis for Market Expansion")
    st.info("Identify high-value states and emerging markets for strategic infrastructure expansion.")

    # 1. Fetch filter options
    years = visualizer.fetch_data("SELECT DISTINCT Year FROM aggregated_transaction_data ORDER BY Year")['Year'].astype(str).tolist()
    selected_year = st.selectbox("Select Year for Expansion Study", years)

    # 2. SQL Query: Aggregate Transaction Data by State
    query = f"""
        SELECT 
            State, 
            SUM(Transaction_count) as Total_Transactions,
            SUM(Transaction_amount) as Total_Amount
        FROM aggregated_transaction_data
        WHERE Year = {selected_year}
        GROUP BY State
        ORDER BY Total_Amount DESC
    """
    
    data = visualizer.fetch_data(query)

    if not data.empty:
        # 3. FIX: Convert Decimal to Float for calculations
        data["Total_Transactions"] = pd.to_numeric(data["Total_Transactions"], errors='coerce')
        data["Total_Amount"] = pd.to_numeric(data["Total_Amount"], errors='coerce')
        
        # Calculate Average Transaction Value (ATV) - helps identify "high-ticket" markets
        data["Avg_Transaction_Value"] = data["Total_Amount"] / data["Total_Transactions"]

        # 4. Visualization: Call the visualizer
        fig = visualizer.visualize_market_expansion(
            data, 
            title=f"Market Size vs. Transaction Frequency ({selected_year})"
        )
        st.plotly_chart(fig, use_container_width=True)

        # 5. Business Insight: Expansion Targets
        # Logic: States with Total Amount > Median but ATV < Median (High volume, need more high-value merchants)
        median_amount = data["Total_Amount"].median()
        
        st.divider()
        st.subheader("🚀 Expansion Strategy: Priority States")
        
        top_states = data[data["Total_Amount"] > median_amount].head(5)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Top 5 Established Markets (Maintain)**")
            st.dataframe(top_states[["State", "Total_Amount"]].style.format({"Total_Amount": "₹{:,.2f}"}))
            
        with col2:
            st.write("**Emerging High-Frequency Markets**")
            emerging = data.sort_values(by="Total_Transactions", ascending=False).head(5)
            st.dataframe(emerging[["State", "Total_Transactions"]])

    else:
        st.warning(f"No transaction data found for the year {selected_year}.")

def user_engagement_growth_strategy():
    st.header("📈 User Engagement and Growth Strategy")
    st.info("Analyze the 'App Opens per User' to identify highly active regions and growth opportunities.")

    # 1. Fetch years and states for filtering
    years = visualizer.fetch_data("SELECT DISTINCT Year FROM map_user_data ORDER BY Year")['Year'].astype(str).tolist()
    states = visualizer.fetch_data("SELECT DISTINCT State FROM map_user_data ORDER BY State")['State'].tolist()

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", years)
    with col2:
        selected_state = st.selectbox("Select State for District Drill-down", ["All"] + states)

    # 2. SQL Query: Join data for Engagement calculation
    # We use map_user_data for district-level precision
    where_clause = f"WHERE Year = {selected_year}"
    if selected_state != "All":
        where_clause += f" AND State = '{selected_state}'"

    query = f"""
        SELECT State, district_name, SUM(registeredUsers) as Total_Users, SUM(appOpens) as Total_Opens
        FROM map_user_data
        {where_clause}
        GROUP BY State, district_name
    """
    
    data = visualizer.fetch_data(query)

    if not data.empty:
        # 3. FIX: Convert to Numeric to avoid Decimal errors
        data["Total_Users"] = pd.to_numeric(data["Total_Users"], errors='coerce')
        data["Total_Opens"] = pd.to_numeric(data["Total_Opens"], errors='coerce')

        # 4. Calculate Engagement Score (App Opens per Registered User)
        data["Engagement_Score"] = data["Total_Opens"] / data["Total_Users"]

        # 5. Visualization: Call the visualizer
        fig = visualizer.visualize_user_engagement_strategy(
            data, 
            title=f"User Engagement Score ({selected_year}) - {'National' if selected_state == 'All' else selected_state}"
        )
        st.plotly_chart(fig, use_container_width=True)

        # 6. Business Insight: Growth Strategy
        st.divider()
        st.subheader("💡 Strategic Insights")
        
        # High Users but Low Engagement = Growth Opportunity
        avg_engagement = data["Engagement_Score"].mean()
        growth_targets = data[data["Engagement_Score"] < avg_engagement].sort_values(by="Total_Users", ascending=False).head(5)

        if not growth_targets.empty:
            st.warning("⚠️ **Retention Risk / Growth Opportunity**: These areas have many users but low app activity. Suggesting targeted notification campaigns.")
            st.table(growth_targets[["State", "district_name", "Total_Users", "Engagement_Score"]])
    else:
        st.warning("No engagement data found for the selection.")




# Call Scenario 2 function
device_dominance_user_engagement()

insurance_penetration_analysis()
market_expansion_analysis()
user_engagement_growth_strategy()