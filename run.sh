#!/bin/bash
#SBATCH -J spellcheck
#SBATCH -A cin_staff 
#SBATCH -p dcgp_usr_prod
#SBATCH --time 00:30:00     
#SBATCH -N 1                
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=56
#SBATCH --qos=boost_qos_dbg
#SBATCH --mem=100GB
#SBATCH --output=out.out

module load python
source env/bin/activate

python -u check.py
