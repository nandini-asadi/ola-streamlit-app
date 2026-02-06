# OLA Bengaluru Operations Dashboard

A professional Streamlit dashboard for analyzing OLA ride-hailing data in Bengaluru. This interactive web application provides comprehensive insights into ride operations, revenue analysis, and business performance metrics.

## Features

- **Interactive Filters**: Filter data by vehicle type and booking status
- **KPI Metrics**: Real-time display of total revenue, bookings, success rate, and average distance
- **Rich Visualizations**: 
  - Revenue analysis by vehicle type
  - Booking status distribution
  - Daily ride trends
  - Hourly demand patterns
  - Payment method analysis
  - Rating comparisons
- **Data Export**: Download filtered data as CSV
- **Professional UI**: OLA-themed design with responsive layout

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone or download the project files**
   ```bash
   git clone <your-repo-url>
   cd nandu-ai-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure your CSV file is in the project directory**
   - Place `Bengaluru Ola.csv` in the same folder as `app.py`

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## Deployment on Streamlit Cloud

### Option 1: GitHub Integration (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select your repository and branch
   - Set main file path: `app.py`
   - Click "Deploy"

### Option 2: Direct Upload

1. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Create account if needed

2. **Upload files directly**
   - Upload `app.py`, `requirements.txt`, and `Bengaluru Ola.csv`
   - Deploy the application

## File Structure

```
nandu-ai-project/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Bengaluru Ola.csv     # Dataset file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Usage

1. **Filters**: Use the sidebar to filter data by vehicle types and booking status
2. **KPIs**: Monitor key performance indicators at the top of the dashboard
3. **Charts**: Analyze various aspects of the business through interactive visualizations
4. **Raw Data**: Expand the "View Raw Data" section to inspect filtered data
5. **Export**: Download filtered data using the download button

## Dependencies

- `streamlit==1.28.1` - Web app framework
- `pandas==2.1.1` - Data manipulation
- `plotly==5.17.0` - Interactive visualizations
- `numpy==1.24.3` - Numerical computations

## Troubleshooting

### Common Issues

1. **CSV file not found**
   - Ensure `Bengaluru Ola.csv` is in the same directory as `app.py`

2. **Module not found errors**
   - Run `pip install -r requirements.txt` to install all dependencies

3. **Port already in use**
   - Use `streamlit run app.py --server.port 8502` to run on a different port

4. **Memory issues with large datasets**
   - The app uses caching to optimize performance
   - For very large datasets, consider data sampling

### Performance Tips

- The app uses `@st.cache_data` for efficient data loading
- Filters are applied dynamically to improve responsiveness
- Charts are optimized for fast rendering

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are correctly installed
3. Verify the CSV file format matches the expected schema

## License

This project is open source and available under the MIT License.
