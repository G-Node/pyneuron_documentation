.. _FAQ_python':

python FAQ
----------

.. contents::

.. _python_assert:

How can I check statements with assert?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``assert`` is usefull to check Boolean expressions (``True`` or ``False``). The
programm will continue in the ``True``-case but will raise an exception in the
``False``-case (and terminate the programm if the exception is not caught). The
statement goes like this::

  assert 1 == 0, "One doesn't equal zero."

A ``try-except`` statement could catch an `AssertationError`::

  try:
    assert 1 == -, "One doesn't equal zero"
  except AssertionError, args:
    print('%s: %s' %(args.__class__.__name__, args)

See also the usage within properties of part...
