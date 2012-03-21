import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sqlite
import part2lib as p2l
cell = p2l.MSO_Neuron()
sim = p2l.Simulation(cell)
sim.set_IClamp()
db_name = "ACCN_2009.sqlite"

# If you want to check, use
# >>> from neuron import gui
# and watch the morphology while playing around, e.g.:
# >>> cell.change_length(50)
# >>> cell.change_diameter(10)

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
Ras = [100]
diameters = np.arange(0.5,5.5,0.5)
lengths = range(10,410,10)
for Ra in Ras:
  cell.set_passive_parameters(gp=0.003, rho=Ra)
  for diameter in diameters:
    cell.change_diameter(diameter)
    for length in lengths:
      cell.change_length(length)
      sim.run()
      Rin = sim.get_Rin()
      tau_eff = sim.get_tau_eff()
      # write result to the database
      query = """
      INSERT INTO results(
        length, diameter, Ra, Rin, tau_eff)
        VALUES (?,?,?,?,?)
      """
      print("Ra: %s, diameter: %s, length: %s" %(Ra, diameter, length))
      cursor.execute(
        query,
        (length, diameter, Ra, Rin, tau_eff)
        )
cxn.commit()


# analyse the data
# ================
p2l.create_aggregate_functions(cxn)

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
"""
show_scatter_query(t_query)
show_query_errorbar(query_avg_errorbar, y='avg(tau_eff)', err='SQLstd(tau_eff)', condition='Ra=1')
show_query_errorbar(query_avg_errorbar, y='avg(tau_eff)', err='SQLstd(tau_eff)', condition='Ra=200')
"""

def show_scatter_query(query, title='Hello World', xlabel="x", ylabel='y',
                       alpha=0.1):
  cursor.execute(query)
  sql_result = cursor.fetchall()
  x, y = zip(*sql_result)
  plt.scatter(x, y, facecolor='black', edgecolor='black', alpha=alpha)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

def show_query_errorbar(query, y='avg(Rin)', err='SQLsem(Rin)',
                        condition='Ra=1'):
  cursor.execute(query %(y, err, condition))
  sql_result = cursor.fetchall()
  x, y, errorbar = zip(*sql_result)
  plt.scatter(x, y, facecolor='black', edgecolor='black', alpha=1)
  plt.errorbar(x, y, errorbar, fmt=None, ecolor='black')
