import pandas as pd
import datetime

def compute_labeling_speed(filename, TH_TIMEOUT_SESSION):
    df = pd.read_csv(filename, parse_dates=['created_date_time', 'updated_date_time'])
    df = df.sort_values(['user_id', 'created_date_time'])
    users_sessions = pd.DataFrame()
    users_speed = {}
    for user_id in df['user_id'].unique():
        d = df[ df['user_id']==user_id]
        d['session'] = d['created_date_time'] - d['created_date_time'].shift()
        d['session'] = (d['session'] > datetime.timedelta(minutes=TH_TIMEOUT_SESSION)).cumsum()
        single_user_sessions = d.groupby('session')['created_date_time'].agg([('count', lambda x: len(x) - 1),
                                                                 ('start_datetime', lambda x: x.iloc[0]),
                                                                 ('end_datetime', lambda x: x.iloc[-1]),
                                                                 ('timediff', lambda x: x.iloc[-1] - x.iloc[0])
                                                       ])
        single_user_sessions['user_id'] = user_id
        users_speed[user_id] = sum(single_user_sessions['timediff'].dt.seconds) / sum(single_user_sessions['count'])
        users_sessions = pd.concat([users_sessions, single_user_sessions])

    return users_speed, users_sessions



filename = r'C:\Users\Omri Allouche\server_documentannotation_201902172119.csv'
TH_TIMEOUT_SESSION = 5
print( compute_labeling_speed(filename, TH_TIMEOUT_SESSION) )