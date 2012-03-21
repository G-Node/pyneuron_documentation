.. _simulation:

Part 3: Writing a Simulation
============================
:Author: Philipp Rautenberg <philipp.rautenberg@skip_this.g-node.org>
:Tags: basics pyneuron sql sqlite

Exercise
--------

**Use a SQL database to control data**

  * Create a SQLite database
  * Run a simulation for a given parameter space
  * Store data in a database
  * Look at the data with Firefox add on `SQLite Manager`
  * Analyze data with a database

Code
----

Here is the same procedure like in part2: first the script and below the
library.

``simulation.py``:

.. literalinclude:: src/simulation.py

And here the sql-library:

``sqllib.py``:

.. literalinclude:: src/sqllib.py

Remarks
-------

* For FAQ see :ref:`FAQ_SQL`
