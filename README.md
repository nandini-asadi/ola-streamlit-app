# OLA Bengaluru Operations Dashboard

A comprehensive Streamlit dashboard for analyzing OLA ride-hailing data in Bengaluru. This interactive web application transforms raw ride data into actionable business insights through rich visualizations and real-time analytics.

🔗 **Live Dashboard**: [https://ola-dashboard.streamlit.app/](https://ola-dashboard.streamlit.app/)

## What It Does

This dashboard provides comprehensive analysis of OLA ride operations including:

- **Revenue Analytics**: Track total revenue, average earnings per ride, and revenue distribution by vehicle types
- **Operational Metrics**: Monitor booking success rates, ride completion statistics, and demand patterns
- **Customer Insights**: Analyze payment preferences, customer ratings, and service quality metrics
- **Temporal Analysis**: Understand daily trends, hourly demand patterns, and peak operation times
- **Geographic Intelligence**: Distance analysis and route optimization insights

## Key Features

### 📊 Interactive Filters
- Filter data by vehicle type (Prime Sedan, Bike, Prime SUV, Auto, etc.)
- Filter by booking status (Trip Completed, Cancelled by Driver/Customer)
- Real-time data updates based on filter selections

### 📈 Rich Visualizations
- **Revenue by Vehicle Type**: Bar chart showing earnings across different vehicle categories
- **Booking Status Distribution**: Pie chart displaying success vs cancellation rates
- **Daily Ride Trends**: Time series analysis of ride patterns over time
- **Hourly Demand Patterns**: Heatmap showing peak and off-peak hours
- **Payment Method Analysis**: Distribution of payment preferences (Cash, Online, Wallet)
- **Rating Comparisons**: Service quality metrics across vehicle types

### 🎯 Business Intelligence
- **KPI Dashboard**: Real-time metrics including total revenue, bookings, success rate, and average distance
- **Data Export**: Download filtered datasets for further analysis
- **Professional UI**: OLA-themed design with responsive layout

## How to Use This Dashboard

### 1. **Access the Dashboard**
Visit [https://ola-dashboard.streamlit.app/](https://ola-dashboard.streamlit.app/) in your web browser.

### 2. **Apply Filters**
- Use the sidebar to select specific vehicle types you want to analyze
- Choose booking statuses to focus on successful rides or cancellations
- Filters automatically update all visualizations and metrics

### 3. **Analyze Key Metrics**
- **Total Revenue**: Monitor overall earnings
- **Total Bookings**: Track ride volume
- **Success Rate**: Measure operational efficiency
- **Average Distance**: Understand trip characteristics

### 4. **Explore Visualizations**
- **Revenue Analysis**: Identify which vehicle types generate the most revenue
- **Booking Patterns**: Understand cancellation reasons and success factors
- **Time-based Trends**: Discover peak hours and seasonal patterns
- **Payment Insights**: Analyze customer payment preferences
- **Quality Metrics**: Review customer satisfaction through ratings

### 5. **Export Data**
- Expand the "View Raw Data" section to inspect filtered datasets
- Use the download button to export data for offline analysis
- Perfect for creating custom reports or deeper statistical analysis

## Business Use Cases

### For Operations Managers
- **Resource Allocation**: Deploy vehicles based on demand patterns
- **Performance Monitoring**: Track success rates and identify improvement areas
- **Revenue Optimization**: Focus on high-performing vehicle types and time slots

### For Business Analysts
- **Trend Analysis**: Identify seasonal patterns and growth opportunities
- **Customer Behavior**: Understand payment preferences and rating patterns
- **Market Intelligence**: Compare performance across different service categories

### For Strategic Planning
- **Capacity Planning**: Use hourly demand data for fleet management
- **Pricing Strategy**: Leverage revenue insights for dynamic pricing
- **Service Improvement**: Address low-rated services and cancellation causes

## Technical Details

- **Built with**: Streamlit, Pandas, Plotly
- **Data Processing**: Real-time filtering and aggregation
- **Visualization**: Interactive charts with hover details and zoom capabilities
- **Performance**: Optimized with caching for fast loading
- **Responsive**: Works on desktop, tablet, and mobile devices

## Dataset Information

The dashboard analyzes OLA ride data from Bengaluru including:
- Ride details (date, time, distance, duration)
- Vehicle information (type, category)
- Booking status (completed, cancelled)
- Payment methods and customer ratings
- Revenue and pricing data

---

*This dashboard transforms complex ride-hailing data into clear, actionable insights for data-driven decision making in the transportation industry.*
