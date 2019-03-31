from datetime import datetime, timedelta
import pytz

def get_week(week):
    if not isinstance(week, datetime):
        try:
            week = datetime.strptime(week, '%Y-%m-%d')
        except:
            week = datetime.now()
    return week


def normalize_week_begin(d):
    assert(isinstance(d, datetime))
    d = d.astimezone(pytz.timezone('Africa/Lagos'))
    return d - timedelta(days=d.weekday())