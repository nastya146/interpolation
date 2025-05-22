.. _reference:

Reference
=========

This section describes the API and CLI of the Interpolation Project.

Command-Line Interface
---------------------

The CLI is implemented in ``src/cli.py`` and supports interpolation with different algorithms.

.. code-block:: bash

   poetry run python -m src.cli interpolate --algorithm bilinear

Available algorithms:
- ``bilinear``: Bilinear interpolation.
- ``lagrange``: Lagrange interpolation.
- ``l2_constant``: L2 optimization (constant).
- ``l2_linear``: L2 optimization (linear).

API
---

.. automodule:: src.linear_interpolation
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: src.lagrange_interpolation
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: src.l2_interpolation
   :members:
   :undoc-members:
   :show-inheritance: