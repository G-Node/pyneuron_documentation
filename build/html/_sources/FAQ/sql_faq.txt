.. _FAQ_SQL:

=========
SQL - FAQ
=========

.. contents::

.. _SQL_add_change_delete_column:

How to add/change/delete a column in a table?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example for a sqlite-database:

 cursor.execute(
   'ALTER TABLE table_name' + 
   'ADD column_name datatype')

 cursor.execute(
   'ALTER TABLE table_name' + 
   'DROP column_name')

 cursor.execute(
   'ALTER TABLE table_name' + 
   'ALTER column_name datatype')

.. _SQL_analyse_group:

How to analyze by group?
~~~~~~~~~~~~~~~~~~~~~~~~

Example for a sqlite-database::

 cursor.execute(
   'SELECT age, COUNT(age) ' + 
   'FROM morphologies ' + 
   'GROUP BY age')

.. _SQL_composite_primary_key:

How to create a table with a composite primary key?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example for a sqlite-database::

 CREATE TABLE track(
  album CHAR(10),
  disk INTEGER,
  posn INTEGER,
  song VARCHAR(255),
  PRIMARY KEY (album, disk, posn)
 )

Source: `SQLzoo <http://sqlzoo.net/howto/source/u.cgi/tip241027/sqlite>`_

Note: this doesn't work if a PK-field contains a NULL.

.. _SQL_selfwritten_aggregate_functions:

How can i write my own aggregate functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example for a sqlite-database::

  import sqlite3 as sqlite
  import numpy as np
  class self_written_SQLvar(object):
    def __init__(self):
      import numpy as np
      self.values = []
    def step(self, value):
      self.values.append(value)
    def finalize(self):
      return np.array(self.values).var()
  cxn = sqlite.connect(':memory:')
  cur = cxn.cursor()
  cur.execute("CREATE TABLE 'mytable' ('numbers' INTEGER)")
  cur.execute("INSERT INTO 'mytable' VALUES (1)") 
  cur.execute("INSERT INTO 'mytable' VALUES (2)") 
  cur.execute("INSERT INTO 'mytable' VALUES (3)") 
  cur.execute("INSERT INTO 'mytable' VALUES (4)")
  cxn.create_aggregate("self_written_SQLvar", 1, self_written_SQLvar)
  a = cur.execute("SELECT avg(numbers), self_written_SQLvar(numbers) FROM mytable")
  print a.fetchall()
  # >>> [(2.5, 1.25)]
