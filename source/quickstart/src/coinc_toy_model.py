import numpy as np
import sqlalchemy as sa
import sqlalchemy.orm as orm
import msolib as ml

# SETTING THE DATABASE
# ====================

# creating/connecting a sqlite database for storing the data
engine = sa.create_engine('sqlite:///coinc_toy_model.sqlite', echo=False)
#engine = sa.create_engine('sqlite:///:memory:')
Session = orm.sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

metadata = sa.MetaData()

# Create Table
results_table = sa.Table('results', metadata,
  sa.Column('gmax_ipsi', sa.Float, primary_key=True),
  sa.Column('gmax_contra', sa.Float, primary_key=True),
  sa.Column('gp', sa.Float, primary_key=True),
  sa.Column('Ra', sa.Float, primary_key=True),
  sa.Column('length', sa.Float, primary_key=True),
  sa.Column('diam', sa.Float, primary_key=True),
  sa.Column('maximum', sa.Float, nullable=False)
)
metadata.create_all(engine)

# Create Object
class Result(object):
  def __init__(self, gmax_ipsi, gmax_contra, gp, Ra, length, diam, maximum):
    self.gmax_ipsi = gmax_ipsi
    self.gmax_contra = gmax_contra
    self.gp = gp
    self.Ra = Ra
    self.length = length
    self.diam = diam
    self.maximum = maximum
  def __repr__(self):
    return "<Result ('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
      self.gmax_ipsi,
      self.gmax_contra,
      self.gp,
      self.Ra,
      self.length,
      self.diam,
      self.maximum)

# Map object to table
orm.mapper(Result, results_table)

# RUNNING THE SIMULATION
# ======================

default_setup = {'gp': 0.003, 'Ra': 100, 'd_length': 130, 'd_diam': 3.5,
 'jitter': False}


def sim_iso_max(cell, lb, ub, step):
  """
  lb: lower bound (avoid ``min`` as this refers to the function ``min()``)
  up: upper bound (avoid ``max`` as this refers to the function ``max()``)
  >>> sim_iso_max(cell, 0, 0.01, 0.0005)
  """
  gmaxs = np.arange(lb, ub, step)
  for idx, gmax_ipsi in enumerate(gmaxs):
    print "countdown: ", len(gmaxs) - idx
    cell.set_syns_attr('ipsi', 'gmax', gmax_ipsi)
    for gmax_contra in gmaxs:
      cell.set_syns_attr('contra', 'gmax', gmax_contra)
      sim.go()
      erg = max(sim.get_recording()['voltage'])
      erg_tup = (gmax_ipsi, gmax_contra, cell.gp, cell.Ra, cell.d_length,
        cell.d_diam, erg)
      print erg_tup
      result = Result(*erg_tup)
      session.add(result)
  session.commit()

if __name__ == '__main__':
  cell = ml.MSO_Neuron(**default_setup)
  sim = ml.Simulation(cell)
  sim_iso_max(cell, 0, 0.01, 0.0005)

