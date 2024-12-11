from .models import CustomUser
from datetime import datetime, timezone, timedelta
from decimal import *
import pytz

getcontext().prec = 3  # decimal digits after the dot

# TO-DO 1.1: make every user page entrance call check_updates method
# TO-DO 1.2: in the future, improve it to live notifications, without the need of switching pages
# @login_required
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
    for subscribed_update in subscribed_updates:
        directive_datetime = datetime.strptime(subscribed_updates[subscribed_update][0], "%H:%M:%S, %d.%m.%y").replace(tzinfo=timezone.utc)
        directive_dir = subscribed_updates[subscribed_update][1]
        directive_val = subscribed_updates[subscribed_update][2]
        if same_date_and_today:
            fetched_data = yf_handler.fetch_current_day_stock_info(subscribed_update)
            if directive_dir == 'up':
                for date, val in fetched_data['Close'][subscribed_update].items():  # TO-DO: verify that this is also the live price (when market is open)
                    # e.g. date = 2024-12-11 18:25:00+00:00, val = 249.1645965576172
                    parsed_date = datetime.strptime(str(date)[:str(date).index(':') + 6], "%Y-%m-%d %H:%M:%S")
                    parsed_date_utc = est.localize(parsed_date, is_dst=None).astimezone(pytz.utc)
                    # print(f'Decimal({val}) >= Decimal(directive_val(={directive_val})): {Decimal(val) >= Decimal(directive_val)}. {parsed_date_utc} > {directive_datetime}: {parsed_date_utc > directive_datetime}')
                    if Decimal(val) >= Decimal(directive_val) and parsed_date_utc > directive_datetime:
                        res.append([datetime.strftime(parsed_date_utc, "%H:%M:%S, %d.%m.%y"), subscribed_update, directive_dir, directive_val])
            elif directive_dir == 'down':
                for date, val in fetched_data['Close'][subscribed_update].items():  # TO-DO: verify that this is also the live price (when market is open)
                    parsed_date = datetime.strptime(str(date)[:str(date).index(':') + 6], "%Y-%m-%d %H:%M:%S")
                    parsed_date_utc = est.localize(parsed_date, is_dst=None).astimezone(pytz.utc)
                    # print(f'Decimal({val}) <= Decimal(directive_val(={directive_val})): {Decimal(val) <= Decimal(directive_val)}. {parsed_date_utc} > {directive_datetime}: {parsed_date_utc > directive_datetime}')
                    if Decimal(val) <= Decimal(directive_val) and parsed_date_utc > directive_datetime:
                        res.append([datetime.strftime(parsed_date_utc, "%H:%M:%S, %d.%m.%y"), subscribed_update, directive_dir, directive_val])
            else:  # means this is a bad subscription: direction not in ['up', 'down'], as it should be
                continue
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
    print(f'added notification: {[datetime.strptime(update[0], "%H:%M:%S, %d.%m.%y").strftime("%H:%M, %d.%m.%y"), update[1], update[2], update[3]]}')