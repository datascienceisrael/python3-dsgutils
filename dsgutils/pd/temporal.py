import datetime
import numpy as np
import pandas as pd

def create_cyclic_time(ts, by = "s"):
    """Convert datetime (pd) to cyclic time representation using sine and cosine"""
    
    # constants
    HOURS_IN_DAY   = 24
    MINUTES_IN_DAY = HOURS_IN_DAY * 60
    SECONDS_IN_DAY = MINUTES_IN_DAY * 60

    # get hour, minute and second from datetime object
    if (type(ts) is pd.Timestamp):
        hour, minute, second = ts.hour, ts.minute, ts.second
        
    elif (type(ts) is pd.Series):
        hour, minute, second = ts.dt.hour, ts.dt.minute, ts.dt.second
    
    else:
        raise ValueError('`ts` argument must be pd.Timestamp or pd.Series of datetime')
        
        
    # convert to time passed after midnight 
    # (seconds, minutes or hours, determined according to the 'by' argument)
    if (by == 's'):
        x = hour * 60 * 60 + minute * 60 + second
        denom = SECONDS_IN_DAY
        
    elif (by == 'm'):
        x = hour * 60 + minute
        denom = MINUTES_IN_DAY
        
    elif (by == 'h'):
        x = hour
        denom = HOURS_IN_DAY
    
    else: # invalid 'by' argument
        raise ValueError("`by` argument expects 's', 'm' or 'h'")

    # convert to sine and cosine time
    sin_time = np.sin(2*np.pi*x/denom)
    cos_time = np.cos(2*np.pi*x/denom)
    
    return([sin_time, cos_time])
