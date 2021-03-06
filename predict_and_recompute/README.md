# New communication hiding conjugate gradient variants

This folder contains materials to help reproduce the results of:
    
    @article{predict_and_recompute_cg,
        title={Predict-and-recompute conjugate gradient variants},
        author={Tyler Chen and Erin C. Carson},
        year={2020},
        eprint={1905.01549},
        archivePrefix={arXiv},
        primaryClass={cs.NA},
        note = {arXiv preprint: 1905.01549}
    }

An extended introduction to this paper can be found [here](https://chen.pw/research/publications/predict_and_recompute.html).

### Sample Convergence
![sample-convergence](numerical_experiments/figures/model_48_8_3-bcsstk03-s3rmq4m1_None-None-jacobi_error_A_norm.svg)

### Sample Scaling
![sample-scaling](scaling_experiments_mpi4py/figures/strong_scale.svg)


## Instructions
All figures and table data from the paper can be generated by navigating to the `experiments` folder, and running `figure_gen.py`.

Generating plots for different matrices is easy. 
Simply add the desired `.mtx` files to the `matrices` folder, and add update the `matrices` list in `figure_gen.py` accordingly. 

To generate plots of different quantities, define the appropriate callback function and add it to the `test_matrix` function.
Then add a plot of this quantity in the `plot_matrix_test` function.


## Notes
You will need Python 3.6 or higher, since some of the python code uses use f-strings.
If you do not have access to Python 3.6, you can replace all f-strings with other string formats and everything should work (if you have a reasonably recent versions of numpy and scipy).

While lots of the experiments run almost instantly on a laptop, there are other experiments which require much longer (hours or days depending on your hardware).
The code is fairly modular, so you can test a single variant on a single matrix, and then regenerate the corresponding figure.
This makes it easier to verify the convergence of a single variant on big problems, since you don't have to run all of the variants.

Github has a filesize limit of 100mb so we couldn't upload the matrix `s3dkq4m2`.
It can be downloaded from the matrix market](https://math.nist.gov/MatrixMarket/data/misc/cylshell/s3dkq4m2.html).

Finally, while we have done our best to run a range of representative experiments, it is quite possible that there are problems on which the variants from this paper do not work better than previously known communication hiding variants.
We would be interested in knowing of such problems so we can use them in tests in the future.


## Repository contents

This folder is roughly structured as follows:

- `numerical_experiments` : python scripts for generating numerical experiments
    - `cg_variants` : implementations of various conjugate gradient variants for numerical experiments
    - `callbacks` : some available callback functions to use with implemented variants to gather convergence data
    - `data` : raw convergence data and table summary statisitcs
    - `figures` : convergence plots for all numerical experiments, and compiled table summary statistics
- `scaling_experiments_mpi4py` : scripts to run scaling tests in mpi4py and plot results
    - `data` : timing and convergence data
    - `cg_variants` : mpi4py implementations of all variants
- `scaling_experiments_petsc` : scripts to run scaling tests in PETSc and plot results
    - `logs` : you will need to extract `logs.tar.gz` to generate plots
    - `cg_impls` : PETSc implementations of PipePRCG
    - `config_info` : information about configuration of MPI and PETSc
- `matrices` : test matrices

