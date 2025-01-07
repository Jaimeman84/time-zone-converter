# app.py
import streamlit as st
from datetime import datetime, timedelta
import pytz
from timezone_utils import get_top5_timezone_times, get_current_est_time

def get_card_color(time_diff):
    """Return background color based on time difference."""
    if abs(time_diff) <= 3:
        return "#4CAF50"
    elif abs(time_diff) <= 6:
        return "#FFA726"
    else:
        return "#EF5350"

def format_time_diff(diff):
    """Format time difference for display."""
    if diff == 0:
        return "Same time"
    elif diff > 0:
        return f"+{diff:.0f}h ahead"
    else:
        return f"{diff:.0f}h behind"

def main():
    st.set_page_config(
        page_title="Time Zone Converter",
        page_icon="🕒",
        layout="centered"
    )
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main > div {
            max-width: 50%;
        }
        .time-card {
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin: 10px 0;
            text-align: center;
        }
        .time-display {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        .city-name {
            font-size: 24px;
            margin-bottom: 5px;
        }
        .time-diff {
            font-size: 16px;
            opacity: 0.9;
        }
        div[data-testid="stMarkdownContainer"] {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("# 🌍 Time Zone Converter")
    st.markdown("### Convert EST time to major global cities")

    # Get current EST time
    current_est = get_current_est_time()
    
    # Custom time inputs
    col1, col2 = st.columns(2)
    
    with col1:
        hours = st.number_input(
            "Hour (24h format)",
            min_value=0,
            max_value=23,
            value=current_est.hour
        )
    
    with col2:
        minutes = st.number_input(
            "Minutes",
            min_value=0,
            max_value=59,
            value=current_est.minute
        )

    # Date selection
    source_date = st.date_input(
        "Select date",
        value=current_est.date(),
        min_value=current_est.date()
    )

    # Combine inputs into datetime
    source_datetime = datetime.combine(
        source_date, 
        datetime.strptime(f"{hours:02d}:{minutes:02d}", "%H:%M").time()
    )
    est_tz = pytz.timezone('America/New_York')
    source_datetime = est_tz.localize(source_datetime)

    # Display selected time
    st.markdown(f"### Selected Time (EST): {source_datetime.strftime('%Y-%m-%d %H:%M')}")

    if st.button("Show Times", type="primary", use_container_width=True):
        timezone_info, error = get_top5_timezone_times(source_datetime)
        
        if error:
            st.error(f"Error occurred: {error}")
        else:
            # Create two columns for cards
            cols = st.columns(2)
            
            # Display timezone cards
            for idx, tz_info in enumerate(timezone_info):
                col_idx = idx % 2
                
                with cols[col_idx]:
                    bg_color = get_card_color(tz_info['time_diff'])
                    
                    st.markdown(f"""
                        <div class="time-card" style="background-color: {bg_color}">
                            <div class="city-name">{tz_info['city']}</div>
                            <div class="time-display">
                                {tz_info['local_time'].strftime('%H:%M')}
                            </div>
                            <div class="time-diff">
                                {format_time_diff(tz_info['time_diff'])}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # Color guide
            st.markdown("""
                🟢 Similar time (±3h) · 🟡 Moderate difference (±6h) · 🔴 Large difference (>6h)
            """)

if __name__ == "__main__":
    main()