import neuron
import matplotlib.pylab as plt
import part2lib as p2l # from the tutorial

cell = p2l.MSO_Neuron()
syn = neuron.h.Exp2Syn(cell.soma(0.5))
syn.e = -80
synputs = [2,5,10,17,20]
netconsyn = neuron.h.NetCon(None, syn, 0.5, 0, 0.2)

# Hey Neil, here comes the little tricky part:
# In order to 'activte' the netcon-events, you have to define a function, that
# is doing that, and you have to call this function with the
# FInitializeHandler (I hope, it works for you):
def set_ini():
  for synput in synputs:
    netconsyn.event(synput)

fini_syn = neuron.h.FInitializeHandler(set_ini)

sim = p2l.Simulation(cell)
sim.sim_time = 50

sim.run()
sim.show()

plt.show()
