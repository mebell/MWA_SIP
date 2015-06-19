#P#!/bin/bash
#PBS -l walltime=04:30:00
#PBS -l mem=58GB
#PBS -l ncpus=16
#PBS -P ek6
#PBS -q normal

# Import the bloody bash file again becuase qsub is retarded. 
#MIRIAD
MIR=/short/ek6/MWA_Code/miriad; export MIR
. $MIR/MIRRC.sh
export PATH=$MIRBIN:$PATH

# CASA PATH
#export PATH=/short/ek6/CASA/casapy-41.0.24668-001-64b-2:$PATH
#export PATH=/short/ek6/CASA/casapy-34.0.19988-002-64b:$PATH
export PATH=/short/ek6/CASA/casapy-stable-42.0.26465-001-64b:$PATH

# MWA_Tools
export MWA_CODE_BASE=/short/ek6/MWA_Code
export PATH=${PATH}:${MWA_CODE_BASE}/bin

# Python stuff for MWA Tools
if [ "$PYTHONPATH" == "" ]; then
  export PYTHONPATH=${MWA_CODE_BASE}/lib/python2.7/site-packages
else
  export PYTHONPATH=${PYTHONPATH}:${MWA_CODE_BASE}/lib/python2.7/site-packages
fi

# Cotter, aoflagger etc. 
export PATH=${PATH}:/short/ek6/MWA_Code/install/bin


#Setup path for pkg-config in .bashrc:
LOCAL_PKG_CONFIG_PATH=${MWA_CODE_BASE}/lib/pkgconfig
if [ "$PKG_CONFIG_PATH" == "" ]; then
  export PKG_CONFIG_PATH=$LOCAL_PKG_CONFIG_PATH
else
  export PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:${LOCAL_PKG_CONFIG_PATH}
fi

# for MWA ngas DB access
export PGPASSWORD=BowTie
export PGHOST=ngas01.ivec.org
export PGDATABASE=mwa
export PGUSER=mwa

# Import raijin python modules
module load python/2.7.5 python/2.7.5-matplotlib

################# CODE #######################
#change_db.py curtin
python /home/562/meb562/MWA_SIP/pre_proc_pipe.py 1093112584
