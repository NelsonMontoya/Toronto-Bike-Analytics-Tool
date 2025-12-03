
# src/config.py
import os
from datetime import time
# --- FILE PATHS ---
# Determine the base directory dynamically
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data')
# DATA_FILE_PATH = os.path.join(DATA_DIR, 'bike_share_data.csv')
DATA_FILE_PATH = os.path.join(os.getcwd(), 'data', 'bike_share_data.csv')

# --- DATA SCHEMA (Column Names) ---
TRIP_ID_COL = 'Trip Id'
TRIP_DURATION_COL = 'Trip  Duration'
START_TIME_COL = 'Start Time'
END_TIME_COL = 'End Time'
USER_TYPE_COL = 'User Type'
START_STATION_COL = 'Start Station Name'
END_STATION_COL = 'End Station Name'
START_STATION_ID_COL = 'Start Station Id'
END_STATION_ID_COL = 'End Station Id'
BIKE_ID_COL = 'Bike Id'
MODEL_COL = 'Model'


# --- FEATURE COLUMNS ---
DURATION_MIN_COL = 'trip_duration_min'
IS_RUSH_HOUR_COL = 'is_rush_hour'
DISTANCE_KM_COL = 'distance_km'

# --- RUSH HOUR CONSTANTS (Used in US-3 and US-13) ---
AM_RUSH_START = time(7, 0, 0)   # 7:00 AM
AM_RUSH_END = time(9, 0, 0)     # 9:00 AM
PM_RUSH_START = time(16, 0, 0)  # 4:00 PM
PM_RUSH_END = time(18, 0, 0)    # 6:00 PM

# --- DATA CLEANING CONSTANTS ---
DATETIME_COLS = [START_TIME_COL, END_TIME_COL]

