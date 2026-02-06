import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="OLA Bengaluru Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for OLA theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the data"""
    df = pd.read_csv('Bengaluru Ola.csv')
    
    # Data preprocessing
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    
    # Handle missing values
    df['Booking Value'] = df['Booking Value'].fillna(0)
    df['Driver Ratings'] = df['Driver Ratings'].fillna(df['Driver Ratings'].mean())
    df['Customer Rating'] = df['Customer Rating'].fillna(df['Customer Rating'].mean())
    df['Ride Distance'] = df['Ride Distance'].fillna(df['Ride Distance'].mean())
    
    return df

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 OLA Bengaluru Operations Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time insights into ride-hailing operations and business performance</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    vehicle_types = st.sidebar.multiselect(
        "Select Vehicle Types:",
        options=df['Vehicle Type'].unique(),
        default=df['Vehicle Type'].unique()
    )
    
    booking_status = st.sidebar.multiselect(
        "Select Booking Status:",
        options=df['Booking Status'].unique(),
        default=df['Booking Status'].unique()
    )
    
    # Filter data
    filtered_df = df[
        (df['Vehicle Type'].isin(vehicle_types)) & 
        (df['Booking Status'].isin(booking_status))
    ]
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = filtered_df['Booking Value'].sum()
    total_bookings = len(filtered_df)
    success_rate = (len(filtered_df[filtered_df['Booking Status'] == 'Success']) / total_bookings * 100) if total_bookings > 0 else 0
    avg_distance = filtered_df['Ride Distance'].mean()
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"₹{total_revenue:,.0f}",
            delta=f"{total_revenue/1000000:.1f}M"
        )
    
    with col2:
        st.metric(
            label="📱 Total Bookings",
            value=f"{total_bookings:,}",
            delta=f"{total_bookings/1000:.1f}K"
        )
    
    with col3:
        st.metric(
            label="✅ Success Rate",
            value=f"{success_rate:.1f}%",
            delta="Target: 85%"
        )
    
    with col4:
        st.metric(
            label="🛣️ Avg Distance",
            value=f"{avg_distance:.1f} km",
            delta=f"{avg_distance:.1f} km"
        )
    
    st.divider()
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    # Revenue by Vehicle Type
    with col1:
        st.subheader("💰 Revenue by Vehicle Type")
        revenue_by_vehicle = filtered_df.groupby('Vehicle Type')['Booking Value'].sum().reset_index()
        fig1 = px.bar(
            revenue_by_vehicle,
            x='Vehicle Type',
            y='Booking Value',
            color='Vehicle Type',
            color_discrete_sequence=['#FFD700', '#FFA500', '#FF8C00', '#FF7F50', '#FF6347', '#FF4500', '#FF0000']
        )
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, width='stretch')
    
    # Booking Status Distribution
    with col2:
        st.subheader("📊 Booking Status Distribution")
        status_counts = filtered_df['Booking Status'].value_counts()
        fig2 = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color_discrete_sequence=['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1']
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, width='stretch')
    
    col3, col4 = st.columns(2)
    
    # Daily Ride Trends
    with col3:
        st.subheader("📈 Daily Ride Trends")
        daily_rides = filtered_df.groupby('Date').size().reset_index(name='Ride Count')
        fig3 = px.line(
            daily_rides,
            x='Date',
            y='Ride Count',
            line_shape='spline'
        )
        fig3.update_traces(line_color='#FFD700', line_width=3)
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, width='stretch')
    
    # Hourly Demand Pattern
    with col4:
        st.subheader("🕐 Hourly Demand Pattern")
        hourly_demand = filtered_df.groupby('Hour').size().reset_index(name='Ride Count')
        fig4 = px.bar(
            hourly_demand,
            x='Hour',
            y='Ride Count',
            color='Ride Count',
            color_continuous_scale='Viridis'
        )
        fig4.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig4, width='stretch')
    
    # Additional insights
    st.divider()
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("💳 Payment Method Distribution")
        payment_dist = filtered_df['Payment Method'].value_counts()
        fig5 = px.pie(
            values=payment_dist.values,
            names=payment_dist.index,
            color_discrete_sequence=['#FFD700', '#FF8C00', '#4ECDC4', '#45B7D1'],
            hole=0.4
        )
        st.plotly_chart(fig5, width='stretch')
    
    with col6:
        st.subheader("⭐ Average Ratings Comparison")
        avg_ratings = pd.DataFrame({
            'Rating Type': ['Driver Rating', 'Customer Rating'],
            'Average Rating': [
                filtered_df['Driver Ratings'].mean(),
                filtered_df['Customer Rating'].mean()
            ]
        })
        fig6 = px.bar(
            avg_ratings,
            x='Rating Type',
            y='Average Rating',
            color='Rating Type',
            color_discrete_sequence=['#FFD700', '#FF8C00']
        )
        fig6.update_layout(showlegend=False, yaxis_range=[0, 5])
        st.plotly_chart(fig6, width='stretch')
    
    # Raw data inspection
    with st.expander("🔍 View Raw Data"):
        st.dataframe(
            filtered_df,
            width='stretch',
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"ola_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
