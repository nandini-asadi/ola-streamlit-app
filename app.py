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
    """Load and preprocess the data with fact-dimension model structure"""
    df = pd.read_csv('Bengaluru Ola.csv')
    
    # Data preprocessing
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    
    # Handle missing values safely
    df['Booking Value'] = pd.to_numeric(df['Booking Value'], errors='coerce').fillna(0)
    df['Driver Ratings'] = pd.to_numeric(df['Driver Ratings'], errors='coerce').fillna(df['Driver Ratings'].mean())
    df['Customer Rating'] = pd.to_numeric(df['Customer Rating'], errors='coerce').fillna(df['Customer Rating'].mean())
    df['Ride Distance'] = pd.to_numeric(df['Ride Distance'], errors='coerce').fillna(df['Ride Distance'].mean())
    
    # Clean string columns for dimensions
    string_cols = ['Vehicle Type', 'Pickup Location', 'Drop Location', 'Payment Method', 'Booking Status']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(['nan', 'NaN', 'None', ''], 'Unknown')
    
    # Create booking status count for fact table (1 for each ride)
    df['Booking Count'] = 1
    
    return df

def get_dimension_config():
    """Define fact-dimension model configuration"""
    return {
        'Vehicle Type': 'Vehicle Type',
        'Pickup Location': 'Pickup Location', 
        'Drop Location': 'Drop Location',
        'Customer ID': 'Customer ID',
        'Payment Method': 'Payment Method'
    }

def get_relationship_filters(selected_dimension):
    """Get contextual relationship filters based on selected dimension"""
    relationships = {
        'Vehicle Type': {
            'Payment Method': ['Payment Method', ['Cash', 'Wallet', 'Card', 'UPI']],
            'Booking Status': ['Booking Status', ['Success', 'Cancelled by Driver', 'Cancelled by Customer', 'Incomplete']],
            'Customer Rating': ['Customer Rating', 'rating_range'],
            'Driver Rating': ['Driver Ratings', 'rating_range']
        },
        'Pickup Location': {
            'Vehicle Type': ['Vehicle Type', ['Auto', 'Bike', 'Mini', 'Prime Plus', 'Prime SUV', 'Prime Sedan', 'eBike']],
            'Payment Method': ['Payment Method', ['Cash', 'Wallet', 'Card', 'UPI']],
            'Booking Status': ['Booking Status', ['Success', 'Cancelled by Driver', 'Cancelled by Customer', 'Incomplete']],
            'Distance Range': ['Ride Distance', 'distance_range']
        },
        'Drop Location': {
            'Vehicle Type': ['Vehicle Type', ['Auto', 'Bike', 'Mini', 'Prime Plus', 'Prime SUV', 'Prime Sedan', 'eBike']],
            'Payment Method': ['Payment Method', ['Cash', 'Wallet', 'Card', 'UPI']],
            'Booking Status': ['Booking Status', ['Success', 'Cancelled by Driver', 'Cancelled by Customer', 'Incomplete']],
            'Distance Range': ['Ride Distance', 'distance_range']
        },
        'Customer ID': {
            'Vehicle Preference': ['Vehicle Type', ['Auto', 'Bike', 'Mini', 'Prime Plus', 'Prime SUV', 'Prime Sedan', 'eBike']],
            'Payment Method': ['Payment Method', ['Cash', 'Wallet', 'Card', 'UPI']],
            'Booking Status': ['Booking Status', ['Success', 'Cancelled by Driver', 'Cancelled by Customer', 'Incomplete']],
            'Rating Given': ['Customer Rating', 'rating_range']
        },
        'Payment Method': {
            'Vehicle Usage': ['Vehicle Type', ['Auto', 'Bike', 'Mini', 'Prime Plus', 'Prime SUV', 'Prime Sedan', 'eBike']],
            'Booking Status': ['Booking Status', ['Success', 'Cancelled by Driver', 'Cancelled by Customer', 'Incomplete']],
            'Distance Range': ['Ride Distance', 'distance_range'],
            'Value Range': ['Booking Value', 'value_range']
        }
    }
    return relationships.get(selected_dimension, {})

