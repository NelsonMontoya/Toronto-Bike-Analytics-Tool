import pandas as pd
from datetime import time

# ============================================================
# Rush Hour Constants (AC 4)
# ============================================================
AM_RUSH_START = time(7, 0, 0)
AM_RUSH_END   = time(8, 59, 59)

PM_RUSH_START = time(16, 0, 0)
PM_RUSH_END   = time(17, 59, 59)


# ============================================================
# Core Logic Function (AC 1)
# ============================================================
def label_rush_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a Boolean column `is_rush_hour` to the DataFrame based on
    the trip start_time.

    Rush hour windows:
    - AM: 07:00:00 to 08:59:59
    - PM: 16:00:00 to 17:59:59

    AC Requirements:
    - Must raise an exception if start_time not present (AC 4)
    - Must add boolean is_rush_hour column (AC 2)
    """

    # ---------------------------
    # AC 4: Dependency Check
    # ---------------------------
    if "start_time" not in df.columns:
        raise KeyError("Input DataFrame must contain a 'start_time' column.")

    # Ensure datetime type
    if not pd.api.types.is_datetime64_any_dtype(df["start_time"]):
        df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")

    # Extract time object from datetime
    start_times = df["start_time"].dt.time

    # ---------------------------
    # AC 3: Rush hour logic
    # Vectorized conditions for performance (AC 1)
    # ---------------------------
    is_am_rush = (start_times >= AM_RUSH_START) & (start_times <= AM_RUSH_END)
    is_pm_rush = (start_times >= PM_RUSH_START) & (start_times <= PM_RUSH_END)

    df["is_rush_hour"] = is_am_rush | is_pm_rush

    return df
