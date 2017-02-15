from django.utils.dateparse import parse_date, parse_datetime


def parse_date_as_datetime(date):
    datetime_split = date.split('.')
    datetime = datetime_split[2] + '-' + datetime_split[1] + '-' + datetime_split[0] + '00:00:00'
    return datetime

