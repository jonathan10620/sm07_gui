from datetime import datetime, timedelta


def date_check(d1,d2):
    d1_obj, d2_obj = datetime.strptime(d1, '%m/%d/%Y'), datetime.strptime(d2, '%m/%d/%Y')   
    delta = d2_obj - d1_obj
    return delta.days + 1

def parse_date(str):
    return datetime.strptime(str, '%m/%d/%Y')


def calculate_recieved_date(date_obj):
    return date_obj + timedelta(days=1)
