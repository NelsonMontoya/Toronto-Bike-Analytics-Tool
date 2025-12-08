

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
* pandas
* numpy
* streamlit
* pytest
* plotly

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

The data can be found at https://cascade.myunfc.ca/d2l/common/viewFile.d2lfile/Database/OTQ2MDMw/Bike%20share%20ridership%202024-08.csv?ou=18038


## 📊 Data Source

This tool utilizes publicly available data from the **Toronto Bike Share** system, typically sourced from their Open Data portal 
or similar providers. Data files are expected to be in a directory (e.g., `./data/`) and formatted as CSV.

## Key Features

- Data Pipeline: Loads, cleans, and processes the Toronto Bike-Sharing dataset using functions in `src/data_processor`.


- Core Analytics: Generates meaningful insights into station usage, trip duration patterns, and peak times via the `src/analytics` module.


- Modular Codebase: Provides reusable Python functions returning data or plot objects.



- Interactive Dashboard: A lightweight interactive dashboard built using Streamlit to display key summaries and charts.



- Agile Discipline: Demonstrates Test-Driven Development (TDD) and intentional refactoring, supported by a comprehensive tests module.

## 📂 Project Structure

* `dashboard.py`: The main Streamlit script that defines the layout and handles user interaction.
* `requirements.txt`: Lists all necessary Python dependencies. Stores the raw input data bike_share_data.csv
* `data/`: Directory where the raw CSV data files should be placed.
* `src/`: Contains all the production Python source code (reusable functions and modules).
* `tests/`: Contains automated unit tests for TDD stories.
* `src/data_processor`: Responsible for the data Load, Clean, and Process steps. 
* - loading_cleaning.py: Handles data ingestion and initial cleaning. 
* - feature_engineering.py: Creates new features required for analysis. 
* - rider_categorization.py: Implements logic for categorizing riders (e.g., membership type).
* `src/analytics`: Responsible for generating reusable data and plot objects. 
* - stations.py, plot_top_stations.py: Focuses on station usage analytics. 
* - usage_patterns.py: Calculates trip duration and peak time patterns.


### Running the App

The project includes automated tests for all core functionality, implementing Test-Driven Development (TDD) for at least five (5) user stories.
To run all automated tests implemented using the pytest framework:

```bash
pytest
 ```

### Deployed App

The app was also deployed to streamlite.  You can see it using this link 
https://toronto-bike-analytics-tool-kuh8hahoazghymgbrxnf5a.streamlit.app