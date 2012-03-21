import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import neuron


def make_compartment(length=150, diameter=3, nseg=1):
  """
  Returns a compartment.

    comp = make_compartment(120, 4) # comp.L: 120; comp.diam: 4; comp.nsg: 1
    comp = make_compartment()       # comp.L: 150; comp.diam: 3; comp.nsg: 1
  """
  compartment = neuron.h.Section()
  compartment.L = length
  compartment.diam = diameter
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
    self.gp = 0.004 # [S/cm^2]
    self.E = -60 # []
    self.Ra = 200
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
  >>> sim.go()
  >>> sim.show()
  """
  def __init__(self, cell, delay=1, amp=1, dur=3, sim_time=5, dt=0.001):
    self.cell = cell
    self.sim_time = sim_time
    self.dt = dt
    self.go_already = False

  def set_IClamp(self, delay=1, amp=-1, dur=3):
    """
    Initializes values for current clamp.
    
    Default values:
      
      delay = 1 [ms]
      amp   = -1 [nA]
      dur   = 3 [ms]
    """
    stim = neuron.h.IClamp(self.cell.soma(0.5))
    stim.delay = 1
    stim.amp = -1
    stim.dur = 3
    self.stim = stim

  def show(self):
    if self.go_already:
      x = np.array(self.rec_t)
      y = np.array(self.rec_v)
      plt.plot(x, y)
      plt.title("Hello World")
      plt.xlabel("Time [ms]")
      plt.ylabel("Voltage [mV]")
      plt.axis(ymin=-120, ymax=-50)
    else:
      print("""First you have to `go()` the simulation.""")
    plt.show()
    
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

  def go(self, sim_time=None):
    self.set_recording()
    neuron.h.dt = self.dt
    neuron.h.finitialize(self.cell.E)
    neuron.init()
    if sim_time:
      neuron.run(sim_time)
    else:
      neuron.run(self.sim_time)
    self.go_already = True

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
