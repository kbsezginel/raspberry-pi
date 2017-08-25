from pghbustime import *
import datetime
import math


mykey = "LMJrK9vutafSVnViFmFvjaXvY"
api = BustimeAPI(mykey)

# Summerlea, Bellefonte, Graham
stops = [8245, 3144, 8192, 2566]
stop_names = ['Summerlea', 'Bellefonte', 'Graham', 'Thackeray']


def get_bus_schedule(stops, stop_names):
    """ Gets bus predictions for given stops """
    now = datetime.datetime.now()
    predictions = {}
    for i, stop in enumerate(stops):
        # print('--------------------------')
        try:
            predictions[stop_names[i]] = dict(bus=[], time=[], min=[])
            p = api.predictions(stpid=stop)
            if len(p['prd']) > 0:
                for prd in p['prd']:
                    # print(prd['stpnm'])
                    bus_name = prd['rt']
                    date = prd['prdtm'].split()[0]
                    year = int(date[:4])
                    month = int(date[4:6])
                    day = int(date[6:8])

                    taym = prd['prdtm'].split()[1].split(':')
                    hr, mn, sc = [int(tm) for tm in taym]

                    t_bus = datetime.datetime(year, month, day, hr, mn, sc)
                    t_delta = t_bus - now
                    min_left = math.ceil(t_delta.total_seconds() / 60)
                    # print('%s arriving in %i minutes at %i:%i' % (bus_name, min_left, hr, mn))
                    predictions[stop_names[i]]['bus'].append(bus_name)
                    predictions[stop_names[i]]['time'].append('%i:%i' % (hr, mn))
                    predictions[stop_names[i]]['min'].append(min_left)
        except:
            predictions[stop_names[i]] = None
            # print('No arrival for: %s' % stop_names[i])
    return predictions