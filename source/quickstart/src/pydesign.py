import matplotlib.pyplot as plt
import sqlite3 as sqlite
import pydesignlib as pdl
cell = pdl.MSO_Neuron()
sim = pdl.Simulation(cell)
sim.set_IClamp()
sim.go()
sim.show()
