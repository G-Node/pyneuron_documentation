"""
Tutorial about PyNEURON
=======================

(Given at Advanced Course of Computational Neuroscience, Freiburg 2009)

Library for part II
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sqlite
import neuron


def make_compartment(length, diameter, nseg=None):
  compartment = neuron.h.Section()
  compartment.L = length
  compartment.diam = diameter
  if nseg:
    compartment.nseg = nseg
  return compartment


class MSO_Neuron(object):
  """
  This class will produce MSO_Neuron objects with a standard soma (L=40 um,
  diam=20 um) with two identical dendrites connected on opposite sites of the
  soma. For the dendrites the following parameters can be changed:
  
  * d_length:   length of each dendrite
  * d_diameter: diameter of each dendrite

  To check the morphology with NEURON gui:
  >>> from neuron import gui
  """
  def __init__(self, d_length=150, d_diam=3):
    """
    This method will be executed when you run
    >>> mycell = MSO_Neuron()
    """
    # passive properties
    self.gp = 0.003 # [S/cm^2]
    self.E = -60 # []
    self.Ra = 100
    # creating compartments
    self.soma = make_compartment(40, 20)
    self.dendrites = {}
    sites = ['contra', 'ipsi']
    for site in sites:
      dendrite = make_compartment(d_length, d_diam)
      if site == 'contra':
        # connecting the contralateral dendrite to the soma
        dendrite.connect(self.soma,1,0)
      elif site == 'ipsi':
        # connecting the ipsilateral dendrite to the soma
        dendrite.connect(self.soma, 0,0)
      else:
        print("Here is something wrong...")
        print("site: %s" %(site))
      self.dendrites.update({site: dendrite})

    # initialize parameters
    self.set_passive_parameters(self.gp, self.E, self.Ra)

  def set_passive_parameters(self, gp=0.004, E=-60, rho=200):
    for sec in neuron.h.allsec():
      sec.Ra = rho
      sec.insert("pas")
      for seg in sec:
        seg.pas.g = gp
        seg.pas.e = E

  def change_diameter(self, diam):
    for dendrite in self.dendrites.itervalues():
      dendrite.diam = diam

  def change_length(self, length):
    for dendrite in self.dendrites.itervalues():
      dendrite.L = length
      
    
class Simulation(object):
  """
  Oblects of this class control a current clamp simulation. Example of use:
  >>> cell = Cell()
  >>> sim = Simulation(cell)
  >>> sim.run()
  >>> sim.show()
  """
  def __init__(self, cell, delay=1, amp=1, dur=3, sim_time=5, dt=0.001):
    self.cell = cell
    self.sim_time = sim_time
    self.dt = dt
    self.run_already = False

  def set_IClamp(self):
    stim = neuron.h.IClamp(self.cell.soma(0.5))
    stim.delay = 1
    stim.amp = -1
    stim.dur = 3
    self.stim = stim

  def show(self):
    if self.run_already:
      x = np.array(self.rec_t)
      y = np.array(self.rec_v)
      plt.plot(x, y)
      plt.title("Hello World")
      plt.xlabel("Time [ms]")
      plt.ylabel("Voltage [mV]")
      plt.axis(ymin=-120, ymax=-50)
    else:
      print("""First you have to `run()` the simulation.""")
    
  def set_recording(self):
    # Record Time
    self.rec_t = neuron.h.Vector()
    self.rec_t.record(neuron.h._ref_t)
    # Record Voltage
    self.rec_v = neuron.h.Vector()
    self.rec_v.record(self.cell.soma(0.5)._ref_v)

  def get_recording(self):
    time = np.array(self.rec_t)
    voltage = np.array(self.rec_v)
    return time, voltage

  def run(self, sim_time=None):
    self.set_recording()
    neuron.h.dt = self.dt
    neuron.h.finitialize(self.cell.E)
    neuron.init()
    if sim_time:
      neuron.run(sim_time)
    else:
      neuron.run(self.sim_time)
    self.run_already = True

  def get_tau_eff(self, ip_flag=False, ip_resol=0.01):
    time, voltage = self.get_recording()
    vsa = np.abs(voltage-voltage[0]) #vsa: voltage shifted and absolut
    v_max = np.max(vsa)
    exp_val = (1-1/np.exp(1)) * v_max # 0.6321 * v_max
    ix_tau = np.where(vsa > ( exp_val ))[0][0] 
    tau = time[ix_tau] - self.stim.delay 
    return tau
  
  def get_Rin(self):
    """
    This function returnes the input resistance.
    """
    _, voltage = self.get_recording()
    volt_diff = max(voltage) - min(voltage)
    Rin = np.abs(float(volt_diff / self.stim.amp))
    return Rin


class SQLaggregate(object):
  """
  This class serves as the parent class of self written aggregate functions.
  The subclasses have to define the `finalize` function.

  **Important**: each aggregate function has to be listed in
  Operator.create_aggregate_functions()
  """
  def __init__(self):
    import numpy as np
    self.values = []
  def step(self, value):
    self.values.append(value)


class SQLstd(SQLaggregate):
  def finalize(self):
    return np.array(self.values).std()


class SQLsem(SQLaggregate):
  def finalize(self):
    values = np.array(self.values)
    return values.std()/np.sqrt(len(values))


def init_database(cursor):
  """
  creates a SQLite database with the following tables:
  - Results
  """
  print('Creating table "Results"')
  query = """
    CREATE TABLE Results(
      length INTEGER,
      diameter REAL,
      Ra INTEGER,
      Rin REAL,
      tau_eff REAL,
      PRIMARY KEY (length, diameter, Ra)
      )
  """
  cursor.execute(query)

def create_aggregate_functions(cxn):
  cxn.create_aggregate("SQLstd", 1, SQLstd)
  cxn.create_aggregate("SQLsem", 1, SQLsem)

def xyz2surf(x_in, y_in, z_in):
  x = np.unique(x_in)
  y = np.unique(y_in)
  lx = len(x)
  ly = len(y)
  matrix = np.zeros((ly, lx))
  for idx in range(len(z_in)):
    matrix[y==y_in[idx], x==x_in[idx]] = z_in[idx]
  return x, y, matrix
