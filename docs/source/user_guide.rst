.. _user_guide:

User Guide
==========

This guide explains how to use the Interpolation Project for 2D interpolation tasks.

Installation
------------

Install the project using Poetry:

.. code-block:: bash

   poetry install

Running the CLI
---------------

To perform interpolation, use the CLI:

.. code-block:: bash

   poetry run python -m src.cli interpolate --algorithm bilinear

Visualization
-------------

To visualize interpolation results, run:

.. code-block:: bash

   poetry run python demo/example1.py

This generates a plot in the ``plots/`` directory comparing all algorithms.

Performance Analysis
-------------------

See the :ref:`performance` section for details on algorithm performance.