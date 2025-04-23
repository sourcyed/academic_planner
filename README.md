# Academic Calendar Pipeline

This project is a modular data pipeline that integrates and processes calendar events from multiple sources (such as Moodle and Google Calendar via `.ics` links). It transforms the data into a structured format, stores it in a local SQLite database, and provides a visual dashboard using Streamlit for exploring upcoming events and analyzing workload over time.

## Features

- Fetches calendar events from multiple `.ics` sources
- Supports recurring events and timezone normalization
- Processes events to assign categories and priority levels
- Filters out past and incomplete events
- Stores processed data in a local SQLite database
- Displays interactive visualizations and tables using Streamlit
- Command-line options for overwriting the database and displaying the dashboard

## Project Structure

```
academic_calendar_pipeline/
├── fetch_events.py         # Event fetching and .ics parsing logic
├── process_events.py       # Data cleaning, enrichment, and transformation
├── database.py             # Database schema and access functions
├── dashboard.py            # Streamlit interface for visualization
├── main.py                 # Pipeline orchestrator with command-line options
├── config.py               # Configuration variables (URLs, DB name, etc.)
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation

Ensure you are using Python 3.8 or newer. Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the pipeline with the following options:

```bash
python main.py [--overwrite | -o] [--show | -s]
```

### Options

- `--overwrite` / `-o`: Deletes the existing database and initializes a new one.
- `--show` / `-s`: Launches the Streamlit dashboard after pipeline execution.

You can also run the dashboard independently:

```bash
streamlit run dashboard.py
```

## Dashboard Overview

The dashboard displays:

- **Upcoming Events Table**: Sorted list of events, filterable by category.
- **Busy Level Chart**: Number of events scheduled per day.
- **Category Distribution**: Bar chart showing count of events by category.

## Configuration

Update the `.ics` calendar source URLs and database name in `config.py`.

```python
# config.py
from zoneinfo import ZoneInfo
MOODLE_ICS_URL = "https://example.com/moodle.ics"
GOOGLE_ICS_URL = "https://example.com/google.ics"
DB_NAME = "events.db"
LOCAL_TZ = ZoneInfo("Europe/Helsinki")
```

## Why This Project?

Managing academic tasks and personal events from multiple sources can be cumbersome. This pipeline consolidates data into a structured and queryable format, offering real-time insights into your schedule and workload. It supports better time management, planning, and academic performance.

## Future Enhancements

- Integration with additional calendar providers
- Notification system for high-priority or imminent events
- Advanced natural language processing for event tagging
- Historical trend analysis for workload prediction

## License

This project is intended for personal and academic use. Contributions are welcome via pull requests or issue reports.
