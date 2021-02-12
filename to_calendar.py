import datetime

def convert_date(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s + '2021', 'W%W-%a%Y')

def event_to_csv(date_str, event: dict) -> str:
    date = convert_date(date_str)
    date_str = date.strftime('%d/%m/%Y')
    start_time = date + datetime.timedelta(hours=event['start'])
    end_time = date + datetime.timedelta(hours=event['end'])
    data = {
        'Subject': event['classcode'],
        'Start Date': date_str,
        'Start Time': start_time.strftime('%I:%M %p'),
        'End Date': date_str,
        'End Time': end_time.strftime('%I:%M %p'),
        'All Day Event': 'False',
        'Description': event['classname'],
        'Location': event['classroom'],
        'Private': 'False'
    }

    return ','.join(data[k] for k in data)

def convert_and_save(courses, path='./calendar.csv'):
    csv = 'Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private\n'
    for course in courses:
        for date_str, events in course.items():
            for event in events:
                csv += event_to_csv(date_str, event) + '\n'

    with open(path, 'w') as f:
        f.write(csv)
