.. _FAQ_pyNEURON:

pyNEURON FAQ
------------

.. contents::

.. _pyNEURON_Python_Dataexchange:

How can I exchange data between pyNEURON and Python?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Don't use ``py_vector = hoc_vector.to_python()`` or ``hoc_vector =
from_python(py_vector)`` for memory reasons (see `The NEURON Forum
<https://www.neuron.yale.edu/phpBB/viewtopic.php?f=2&t=1383>`_).

Instead use::

  # to convert a hoc-vector to a list or a numpy array:
  py_vector = list(hoc_vector) #, or
  py_vector = numpy.array(hoc_vector)

  # to convert a list or a numpy array to a hoc-vector:
  hoc_vector = neuron.h.Vector(py_vector)

.. _Change_Cell_Morphology:

How to change the cell morphology without restarting the NEURON module?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Delete all sections ``neuron.h('forall delete_section')``
#. Create your new morphology or load new morphology from hoc file
   with ``neuron.h.load_file(1, hoc_file)``. Note: ``load_file(hoc_file)`` only
   loads once.

See also this post: `NEURON forum
<http://www.neuron.yale.edu/phpBB2/viewtopic.php?f=2&t=1484&p=5369#p5369>`_:

.. _nrngui_python_libraries:

Why doesn't nrngui find self written libraries?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to run the python scripts with the gui of neuron with ``nrngui
-python my_python_script.py`` and nrngui can't find self written libraries you
just have to export the library path with ``export PYTHONPATH
path/to/mylibrary``. 
