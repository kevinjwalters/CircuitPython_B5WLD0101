# SPDX-FileCopyrightText: 2021 Kevin J. Walters
#
# SPDX-License-Identifier: MIT
"""
`b5wld0101`
================================================================================

Helper library for the Omron B5W-LD0101 Air Quality (particulate matter) sensor.

Ensure the outputs are converted to a safe level if using a 3.3V microcontroller -
this can be achieved with a 4.7k resistor to ground on each output.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

**Hardware:**

* `Omron B5W-LD0101 <https://components.omron.com/product-detail?partId=39064>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware with pulseio or countio for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/kevinjwalters/CircuitPython_B5WLD0101.git"


import time
import analogio
import pulseio

class B5WLD0101:
    """TODO
    """

    FIELD_NAMES = (
        "pm25 standard",
        "pm100 standard",
        "particles 25um",
        "particles 100um",
        "raw out1",
        "raw out2",
    )

    DEFAULT_PULSES = 500


    def __init__(self, pin_out1, pin_out2,
                 *,
                 pin_vth=None, max_pulses=DEFAULT_PULSES):

        self.pin_out1 = pin_out1
        self.pin_out2 = pin_out2
        self.pin_vth = pin_vth

        now_t = time.monotonic()
        self._last_read1 = now_t
        self._last_read2 = now_t
        self._max_pulses = max_pulses
        self._pulse1 = pulseio.PulseIn(pin_out1, max_pulses)
        self._pulse2 = pulseio.PulseIn(pin_out2, max_pulses)
        self.overflows = 0

        self._vth = analogio.AnalogIn(pin_vth) if pin_vth else None

        self.aqi_reading = {k: None for k in self.FIELD_NAMES}

    ### Infrequent 1ms test pulses can show up as
    ### [971] then [971, 65535, 971]
    ### or less frequently as [65535, 972] then [65535, 972, 65535, 972]
    def _measure(self, pulsein):
        duration = 0
        pulsein.pause()
        pulses = len(pulsein)
        if pulses:
            duration = sum([pulsein[idx] for idx in range(pulses)])
        pulsein.clear()
        pulsein.resume()
        if pulses == self._max_pulses:
            self.overflows += 1

        if duration == 0:
            return (0, 0.0)
        particles = (pulses + 1) // 2
        return (particles, duration * 1e-6)


    def _get_raw_values(self):
        """TODO
        """
        read1_t = time.monotonic()
        pm_25, _ = self._measure(self._pulse1)
        read2_t = time.monotonic()
        pm_25_100, _ = self._measure(self._pulse2)

        pm_25_per_sec = pm_25 / max(read1_t - self._last_read1, 0.005)
        self._last_read1 = read1_t
        pm_25_100_per_sec = pm_25_100 / max(read2_t - self._last_read2, 0.005)
        self._last_read2 = read2_t
        return (pm_25_per_sec, pm_25_100_per_sec)


    def read(self):
        """TODO
        """
        raw_25, raw_25_100 = self._get_raw_values()
        self.aqi_reading["raw out1"] = raw_25
        self.aqi_reading["raw out2"] = raw_25_100
        return self.aqi_reading
