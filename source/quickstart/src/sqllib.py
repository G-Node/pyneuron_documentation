import matplotlib.pyplot as plt
import numpy as np

class SQLaggregate(object):
  """
  This class serves as the parent class of self written aggregate functions.
  The subclasses have to define the `finalize` function.

  **Important**: each aggregate function has to be listed in the function
  `create_aggregate_functions`
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


def create_aggregate_functions(cxn):
  cxn.create_aggregate("SQLstd", 1, SQLstd)
  cxn.create_aggregate("SQLsem", 1, SQLsem)

# Here are two function to illustrate how to plot data from a database and how
# to use aggregate functions:

def show_scatter_query(cursor, query, title='Hello World', xlabel="x", ylabel='y',
                       alpha=0.1):
  cursor.execute(query)
  sql_result = cursor.fetchall()
  x, y = zip(*sql_result)
  plt.scatter(x, y, facecolor='black', edgecolor='black', alpha=alpha)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.show()

def show_query_errorbar(cursor, query, y='avg(Rin)', err='SQLsem(Rin)',
                        condition='Ra=1'):
  cursor.execute(query %(y, err, condition))
  sql_result = cursor.fetchall()
  x, y, errorbar = zip(*sql_result)
  plt.scatter(x, y, facecolor='black', edgecolor='black', alpha=1)
  plt.errorbar(x, y, errorbar, fmt=None, ecolor='black')
  plt.show()
