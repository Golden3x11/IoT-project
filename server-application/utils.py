import time
import datetime
from config import PRICE_MULTIPLIER
 
# input - czas wejscia, wyjscia
# return - czas przejazdu (w minutach) razy taryfikator (PRICE_MYLTIPLIER)
def count_price_and_duration(time_in, time_out):
    time_in_con = time.strptime(time_in, "%c")
    time_out_con = time.strptime(time_out, "%c")
    time_in_sec = datetime.timedelta(days=time_in_con.tm_mday, hours=time_in_con.tm_hour,
                                     minutes=time_in_con.tm_min, seconds=time_in_con.tm_sec).total_seconds()
    time_out_sec = datetime.timedelta(days=time_out_con.tm_mday, hours=time_out_con.tm_hour,
                                      minutes=time_out_con.tm_min, seconds=time_out_con.tm_sec).total_seconds()

    time_diff = time_out_sec - time_in_sec
    return round(time_diff / 60 * PRICE_MULTIPLIER, 2), time_diff

def value_or_question_mark(value):
    return value if value is not None else '?'