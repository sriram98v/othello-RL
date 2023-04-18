#!/bin/bash

# Copy/paste this job script into a text file and submit with the command:
#    sbatch thefilename

#SBATCH --time=12::00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=36   # 36 processor core(s) per node 
#SBATCH --mem=8G   # maximum memory per node
#SBATCH --partition=class-long    # class node(s)
#SBATCH --job-name="train_vs_heu"
#SBATCH --mail-user=<fill_here>@iastate.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --output="stdout.out" # job standard output file (%j replaced by job id)
#SBATCH --error="stderror.out" # job standard error file (%j replaced by job id)

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE

module load python_3/3.9.2
python3 -m venv othello-RL
source othello-RL/bin/activate
python3 -m pip --no-cache-dir -r requirements.txt
python3 train_heu.py