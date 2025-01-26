import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Slider, Div, CustomJS
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap
from bokeh.palettes import all_palettes
import numpy as np
from scipy.integrate import odeint
 
def deriv(y, t, N, beta, gamma):
    tmp_S, tmp_I, tmp_R = y
    dSdt = -beta * tmp_S * tmp_I / N
    dIdt = beta * tmp_S * tmp_I / N - gamma * tmp_I
    dRdt = gamma * tmp_I
    return dSdt, dIdt, dRdt

time = np.linspace(0, 100, 100)

N = 100
I0 = 10 
R0 = 2 
S0 = N - I0 - R0 
beta = 0.2 
gamma = 0.1 

y0 = S0, I0, R0
S, I, R = odeint(deriv, y0, time, args=(N, beta, gamma)).T

fig = figure(
    width=1000,
    height=500,
    x_axis_label='t [dni]',
    y_axis_label='SIR population')

splot = fig.line(time, S, legend_label='S(t)', line_width=5, color='blue')
iplot = fig.line(time, I, legend_label='I(t)', line_width=5, color='red')
rplot = fig.line(time, R, legend_label='R(t)', line_width=5, color='green')

fig.grid.grid_line_dash = [6, 4]
fig.toolbar.logo = None
fig.toolbar.autohide = True
fig.xaxis.axis_label_text_font_size = "15pt"
fig.yaxis.axis_label_text_font_size = "15pt"
fig.xaxis.major_label_text_font_size = "14pt"
fig.yaxis.major_label_text_font_size = "14pt"
fig.legend.label_text_font_size = "15pt"

s1 = Slider(title='$$\\beta$$', value=beta, start=0.0, end=1.0, step=0.05, width = 500)
s2 = Slider(title='$$\\gamma$$', value=gamma, start=0.0, end=1.0, step=0.05, width = 500)

def update(attr, old, new):
    beta = s1.value
    gamma = s2.value

    S, I, R = odeint(deriv, y0, time, args=(N, beta, gamma)).T

    splot.data_source.data['y'] = S
    iplot.data_source.data['y'] = I
    rplot.data_source.data['y'] = R

s1.on_change('value_throttled', update)
s2.on_change('value_throttled', update)

curdoc().add_root(column(fig, row(s1, s2)))