# app.py
import streamlit as st
from datetime import datetime
import pytz
from timezone_utils import get_top5_timezone_times
import time

def get_card_color(time_diff):
    """Return background color based on time difference."""
    if abs(time_diff) <= 3:
        return "#4CAF50"  # Green for similar times
    elif abs(time_diff) <= 6:
        return "#FFA726"  # Orange for moderate difference
    else:
        return "#EF5350"  # Red for large difference

def format_time_diff(diff):
    """Format time difference for display."""
    if diff == 0:
        return "Same time"
    elif diff > 0:
        return f"+{diff:.0f}h ahead"
    else:
        return f"{diff:.0f}h behind"

def format_12hour_time(dt):
    """Convert datetime to 12-hour format with AM/PM."""
    return dt.strftime('%I:%M:%S %p')

def main():
    st.set_page_config(
        page_title="Top 5 Time Zones",
        page_icon="🕒",
        layout="wide"
    )
    
    # Custom CSS for cards and centered layout
    st.markdown("""
        <style>
        .stApp {
            text-align: center;
        }
        .time-card {
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin: 10px auto;
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
        .css-1629p8f h1 {  /* Center title */
            text-align: center;
        }
        .css-1629p8f h3 {  /* Center headings */
            text-align: center;
        }
        .css-1629p8f p {   /* Center paragraphs */
            text-align: center;
        }
        /* Center date and time inputs */
        .css-1x8cf1d {
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        .stButton {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Major Time Zones Converter")
    st.write("View current time across major global cities based on EST")

    # Center the input controls using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        source_date = st.date_input("Select date")
        source_time = st.time_input("Select time")
        source_datetime = datetime.combine(source_date, source_time)

    if st.button("Show Times", type="primary"):
        timezone_info, error = get_top5_timezone_times(source_datetime)
        
        if error:
            st.error(f"Error occurred: {error}")
        else:
            # Create three columns for cards
            cols = st.columns(3)
            
            # Display timezone cards
            for idx, tz_info in enumerate(timezone_info):
                col_idx = idx % 3
                
                with cols[col_idx]:
                    # Card container
                    bg_color = get_card_color(tz_info['time_diff'])
                    
                    st.markdown(f"""
                        <div class="time-card" style="background-color: {bg_color}">
                            <div class="city-name">{tz_info['city']}</div>
                            <div class="time-display">
                                {format_12hour_time(tz_info['local_time'])}
                            </div>
                            <div class="time-diff">
                                {format_time_diff(tz_info['time_diff'])}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # Add information about color coding
            st.markdown("### Color Guide")
            st.markdown("""
                🟢 Green: Similar time zone (±3 hours)
                🟡 Orange: Moderate difference (±4-6 hours)
                🔴 Red: Large time difference (>6 hours)
            """)

if __name__ == "__main__":
    main()