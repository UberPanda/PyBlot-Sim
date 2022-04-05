# PyBlot-Sim

- The Common folder includes the current most complete version of the simulator, including all algorithms, schedulers, error functions, etc.

- The Test folder contains minimum working examples for each problem and model. 

- Any script can be run with CPython3 (the standard python3 implementation). It can also be run without any modification using pypy3 for massive performance gains. However, pypy3 may be tricky to set up with matplotlib, so, unless you know what you are doing, we recommend running scripts using matplolib with CPython3. these scripts are marked with an initial '# Run with python, not pypy' comment.

- The file structure is the following : 
	- The root folder contains the simulation script 
	- The simulator backend is stored in 5 files in the Common subfolder
	- lib_algorithm contains the algorithms to be executed in the COMPUTE phase
	- lib_robot defines the robot class
	- lib_schedulers defines the scheduling functions to be called by the simulation script
	- lib_sim_functions contains functions to be used for the simulation, such as error functions
	- lib_misc_functions contains convenience functions, such as a centroid function
	- Some problems require the use of a Smallest Enclosing Circle. We use lib_SEC, from Project Nayuki to compute the SEC. this is conveniently done for robots by the rob_SEC function in lib_misc_functions, so this file should not be modified.


> The simulator is currently unproven and should never be used a substitute for actual proofs.

See details at : https://arxiv.org/pdf/2105.09667.pdf

