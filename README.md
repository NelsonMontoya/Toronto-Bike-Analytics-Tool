

# 🚴 Toronto Bike Analytics Tool (Streamlit Dashboard)

An interactive dashboard built with Streamlit and Python to visualize and analyze historical bike-sharing trip data from Toronto's 
Bike Share system. Explore trends in trip duration, time of day, popular stations, and user demographics.

## ✨ Key Features

* **Interactive Filtering:** Use sidebar widgets (like sliders for duration and time) to drill down into specific data segments.
* **Trip Duration Analysis:** Visualize trip length distributions.
* **Temporal Analysis:** Examine ridership trends by hour of day, day of the week, and month.
* **User Segmentation:** Compare ridership between casual users and annual members.

## 🚀 Getting Started

### Prerequisites

You need **Python 3.10+** and the following libraries:

* Streamlit
* Pandas
* Plotly (or Matplotlib/Seaborn, depending on what you used)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/nelsonbenitez/Toronto-Bike-Analytics-Tool.git](https://github.com/nelsonbenitez/Toronto-Bike-Analytics-Tool.git)
    cd Toronto-Bike-Analytics-Tool
    ```
2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

Execute the main dashboard script:

```bash
streamlit run dashboard.py
 ```
### 4. Data Source

Always acknowledge where the data comes from.


## 📊 Data Source

This tool utilizes publicly available data from the **Toronto Bike Share** system, typically sourced from their Open Data portal 
or similar providers. Data files are expected to be in a directory (e.g., `./data/`) and formatted as CSV.

## 📂 Project Structure

* `dashboard.py`: The main Streamlit script that defines the layout and handles user interaction.
* `data_loader.py` (Hypothetical): Contains functions for fetching and cleaning the raw data.
* `requirements.txt`: Lists all necessary Python dependencies.
* `data/`: Directory where the raw CSV data files should be placed.