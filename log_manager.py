import csv
import os
from datetime import datetime

LOG_FILE = 'upload_logs.csv'

def log_upload(user, file_name, owner, property_type, doc_type):
    # Check if file exists
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['User', 'File', 'Owner', 'Property', 'Document', 'Date'])

        writer.writerow([user, file_name, owner, property_type, doc_type, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])


def get_all_logs():
    logs = []
    if not os.path.exists(LOG_FILE):
        return logs

    with open(LOG_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            logs.append({
                'user': row['User'],
                'file': row['File'],
                'owner': row['Owner'],
                'property': row['Property'],
                'doc': row['Document'],
                'date': row['Date']
            })

    return logs
