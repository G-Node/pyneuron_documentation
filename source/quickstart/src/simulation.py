import matplotlib.pyplot as plt
import os
import numpy as np
import sqlite3 as sqlite

import pydesignlib as pdl
import sqllib as sl

cell = pdl.MSO_Neuron()
sim = pdl.Simulation(cell)
sim.set_IClamp()
db_name = "simulation_results.sqlite"

# If you want to check, use
# >>> from neuron import gui
# and watch the morphology while playing around, e.g.:
# >>> cell.change_length(50)
# >>> cell.change_diameter(10)

if os.path.isfile(db_name):
  os.remove(db_name)

# connect to database
# ==========================
cxn = sqlite.connect(db_name)
cursor = cxn.cursor()
query = """
  CREATE TABLE results(
    length INTEGER,
    diameter REAL,
    Ra INTEGER,
    Rin REAL,
    tau_eff REAL,
    PRIMARY KEY (length, diameter, Ra)
    )
    """
cursor.execute(query)

# run simulation across sets of parameters
# ========================================
Ras = [1, 200]
diameters = np.arange(0.5,3.5,0.5)
lengths = range(10,210,10)
for Ra in Ras:
  cell.set_passive_parameters(gp=0.004, E=-60, rho=Ra)
  for diameter in diameters:
    cell.change_diameter(diameter)
    for length in lengths:
      cell.change_length(length)
      sim.go()
      Rin = sim.get_Rin()
      tau_eff = sim.get_tau_eff()
      # write result to the database
      query = """
      INSERT INTO results(
        length, diameter, Ra, Rin, tau_eff)
        VALUES (?,?,?,?,?)
      """
      print("Ra: %s, diameter: %s, length: %s ----> R_in: %s, tau_eff: %s" %(
        Ra, diameter, length, Rin, tau_eff))
      cursor.execute(
        query,
        (length, diameter, Ra, Rin, tau_eff)
        )
cxn.commit()


# analyse the data
# ================
sl.create_aggregate_functions(cxn)

# If you want to play with SQL you can download a nice firefox add on called
# 'SQLite Manager'. Connect to the database (which is the file
# 'simulation_results.sqlite') and play with SQL-statements (click on the left
# side on `Tables -> Results` and then on the register `execute SQL`). Then you
# can enter SQL statements. Use the examples from below to start with (e.g.:
# 'SELECT length, tau_eff FROM results')

t_query = ('SELECT length, tau_eff FROM results')
t_query1 = ('SELECT length, tau_eff FROM results WHERE Ra=1 AND diameter=1')
t_query2 = ('SELECT length, tau_eff FROM results WHERE Ra=200 AND diameter=1')
t_query3 = ('SELECT length, tau_eff FROM results WHERE Ra=200 AND diameter=3')
t_query_avg1 = (
  'SELECT length, avg(tau_eff) FROM results WHERE Ra=1 GROUP BY length')
t_query_avg2 = (
  'SELECT length, avg(tau_eff) FROM results WHERE Ra=200 GROUP BY length')

r_query = ('SELECT length, Rin FROM results')
r_query1 = ('SELECT length, Rin FROM results WHERE Ra=1 AND diameter=1')
r_query2 = ('SELECT length, Rin FROM results WHERE Ra=200 AND diameter=1')
r_query3 = ('SELECT length, Rin FROM results WHERE Ra=200 AND diameter=3')
r_query_avg1 = (
  'SELECT length, avg(Rin) FROM results WHERE Ra=1 GROUP BY length')
r_query_avg2 = (
  'SELECT length, avg(Rin) FROM results WHERE Ra=200 GROUP BY length')

query_avg_errorbar = (
  'SELECT length, %s, %s FROM results WHERE %s GROUP BY length')

# examples for plotting results for some queries:
sl.show_scatter_query(cursor, t_query)
sl.show_query_errorbar(cursor, query_avg_errorbar, y='avg(tau_eff)', err='SQLstd(tau_eff)', condition='Ra=1')
sl.show_query_errorbar(cursor, query_avg_errorbar, y='avg(tau_eff)', err='SQLstd(tau_eff)', condition='Ra=200')
