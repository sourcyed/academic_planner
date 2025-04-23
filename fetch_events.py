import requests
import recurring_ical_events
from icalendar import Calendar
from datetime import datetime, timedelta, time
from time import sleep
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor
import logging
from urllib.parse import urlparse
from config import MOODLE_ICS_URL, GOOGLE_ICS_URL, LOCAL_TZ

RETRIES = 3
DELAY = 2

def fetch_calendar_data(ics_url):
    for attempt in range(RETRIES):
        try:
            response = requests.get(ics_url, timeout=10)
            response.raise_for_status()

            calendar = Calendar.from_ical(response.text)
            start = datetime.now()
            end = start + timedelta(days=30)

            events = recurring_ical_events.of(calendar).between(start, end)
            results = []

            for event in events:
                summary = str(event.get('summary'))
                start_dt = event.decoded('dtstart')
                end_dt = event.decoded('dtend')

                # Handle time zones
                if isinstance(start_dt, datetime):
                    if start_dt.tzinfo is None:
                        start_dt = start_dt.replace(tzinfo=ZoneInfo("UTC"))
                    start_dt = start_dt.astimezone(LOCAL_TZ)
                else:
                    # All-day event — treat as local midnight without converting from UTC
                    start_dt = datetime.combine(start_dt, time.min).replace(tzinfo=LOCAL_TZ)

                if isinstance(end_dt, datetime):
                    if end_dt.tzinfo is None:
                        end_dt = end_dt.replace(tzinfo=ZoneInfo("UTC"))
                    end_dt = end_dt.astimezone(LOCAL_TZ)
                else:
                    end_dt = datetime.combine(end_dt, time.min).replace(tzinfo=LOCAL_TZ)

                if summary and start_dt and end_dt:
                    results.append({
                        "summary": summary,
                        "start": start_dt.strftime("%Y-%m-%d %H:%M"),
                        "end": end_dt.strftime("%Y-%m-%d %H:%M"),
                    })
            logging.info(f"Calendar info fetched from {urlparse(ics_url).netloc}")
            return results
        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed for {urlparse(ics_url).netloc}")
            sleep(DELAY)
    logging.error(f"Failed to fetch after {RETRIES} attempts: {urlparse(ics_url).netloc}")
    return []


def fetch_all_events():
    with ThreadPoolExecutor() as executor:
        moodle_future = executor.submit(fetch_calendar_data, MOODLE_ICS_URL)
        google_future = executor.submit(fetch_calendar_data, GOOGLE_ICS_URL)
        return moodle_future.result() + google_future.result()