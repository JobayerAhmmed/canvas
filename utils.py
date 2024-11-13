from datetime import datetime, timedelta


def find_column(ws, column_name):
    searched_col = None
    for col in range(1, ws.max_column + 1):
        header = ws.cell(row=1, column=col).value
        if header == column_name:
            searched_col = col
            break
    return searched_col


def convert_utc_to_iowa(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')

    # Define the time offset for Iowa (CST/CDT)
    # Central Standard Time (CST) is UTC-6
    # Central Daylight Time (CDT) is UTC-5
    # If you want to consider whether it's during CST or not, you can check the date:
    if utc_time.month in (3, 4, 5, 6, 7, 8, 9) or (utc_time.month == 10 and utc_time.day < 1):
        iowa_offset = timedelta(hours=-5)  # CDT
    else:
        iowa_offset = timedelta(hours=-6)  # CST

    iowa_time = utc_time + iowa_offset

    return iowa_time