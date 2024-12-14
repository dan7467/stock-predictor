from .models import CustomUser
from datetime import datetime, timezone, timedelta
from decimal import *
import pytz

getcontext().prec = 3  # decimal digits after the dot

# TO-DO 1: in the future, improve it to live notifications, without the need of switching pages
def check_updates(request, profile, yf_handler):
    # profile = CustomUser.objects.get(username=request.user.username)
    # suggestion: query yfinance for history since last website visit, and check if the price bound has been reached
    profile = CustomUser.objects.get(username=request.user.username)
    last_action_time = datetime.strptime(profile.last_action_datetime_utc, "%H:%M:%S, %d.%m.%y").replace(tzinfo=timezone.utc)
    last_action_date = last_action_time.date()
    subscribed_updates = profile.user_updates
    same_date_and_today = datetime.now(timezone.utc).date() == last_action_date
    res = []
    est = pytz.timezone('US/Eastern')  # yfinance is in EST time
    # TO-DO: test thoroughly this whole function and it's end cases
    for subscribed_update_stock_sym in subscribed_updates:
        directive_datetime = datetime.strptime(subscribed_updates[subscribed_update_stock_sym][0], "%H:%M:%S, %d.%m.%y").replace(tzinfo=timezone.utc)
        directive_dir = subscribed_updates[subscribed_update_stock_sym][1]
        directive_val = subscribed_updates[subscribed_update_stock_sym][2]
        if same_date_and_today:
            fetched_data = yf_handler.fetch_current_day_stock_info(subscribed_update_stock_sym)
        else:
            fetched_data = yf_handler.min_interval_fetch_data(subscribed_update_stock_sym, last_action_date)
        if directive_dir == 'up':
            for date, val in fetched_data['Close'][subscribed_update_stock_sym].items():
                parsed_date = datetime.strptime(str(date)[:str(date).index(':') + 6], "%Y-%m-%d %H:%M:%S")
                parsed_date_utc = est.localize(parsed_date, is_dst=None).astimezone(pytz.utc)
                if Decimal(val) >= Decimal(directive_val) and parsed_date_utc > directive_datetime:
                    res.append([datetime.strftime(parsed_date_utc, "%H:%M:%S, %d.%m.%y"), subscribed_update_stock_sym, directive_dir, directive_val])
        elif directive_dir == 'down':
            for date, val in fetched_data['Close'][subscribed_update_stock_sym].items():
                parsed_date = datetime.strptime(str(date)[:str(date).index(':') + 6], "%Y-%m-%d %H:%M:%S")
                parsed_date_utc = est.localize(parsed_date, is_dst=None).astimezone(pytz.utc)
                if Decimal(val) <= Decimal(directive_val) and parsed_date_utc > directive_datetime:
                        res.append([datetime.strftime(parsed_date_utc, "%H:%M:%S, %d.%m.%y"), subscribed_update_stock_sym, directive_dir, directive_val])
    return res

def add_user_notification(request, notification_message):
    # regular user notification, of length 2: [datetime_utc_str, notification_msg]
    profile = CustomUser.objects.get(username=request.user.username)
    profile.user_notifications.append([datetime.now().strftime("%H:%M, %d.%m.%y"), notification_message])
    profile.save()
    
def add_user_stock_notification(request, profile, update):  # update == ["%H:%M:%S, %d.%m.%y", subscribed_update, directive_dir, directive_val]
    # user stock subscription notification, of length 5: [datetime_utc_str, subscribed_update, directive_dir, directive_val, color(according to directive_dir)]
    if update[2] == 'up':
        profile.user_notifications.append([datetime.strptime(update[0], "%H:%M:%S, %d.%m.%y").strftime("%H:%M, %d.%m.%y"), update[1], update[2], update[3], '#4CCD99'])
    else:
        profile.user_notifications.append([datetime.strptime(update[0], "%H:%M:%S, %d.%m.%y").strftime("%H:%M, %d.%m.%y"), update[1], update[2], update[3], '#FF204E'])
    profile.save()
    # print(f'added notification: {[datetime.strptime(update[0], "%H:%M:%S, %d.%m.%y").strftime("%H:%M, %d.%m.%y"), update[1], update[2], update[3]]}')