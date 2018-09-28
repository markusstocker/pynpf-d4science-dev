# -*- coding: utf-8 -*-
import requests, io, pandas as pd, urllib3
from datetime import datetime, timedelta
from pytz import timezone
import warnings, sys
warnings.filterwarnings('ignore')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

configuration = {
    'Hyytiaelae': {
        'smear_table': 'HYY_DMPS',
        'smear_variables': 'd316e1,d355e1,d398e1,d447e1,d501e1,d562e1,d631e1,d708e1,d794e1,'\
                           'd891e1,d100e2,d112e2,d126e2,d141e2,d158e2,d178e2,d200e2,d224e2,'\
                           'd251e2,d282e2,d316e2,d355e2,d398e2,d447e2,d501e2,d562e2,d631e2,'\
                           'd708e2,d794e2,d891e2,d100e3,d112e3,d126e3,d141e3,d158e3,d178e3,d200e3',
        'num_var_less_than_10nm': 10
    },
    'Puijo': {
        'smear_table': 'PUI_dmps_tot',
        'smear_variables': 'ch01,ch02,ch03,ch04,ch05,ch06,ch07,ch08,ch09,ch10,ch11,ch12,ch13,ch14,ch15,ch16,'\
                           'ch17,ch18,ch19,ch20,ch21,ch22,ch23,ch24,ch25,ch26,ch27,ch28,ch29,ch30,ch31,ch32,'\
                           'ch33,ch34,ch35,ch36,ch37,ch38,ch39,ch40',
        'num_var_less_than_10nm': 10
    },
    'Vaerrioe': {
        'smear_table': 'VAR_DMPS',
        'smear_variables': 'd316e1,d355e1,d398e1,d447e1,d501e1,d562e1,d631e1,d708e1,d794e1,'\
                           'd891e1,d100e2,d112e2,d126e2,d141e2,d158e2,d178e2,d200e2,d224e2,'\
                           'd251e2,d282e2,d316e2,d355e2,d398e2,d447e2,d501e2,d562e2,d631e2,'\
                           'd708e2,d794e2,d891e2,d100e3,d112e3,d126e3,d141e3,d158e3,d178e3,d200e3',
        'num_var_less_than_10nm': 10
    }
}

day = sys.argv[1]
place = sys.argv[2]

time_from = timezone('Europe/Helsinki').localize(datetime.strptime(day, '%Y-%m-%d'))
time_to = time_from + timedelta(days=1)

try:
    smear_table = configuration[place]['smear_table']
    smear_variables = configuration[place]['smear_variables']
except LookupError:
    print('Place not found in configuration [place = {}, places = {}]'.format(place, configuration.keys()))
    sys.exit()


http = urllib3.PoolManager()
r = http.request('GET', 
		 'http://avaa.tdata.fi/smear-services/smeardata.jsp', 
		 fields={'table': smear_table, 'quality': 'ANY', 'averaging': 'NONE', 'type': 'NONE',
         'from': str(time_from), 'to': str(time_to), 'variables': smear_variables})

data = pd.read_csv(io.StringIO(r.data.decode('utf-8')))

d = data.copy(deep=True)
d = d.ix[:, 6:].as_matrix()
m = len(d)
n = len(d[0])
x = range(0, m)
y = range(0, n)
x, y = np.meshgrid(x, y)
z = np.transpose(np.array([row[1:] for row in d]).astype(np.float))
plt.figure(figsize=(10, 5), dpi=100)
plt.pcolormesh(x, y, z)
plt.plot((0, x.max()), (y.max()/2, y.max()/2), "r-")
plt.colorbar()
plt.xlim(xmax=m-1)
x_ticks = np.arange(x.min(), x.max(), 6)
x_labels = range(x_ticks.size)
plt.xticks(x_ticks, x_labels)
plt.xlabel('Hours')
y_ticks = np.arange(y.min(), y.max(), 6)
y_labels = ['3.16', '6.31', '12.6', '25.1', '50.1', '100']
plt.yticks(y_ticks, y_labels)
plt.ylabel('Diameter [nm]')
plt.ylim(ymax=n-1)
plt.savefig('plot.png')


