import re
import pandas as pd
import unicodedata


def remove_junk_chars(text):
    if not isinstance(text, str):
        return ""
    return "".join(
        ch for ch in text
        if unicodedata.category(ch)[0] != "C"
    )


def preprocess(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%y, %H:%M - '
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages_clean = []

    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages_clean.append(entry[2])
        else:
            users.append('group_notification')
            messages_clean.append(entry[0])

    df['user'] = users
    df['message'] = messages_clean
    df.drop(columns=['user_message'], inplace=True)

    # remove junk control characters but keep emojis
    df['message'] = df['message'].apply(remove_junk_chars)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append('23-00')
        elif hour == 0:
            period.append('00-01')
        else:
            period.append(f'{hour}-{hour+1}')

    df['period'] = period

    return df
