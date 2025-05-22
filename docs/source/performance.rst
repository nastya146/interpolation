.. _performance:

Performance Analysis
====================

This section presents the performance of the interpolation algorithms.

Methodology
-----------

We measured the execution time of each algorithm (``bilinear``, ``lagrange``, ``l2_constant``, ``l2_linear``) for different grid sizes (2x2, 4x4, 8x8, 16x16). The input data consisted of a 2x2 grid with fixed coordinates and values.

Results
-------

The following plot shows the execution time as a function of grid size:

.. figure:: ../plots/performance.png
   :width: 80%
   :alt: Performance of Interpolation Algorithms

   Performance of interpolation algorithms for different grid sizes.

Analysis
--------

- **Bilinear**: Typically the fastest due to its simplicity, but may fail for certain inputs (see CLI test issues).
- **Lagrange**: Slower due to polynomial computations, with performance degrading as grid size increases.
- **L2 Constant/Linear**: Computationally intensive, especially for larger grids, due to optimization procedures.