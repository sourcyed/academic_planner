import argparse
import os
import subprocess
import logging

from fetch_events import fetch_all_events
from process_events import process_events
from database import init_db, insert_event
from config import DB_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def launch_dashboard():
    logging.info("Launching dashboard...")
    subprocess.run(["streamlit", "run", "dashboard.py"])

def run_pipeline():
    logging.info("Starting pipeline...")
    init_db()
    events = fetch_all_events()
    processed = process_events(events)
    for event in processed:
        insert_event(event)
    logging.info("Pipeline complete.")

def parse_args():
    parser = argparse.ArgumentParser(description="Run calendar pipeline.")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite the existing database")
    parser.add_argument("-s", "--show", action="store_true", help="Show the dashboard after running the pipeline")
    return parser.parse_args()

def main():
    args = parse_args()

    db_exists = os.path.exists(DB_NAME)

    if db_exists and not args.overwrite:
        logging.info("Database already exists and overwrite not specified. Skipping pipeline.")
        if args.show:
            launch_dashboard()
        else:
            logging.info("Exiting without running pipeline or dashboard.")
        return

    if args.overwrite and db_exists:
        os.remove(DB_NAME)
        logging.info("Existing database deleted.")

    # Early exit if DB exists and no overwrite flag
    if os.path.exists(DB_NAME) and not args.overwrite:
        logging.warning(f"Database '{DB_NAME}' already exists. Use -o or --overwrite to reset it.")
        return

    run_pipeline()

    if args.show:
        launch_dashboard()

if __name__ == "__main__":
    main()