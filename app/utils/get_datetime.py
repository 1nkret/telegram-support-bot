from datetime import datetime, timedelta


def get_datetime(date):
    return datetime.strftime(date, '%Y.%m.%d %H:%M')


def get_short_datetime(date):
    if isinstance(date, timedelta):
        return format_timedelta(date)
    return date.strftime("%Y.%m.%d %H:%M")


def format_timedelta(delta):
    minutes, seconds = divmod(int(delta.total_seconds()), 60)
    return f"{minutes} хвилин {seconds} секунд"
