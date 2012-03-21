import sqlite3 as sqlite
from numpy.random import rand

db_name = "example.sqlite"

# connect to database
# ==========================
cxn = sqlite.connect(db_name)
cursor = cxn.cursor()

# Create table "cells"
query = """
  CREATE TABLE cells(
    cellname VARCHAR(64) PRIMARY KEY,
    age INTEGER,
    surface_area INTEGER
    )
    """
cursor.execute(query)
cxn.commit()


# Fill table "cells" with random data
names = ['neuron1', 'neuron2', 'pippi', 'berta', 'neuron5']
ages = [10, 15]

for name in names:
  age = ages[int(round(rand(1)))]
  surface_area = int(age * 800 + rand(1)*1000)
  query = """
    INSERT INTO cells(cellname, age, surface_area)
    VALUES (?,?,?)
  """
  cursor.execute(query, (name, age, surface_area)) # write to db-buffer
cxn.commit() # write to database

# Analyse Data
# ------------

# Get mean age
query = "SELECT cellname, age FROM cells"
cursor.execute(query)
# now: where is the result of the query? To get it do:
q_result = cursor.fetchall()
# q_result stores the result of the query as a list of tuples where each tuple
# represents one row. To illustrate this, we SELECTed both, name and age. Try:
# >>> print q_result
_, age = zip(*q_result)
mean_age = np.mean(age)
print mean_age

# Another way to get the mean: let the database work!
query = """
  SELECT avg(age) FROM cells"""
cursor.execute(query)
q_result = cursor.fetchall()
mean_age = q_result[0][0]
print mean_age

# This makes
query = """
  SELECT age, avg(surface_area) FROM cells GROUP BY age"""
cursor.execute(query)
q_result = cursor.fetchall()
age, mean_surface_area = zip(*q_result)
print age, mean_surface_area

query = """
  CREATE TABLE results(
    cellname VARCHAR(64),
    simulation VARCHAR(64),
    result INTEGER,
    PRIMARY KEY (cellname, simulation)
    )"""

cursor.execute(query)

simulations = ['sim1', 'sim2']
for idx, simulation in enumerate(simulations):
  for name in names:
    result = int(10*idx + rand(1) * 5)
    query = """
      INSERT INTO results(cellname, simulation, result)
      VALUES (?,?,?)
    """
    cursor.execute(query, (name, simulation, result)) # write to db-buffer
cxn.commit() # write to database

query = """
  SELECT
    t1.cellname, t1.age, t1.surface_area,
    t2.simulation, t2.result, t2.cellname
  FROM cells t1, results t2
  WHERE t1.cellname = t2.cellname
  """


