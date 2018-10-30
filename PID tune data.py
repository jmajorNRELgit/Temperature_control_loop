# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 13:45:39 2018

@author: jmajor
"""

import matplotlib.pyplot as plt


for i in range(0,63,3):
    plt.plot(master_temp[i], label = master_temp[i+2])

plt.legend()
plt.show()


#import plotly.plotly as py
import plotly.graph_objs as go


from plotly.offline import plot


trace = []

for i in range(0,60,3):
    trace.append(go.Scatter(
            y = master_temp[i],
            name = "p: {0}, i: {1}".format(master_temp[i+1],master_temp[i+2])))

data = trace


layout = go.Layout(
        title = 'PID Tuning',
    yaxis=dict(
        autorange=True,
        title = 'Temp' ),
    xaxis = dict(
            autorange=True,
            title = 'Time'))

fig = go.Figure(data=data, layout=layout)
plot(fig, filename = r'C:\Users\jmajor\Desktop\github\Second tuning trial.html')# , filename = r'C:\Users\jmajor\Desktop\DuPont_Substrate Comparison_integral.html'