"""
An dieser Stelle sollten keine Daten erzeugt werden!

Plotting Remarks
================

How should single plots be combined to a figure. One solution is to save each
plot as pdf and put the plots together with inkscape.

Questions to answere::

- which font to use (e.g.: bitstream vera?)
  - Christian: Helvetica
- which program supports a good plotting interface
  - Christian: xmgrace

"""
import os
import numpy as np
import simlib as sl

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


import time
import sqlite3 as sqlite
import datahandlinglib as dhl

# os
home = dhl.get_home_path()
project = os.path.join(home, 'Manuskript/')

mpl.rc('lines', color='black')

def make_figure_1():
  """
  Figure 1:
  """
  from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
  from matplotlib.figure import Figure
  import matplotlib.artist as artist
  fig = plt.figure()
  fig.text(0.5, 0.01, 'Figure 1', ha='center', color='black', weight='bold',
    size='large')
  fig.text(0.05, 0.94, 'A', ha='center', color='black', size='large')
  fig.text(0.55, 0.94, 'B', ha='center', color='black', size='large')

  canvas = FigureCanvas(fig)
  # other things to do:
  # >>> fig.patch.set_facecolor('white')
  # >>> help fig.patch
  # >>> fig.patch.set_alpha(0.5)
  # >>> artist.getp(fig)
  # >>> plt.draw() # uses: fig.canvas.draw()

  # Fig. 1A
  # =======

  # axes 0: Scatch of patch clamp simulation
  # ----------------------------------------
  ax = fig.add_subplot(221)
  im_file = os.path.join(project, 'Figure1/Graph1.png')
  img = mpimg.imread(im_file)
  ax.imshow(img)
  ax.axis('off')

  """
  ax1.set_xticklabels([])
  ax.set_xticks([])
  ax.set_yticks([])
  ax1.set_yticklabels([])
  """
  
  # Fig. 1B
  # =======

  import msolib as ml
  cell = ml.MSO_Neuron(sy_gmax = 0)
  sim = ml.Simulation(cell, sim_time=4)
  sim.set_IClamp(delay=0.5)
  sim.go()
  rec = sim.get_recording()
  vmax = max(rec['voltage'])
  vmin = min(rec['voltage'])
  t_vmax = sim.stim.delay + sim.stim.dur
  tau, pnts = sim.get_tau_eff()
  xs = [pnts['x0'], pnts['x1']]
  ys = [pnts['y0'], pnts['y1']]

  # axes 1: Voltage trace
  # ---------------------
  
  # subplot 422
  ax = plt.subplot(422)
  ax.plot(rec['time'], rec['voltage'], color='black')
  artist.setp(ax.get_xticklabels(), visible=False)
  #ax.set_xticklabels([])
  ax.axis('off')
  # draw tau-triangle
  style={'linestyle': ':', 'color': 'black'}
  ax.plot(xs, [ys[1], ys[1]], **style)
  ax.plot([xs[0], xs[0]], ys, **style)
  # - add text
  ax.text(xs[0], sum(ys)/2, r"$\rm dV^{(1-\frac{1}{e})}$",
    rotation=90,
    horizontalalignment='right',
    verticalalignment='center',
    size='small')
  ax.text(sum(xs)/2, ys[1]-0.1, r"$\tau_{\rm eff}$",
    horizontalalignment='center',
    verticalalignment='top',
    size='small')
  # draw dV and asymptote
  ax.plot([t_vmax, t_vmax], [vmax, vmin], **style)
  ax.text(t_vmax, (vmax+vmin)/2, r"$\rm dV$",
    rotation=90,
    horizontalalignment='right',
    verticalalignment='center',
    size='small')
  style['linestyle'] = '--'
  ax.axhline(y=min(rec['voltage']), **style)
  ax.axhline(y=max(rec['voltage']), **style)

  # axes 2: Current trace
  ax = plt.subplot(424, sharex=fig.axes[-1])
  ax.plot(rec['time'], rec['current'])
  ax.axis('off')
  ax.axis(ymin=-1.5, ymax=0.5)
  # add text "dI"
  ax.text(xs[0], -0.5, r"$\rm dI$",
    rotation=90,
    horizontalalignment='right',
    verticalalignment='center',
    size='small')
  
  plt.draw()
  return fig
