#!/bin/bash

# Copy/paste this job script into a text file and submit with the command:
#    sbatch thefilename

#SBATCH --time=24:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=64   # 64 processor core(s) per node
#SBATCH --mem=64G   # maximum memory per node
#SBATCH --partition=huge    # huge node(s)
#SBATCH --job-name="@train_hue"
#SBATCH --output="@train_hue" # job standard output file (%j replaced by job id)

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE

cd /work/ratul/chuen/structural_characterization/pbd_python_script/673/othello-RL
module load miniconda3/4.10.3-svrr7oe
source activate viralescape_conda_env

python train_heu.py

conda deactivate
module purge