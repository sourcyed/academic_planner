from datetime import datetime
import re
import logging

def assign_priority(event):
    days_left = event['days_left']
    if days_left <= 1:
        return "High"
    elif days_left <= 3:
        return "Medium"
    else:
        return "Low"


def tag_category(summary):
    summary = summary.lower()
    if re.search(r'\bexam|test|quiz\b', summary):
        return "Assessment"
    elif re.search(r'\btravel|flight|stay|hotel|festival|train\b', summary):
        return "Travel"
    elif re.search(r'\bmeeting|appointment|lesson\b', summary):
        return "Meeting"
    elif re.search(r'\bproject|assignment|homework|return|submit|deadline|due|moodle|loppukoe|koe|palautettava|completed\b', summary):
        return "Project"
    else:
        return "Other"


def clean_data(event):
    try:
        local_dt = datetime.strptime(event['start'], "%Y-%m-%d %H:%M")

        now = datetime.now()
        if local_dt < now:
            return None  # Skip events that have already started

        event['start'] = local_dt.strftime("%Y-%m-%d %H:%M")
        event['days_left'] = (local_dt.date() - now.date()).days
        event['priority'] = assign_priority(event)
        event['category'] = tag_category(event['summary'])
        event['date_only'] = local_dt.strftime("%Y-%m-%d")
        return event
    except Exception as e:
        logging.error(f"Error processing event: {e}")
        return None


def process_events(events):
    cleaned = [clean_data(e) for e in events]
    logging.info(f"Data cleaning and processing complete.")
    return [e for e in cleaned if e and e['days_left'] >= 0]