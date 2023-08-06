.. _sec_tutorial:

========
Tutorial
========

*********************
Sampling ARGs
*********************
As a simple example, we will first simulate sample
 data with  `msprime <https://tskit.dev/msprime/docs/stable/>`_. We will then run `arginfer` on the simulated dataset.

The following code simulates a tree sequence and the sequences for a sample size of `10` and sequence
length of `1e5`.

.. code-block:: python

    import msprime
    import os
    ts_full = msprime.simulate(sample_size=10, Ne=5000,
                                            length=1e5,
                                            mutation_rate=1e-8,
                                            recombination_rate=1e-8,
                                            record_full_arg= True,
                                            random_seed=2)
    ts_full.dump(os.getcwd()+"/out/"+"ts_full.args")

#.. comment:: To run arginfer, we cawe use `arginfer` to take `ts_full.args` and

The output of this code is a `tree sequence` stored in "out/" directory under the name of `ts_full.args`.

Next, we take this simulated tree sequence and run `arginfer` to infer the ARG:



.. code-block::
pip install -i https://test.pypi.org/simple/ arginfer