def apply_dynamic_filter(df, dimension_column, selected_values):
    """Apply dynamic filtering based on selected dimension and values"""
    if not dimension_column or not selected_values:
        return df
    
    # Handle null/missing values safely
    mask = df[dimension_column].notna() & df[dimension_column].isin(selected_values)
    return df[mask]

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 OLA Bengaluru Operations Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time insights into ride-hailing operations and business performance</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters - Simplified Dynamic Filtering
    st.sidebar.header("📊 Analysis Filters")
    
    # Dimension selector dropdown
    dimension_config = get_dimension_config()
    selected_dimension = st.sidebar.selectbox(
        "Analyze by:",
        options=['All Data'] + list(dimension_config.keys()),
        help="Choose how you want to analyze the data"
    )
    
    # Dynamic value selector based on selected dimension
    filtered_df = df.copy()
    if selected_dimension != 'All Data':
        dimension_column = dimension_config[selected_dimension]
        unique_values = df[dimension_column].dropna().unique()
        unique_values = [str(val) for val in unique_values if str(val) != 'Unknown']
        
        selected_values = st.sidebar.multiselect(
            f"Select {selected_dimension}:",
            options=sorted(unique_values),
            default=sorted(unique_values),
            help=f"Choose specific {selected_dimension.lower()} values to analyze"
        )
        
        if selected_values:
            filtered_df = apply_dynamic_filter(df, dimension_column, selected_values)
            
            # Contextual relationship filters
            st.sidebar.divider()
            st.sidebar.subheader("🔗 Related Insights")
            
            relationships = get_relationship_filters(selected_dimension)
            for relation_name, (relation_column, relation_values) in relationships.items():
                if relation_column in filtered_df.columns:
                    if isinstance(relation_values, list):
                        # Use predefined values, filter only those present in data
                        available_values = [val for val in relation_values if val in filtered_df[relation_column].values]
                    elif relation_values == 'rating_range':
                        available_values = ['High (4-5)', 'Medium (3-4)', 'Low (3-3.5)']
                    elif relation_values == 'distance_range':
                        available_values = ['Short (1-15km)', 'Medium (15-30km)', 'Long (30km+)']
                    elif relation_values == 'value_range':
                        available_values = ['Low (₹50-500)', 'Medium (₹500-1000)', 'High (₹1000+)']
                    
                    if available_values:
                        relation_filter = st.sidebar.multiselect(
                            f"{relation_name}:",
                            options=available_values,
                            default=available_values,
                            key=f"relation_{relation_name}"
                        )
                        
                        # Apply relationship filter
                        if relation_filter:
                            if relation_values == 'rating_range':
                                mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
                                if 'High (4-5)' in relation_filter:
                                    mask |= (filtered_df[relation_column] >= 4)
                                if 'Medium (3-4)' in relation_filter:
                                    mask |= ((filtered_df[relation_column] >= 3) & (filtered_df[relation_column] < 4))
                                if 'Low (3-3.5)' in relation_filter:
                                    mask |= ((filtered_df[relation_column] >= 3) & (filtered_df[relation_column] < 3.5))
                                filtered_df = filtered_df[mask]
                            elif relation_values == 'distance_range':
                                mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
                                if 'Short (1-15km)' in relation_filter:
                                    mask |= (filtered_df[relation_column] <= 15)
                                if 'Medium (15-30km)' in relation_filter:
                                    mask |= ((filtered_df[relation_column] > 15) & (filtered_df[relation_column] <= 30))
                                if 'Long (30km+)' in relation_filter:
                                    mask |= (filtered_df[relation_column] > 30)
                                filtered_df = filtered_df[mask]
                            elif relation_values == 'value_range':
                                mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
                                if 'Low (₹50-500)' in relation_filter:
                                    mask |= (filtered_df[relation_column] <= 500)
                                if 'Medium (₹500-1000)' in relation_filter:
                                    mask |= ((filtered_df[relation_column] > 500) & (filtered_df[relation_column] <= 1000))
                                if 'High (₹1000+)' in relation_filter:
                                    mask |= (filtered_df[relation_column] > 1000)
                                filtered_df = filtered_df[mask]
                            else:
                                filtered_df = filtered_df[filtered_df[relation_column].isin(relation_filter)]
    
    # KPI Metrics - Fact measures from filtered data
    col1, col2, col3, col4 = st.columns(4)
    
    # Fact measures: Booking Value, Ride Distance, Booking Status count
    total_revenue = filtered_df['Booking Value'].sum()
    total_bookings = len(filtered_df)  # Use len() as fallback for booking count
    success_rate = (len(filtered_df[filtered_df['Booking Status'] == 'Success']) / total_bookings * 100) if total_bookings > 0 else 0
    avg_distance = filtered_df['Ride Distance'].mean()
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"₹{total_revenue:,.0f}",
            delta=f"{total_revenue/1000000:.1f}M" if total_revenue > 0 else "0"
        )
    
    with col2:
        st.metric(
            label="📱 Total Bookings", 
            value=f"{total_bookings:,}",
            delta=f"{total_bookings/1000:.1f}K" if total_bookings > 0 else "0"
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
            value=f"{avg_distance:.1f} km" if not pd.isna(avg_distance) else "0 km",
            delta=f"{avg_distance:.1f} km" if not pd.isna(avg_distance) else "0 km"
        )
    
    # Display active filter info
    if selected_dimension != 'All Data':
        st.info(f"📊 **Analyzing by**: {selected_dimension} | **Data Points**: {len(filtered_df):,} rides")
    else:
        st.info(f"📊 **Analyzing**: Complete Dataset | **Data Points**: {len(filtered_df):,} rides")
    
    st.divider()
    
    # Visualizations - All charts update dynamically based on filtered data
    col1, col2 = st.columns(2)
    
    # Revenue by Vehicle Type (Fact: Booking Value, Dimension: Vehicle Type)
    with col1:
        st.subheader("💰 Revenue by Vehicle Type")
        if not filtered_df.empty:
            revenue_by_vehicle = filtered_df.groupby('Vehicle Type')['Booking Value'].sum().reset_index()
            fig1 = px.bar(
                revenue_by_vehicle,
                x='Vehicle Type',
                y='Booking Value',
                color='Vehicle Type',
                color_discrete_sequence=['#FFD700', '#FFA500', '#FF8C00', '#FF7F50', '#FF6347', '#FF4500', '#FF0000']
            )
            fig1.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("No data available for selected filters")
    
    # Booking Status Distribution (Fact: Booking Count, Dimension: Booking Status)
    with col2:
        st.subheader("📊 Booking Status Distribution")
        if not filtered_df.empty:
            status_counts = filtered_df['Booking Status'].value_counts()
            fig2 = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color_discrete_sequence=['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1']
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No data available for selected filters")
    
    col3, col4 = st.columns(2)
    
    # Daily Ride Trends (Fact: Booking Count, Dimension: Date)
    with col3:
        st.subheader("📈 Daily Ride Trends")
        if not filtered_df.empty:
            daily_rides = filtered_df.groupby('Date').size().reset_index(name='Ride Count')
            fig3 = px.line(
                daily_rides,
                x='Date',
                y='Ride Count',
                line_shape='spline'
            )
            fig3.update_traces(line_color='#FFD700', line_width=3)
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("No data available for selected filters")
    
    # Hourly Demand Pattern (Fact: Booking Count, Dimension: Hour)
    with col4:
        st.subheader("🕐 Hourly Demand Pattern")
        if not filtered_df.empty:
            hourly_demand = filtered_df.groupby('Hour').size().reset_index(name='Ride Count')
            fig4 = px.bar(
                hourly_demand,
                x='Hour',
                y='Ride Count',
                color='Ride Count',
                color_continuous_scale='Viridis'
            )
            fig4.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("No data available for selected filters")
    
    # Additional insights - Dynamic visualizations
    st.divider()
    
    col5, col6 = st.columns(2)
    
    # Payment Method Distribution (Fact: Booking Count, Dimension: Payment Method)
    with col5:
        st.subheader("💳 Payment Method Distribution")
        if not filtered_df.empty and 'Payment Method' in filtered_df.columns:
            payment_dist = filtered_df['Payment Method'].value_counts()
            if not payment_dist.empty:
                fig5 = px.pie(
                    values=payment_dist.values,
                    names=payment_dist.index,
                    color_discrete_sequence=['#FFD700', '#FF8C00', '#4ECDC4', '#45B7D1'],
                    hole=0.4
                )
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.warning("No payment method data available")
        else:
            st.warning("No data available for selected filters")
    
    # Average Ratings Comparison (Fact: Rating values)
    with col6:
        st.subheader("⭐ Average Ratings Comparison")
        if not filtered_df.empty:
            driver_avg = filtered_df['Driver Ratings'].mean()
            customer_avg = filtered_df['Customer Rating'].mean()
            
            if not (pd.isna(driver_avg) and pd.isna(customer_avg)):
                avg_ratings = pd.DataFrame({
                    'Rating Type': ['Driver Rating', 'Customer Rating'],
                    'Average Rating': [
                        driver_avg if not pd.isna(driver_avg) else 0,
                        customer_avg if not pd.isna(customer_avg) else 0
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
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.warning("No rating data available")
        else:
            st.warning("No data available for selected filters")
    
    # Raw data inspection with dynamic filtering applied
    with st.expander("🔍 View Filtered Data"):
        if not filtered_df.empty:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )
            
            # Download button for filtered data
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"ola_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data matches the selected filters")

if __name__ == "__main__":
    main()
