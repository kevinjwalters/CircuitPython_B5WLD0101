Introduction
============

This is a `CircuitPython <https://circuitpython.org/>`_ library which
reads the outputs from an Omron B5W LD0101 particulate matter sensor
using pulseio to count the pulses to return the count per second
for OUT1 and OUT2.


Dependencies
=============

This library depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_


Usage Example
=============

.. code-block:: python

    import board
    import time
    import b5wld0101

    b5wld0101 = b5wld0101.B5WLD0101(board.GP10, board.GP11)
    while True:
        print(b5wld0101.read())
        time.sleep(5)

