#!/bin/bash
#PBS -q analysis
#PBS -l walltime=36:00:00
#PBS -l nodes=1:ppn=1
#PBS -j oe
#SBATCH --mem=214GB

source ~/.bash_profile

cd $SLURM_SUBMIT_DIR

cd /import/c1/ICESHEET/aaschwanden/pism-gris/stability/2018_08_ctrl/spatial
mkdir -p ../basins
/usr/local/unsupported/ICESHEET/gris-analysis/basins/extract_basins.py --basins $2  --o_dir ../basins ex_gris_g900m_v3a_rcp_$1_id_CTRL_0_1000.nc
