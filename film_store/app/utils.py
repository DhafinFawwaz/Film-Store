import datetime

# seconds to hh:mm:ss
def duration_to_format(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    if hours < 10:
        hours = f'0{hours}'
    if minutes < 10:
        minutes = f'0{minutes}'
    if seconds < 10:
        seconds = f'0{seconds}'
    return f'{hours}:{minutes}:{seconds}'

def format_date_from_str(date_str: str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date.strftime('%d %b %Y %I:%M %p')

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)