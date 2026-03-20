import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from sqlalchemy import create_engine,text


class DataVisualization:
    def __init__(self, db_config):
        self.db_config = db_config
        self.engine = create_engine(f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}/{db_config["database"]}')
    
    def fetch_data(self, query):
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            columns = result.keys()
            return pd.DataFrame(data, columns=columns)
    def format_indian_currency(self,value):
        if value >= 10000000:
            return f"₹{value/10000000:.2f} Cr"
        elif value >= 100000:
            return f"₹{value/100000:.2f} L"
        return f"₹{value:,.2f}"
    
    def visualize_data_amount_by_state(self, data, title='Total Transaction Amount by State'):
        # Code to visualize the data using libraries like matplotlib or seaborn
        india_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        data['state'] = data['state'].str.replace('-', ' ').str.title()
        data['state'] = data['state'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar Island') 
        data['Total_Amount'] = pd.to_numeric(data['Total_Amount'], errors='coerce')
    
        # 3. SCALE DATA: Create a numeric column for the gradient (e.g., in Crores)
        data['Amount_in_Cr'] = data['Total_Amount'] / 10000000
        
        # 4. FORMAT FOR HOVER: This is just for the text popup
        data['Formatted_Amount'] = data['Total_Amount'].apply(self.format_indian_currency)

        # 5. CREATE MAP: 
        fig = px.choropleth(
            data,
            geojson=india_geojson_url,
            featureidkey='properties.ST_NM',
            locations='state',
            color='Amount_in_Cr',            
            color_continuous_scale="Blues", 
            hover_name='state',
            custom_data=['Formatted_Amount'],
            title=title
        )

        # 6. ENFORCE GRADIENT RANGE (Optional: Helps if one state is huge)
        fig.update_coloraxes(colorbar_title="Amount (₹ Cr)")

        fig.update_geos(fitbounds="locations", visible=False)
        return fig

    def visualize_device_engagement(self, data, title='Device Engagement'):
        """Visualize device engagement (registered users vs app opens) by device brand."""
        # Ensure numeric columns are treated as numeric
        data['Registered_Users'] = pd.to_numeric(data.get('Registered_Users', pd.Series()), errors='coerce')
        data['App_Opens'] = pd.to_numeric(data.get('App_Opens', pd.Series()), errors='coerce')

        

        fig = px.bar(
            data,
            x='brand',
            y=['Registered_Users', 'App_Opens'],
            barmode='group',
            title=title,
            labels={'brand': 'Device Brand', 'value': 'Count'}
        )
        return fig

    def visualize_insurance_penetration(self, data, title):
        import plotly.express as px
        fig = px.scatter(
            data, 
            x="Total_Registered_Users", 
            y="Penetration_Rate",
            size="Total_Insurance_Transactions", 
            color="State",
            hover_name="State",
            title=title,
            labels={
                "Penetration_Rate": "Penetration (%)", 
                "Total_Registered_Users": "Registered Users"
            }
        )
        return fig
    
    def visualize_market_expansion(self, data, title):
        import plotly.express as px
        # Treemap: Large boxes = High Transaction Amount, Color = Avg Transaction Value
        fig = px.treemap(
            data, 
            path=['State'], 
            values='Total_Amount',
            color='Avg_Transaction_Value',
            color_continuous_scale='RdYlGn',
            title=title,
            labels={'Total_Amount': 'Market Size (₹)', 'Avg_Transaction_Value': 'Avg. Ticket Size'}
        )
        return fig
    
    def visualize_user_engagement_strategy(self, data, title):
        import plotly.express as px
        # Color represents the Engagement Score (Darker = More Active)
        fig = px.bar(
            data.sort_values(by="Engagement_Score", ascending=False).head(20), 
            x="district_name", 
            y="Engagement_Score",
            color="Engagement_Score",
            text_auto='.2f',
            title=title,
            labels={"district_name": "District", "Engagement_Score": "Opens per User"},
            color_continuous_scale="Viridis"
        )
        return fig




