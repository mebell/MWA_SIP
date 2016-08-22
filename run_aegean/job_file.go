#!/bin/bash
#PBS -l walltime=08:00:00
#PBS -l mem=1GB
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
cd /short/ek6/meb562/SIP_results/MWA_SIP_out/mwats
################# CODE #######################
#change_db.py curtin
python /short/ek6/MWA_Code/Aegean/BANE.py 1131912952_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131912952_W_bm_1.0_SC_I.fits --table 1131912952_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1113072208_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1113072208_W_bm_1.0_SC_I.fits --table 1113072208_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135618816_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135618816_W_bm_1.0_SC_I.fits --table 1135618816_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138371952_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138371952_W_bm_1.0_SC_I.fits --table 1138371952_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140867168_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140867168_W_bm_1.0_SC_I.fits --table 1140867168_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1093097704_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1093097704_W_bm_1.0_SC_I.fits --table 1093097704_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135605976_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135605976_W_bm_1.0_SC_I.fits --table 1135605976_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121885744_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121885744_W_bm_1.0_SC_I.fits --table 1121885744_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1093121464_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1093121464_W_bm_1.0_SC_I.fits --table 1093121464_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124638744_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124638744_W_bm_1.0_SC_I.fits --table 1124638744_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128263848_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128263848_W_bm_1.0_SC_I.fits --table 1128263848_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135605016_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135605016_W_bm_1.0_SC_I.fits --table 1135605016_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124647384_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124647384_W_bm_1.0_SC_I.fits --table 1124647384_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1088177400_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1088177400_W_bm_1.0_SC_I.fits --table 1088177400_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138381912_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138381912_W_bm_1.0_SC_I.fits --table 1138381912_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121883704_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121883704_W_bm_1.0_SC_I.fits --table 1121883704_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121874464_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121874464_W_bm_1.0_SC_I.fits --table 1121874464_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138382632_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138382632_W_bm_1.0_SC_I.fits --table 1138382632_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128266128_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128266128_W_bm_1.0_SC_I.fits --table 1128266128_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1093110904_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1093110904_W_bm_1.0_SC_I.fits --table 1093110904_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135598656_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135598656_W_bm_1.0_SC_I.fits --table 1135598656_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138385392_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138385392_W_bm_1.0_SC_I.fits --table 1138385392_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124628424_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124628424_W_bm_1.0_SC_I.fits --table 1124628424_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1076087744_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1076087744_W_bm_1.0_SC_I.fits --table 1076087744_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1070388824_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1070388824_W_bm_1.0_SC_I.fits --table 1070388824_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1096735528_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1096735528_W_bm_1.0_SC_I.fits --table 1096735528_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1093091224_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1093091224_W_bm_1.0_SC_I.fits --table 1093091224_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140794624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140794624_W_bm_1.0_SC_I.fits --table 1140794624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128269128_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128269128_W_bm_1.0_SC_I.fits --table 1128269128_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124653624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124653624_W_bm_1.0_SC_I.fits --table 1124653624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1076093144_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1076093144_W_bm_1.0_SC_I.fits --table 1076093144_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138387432_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138387432_W_bm_1.0_SC_I.fits --table 1138387432_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140799544_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140799544_W_bm_1.0_SC_I.fits --table 1140799544_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121886344_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121886344_W_bm_1.0_SC_I.fits --table 1121886344_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135599376_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135599376_W_bm_1.0_SC_I.fits --table 1135599376_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1116696096_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1116696096_W_bm_1.0_SC_I.fits --table 1116696096_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131912592_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131912592_W_bm_1.0_SC_I.fits --table 1131912592_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1096724608_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1096724608_W_bm_1.0_SC_I.fits --table 1096724608_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140797264_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140797264_W_bm_1.0_SC_I.fits --table 1140797264_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124657944_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124657944_W_bm_1.0_SC_I.fits --table 1124657944_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124661064_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124661064_W_bm_1.0_SC_I.fits --table 1124661064_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140887688_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140887688_W_bm_1.0_SC_I.fits --table 1140887688_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138381192_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138381192_W_bm_1.0_SC_I.fits --table 1138381192_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131904672_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131904672_W_bm_1.0_SC_I.fits --table 1131904672_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121896544_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121896544_W_bm_1.0_SC_I.fits --table 1121896544_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138376752_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138376752_W_bm_1.0_SC_I.fits --table 1138376752_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140799664_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140799664_W_bm_1.0_SC_I.fits --table 1140799664_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131884632_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131884632_W_bm_1.0_SC_I.fits --table 1131884632_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1108823480_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1108823480_W_bm_1.0_SC_I.fits --table 1108823480_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131880792_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131880792_W_bm_1.0_SC_I.fits --table 1131880792_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1088169840_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1088169840_W_bm_1.0_SC_I.fits --table 1088169840_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140789944_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140789944_W_bm_1.0_SC_I.fits --table 1140789944_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1113077968_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1113077968_W_bm_1.0_SC_I.fits --table 1113077968_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128274168_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128274168_W_bm_1.0_SC_I.fits --table 1128274168_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140888408_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140888408_W_bm_1.0_SC_I.fits --table 1140888408_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124627704_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124627704_W_bm_1.0_SC_I.fits --table 1124627704_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131880312_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131880312_W_bm_1.0_SC_I.fits --table 1131880312_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1080310472_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1080310472_W_bm_1.0_SC_I.fits --table 1080310472_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1089464440_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1089464440_W_bm_1.0_SC_I.fits --table 1089464440_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1093095184_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1093095184_W_bm_1.0_SC_I.fits --table 1093095184_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131882472_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131882472_W_bm_1.0_SC_I.fits --table 1131882472_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1096725328_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1096725328_W_bm_1.0_SC_I.fits --table 1096725328_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121889584_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121889584_W_bm_1.0_SC_I.fits --table 1121889584_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140875208_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140875208_W_bm_1.0_SC_I.fits --table 1140875208_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138396192_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138396192_W_bm_1.0_SC_I.fits --table 1138396192_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1089468760_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1089468760_W_bm_1.0_SC_I.fits --table 1089468760_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1096744648_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1096744648_W_bm_1.0_SC_I.fits --table 1096744648_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1117730592_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1117730592_W_bm_1.0_SC_I.fits --table 1117730592_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128278728_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128278728_W_bm_1.0_SC_I.fits --table 1128278728_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121872904_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121872904_W_bm_1.0_SC_I.fits --table 1121872904_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135616296_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135616296_W_bm_1.0_SC_I.fits --table 1135616296_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140870048_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140870048_W_bm_1.0_SC_I.fits --table 1140870048_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140875808_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140875808_W_bm_1.0_SC_I.fits --table 1140875808_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1117736592_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1117736592_W_bm_1.0_SC_I.fits --table 1117736592_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1121886104_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1121886104_W_bm_1.0_SC_I.fits --table 1121886104_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128274408_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128274408_W_bm_1.0_SC_I.fits --table 1128274408_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1116700176_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1116700176_W_bm_1.0_SC_I.fits --table 1116700176_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140781544_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140781544_W_bm_1.0_SC_I.fits --table 1140781544_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1096740328_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1096740328_W_bm_1.0_SC_I.fits --table 1096740328_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135625416_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135625416_W_bm_1.0_SC_I.fits --table 1135625416_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1093111624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1093111624_W_bm_1.0_SC_I.fits --table 1093111624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140779624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140779624_W_bm_1.0_SC_I.fits --table 1140779624_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1076087024_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1076087024_W_bm_1.0_SC_I.fits --table 1076087024_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1108831280_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1108831280_W_bm_1.0_SC_I.fits --table 1108831280_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128272608_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128272608_W_bm_1.0_SC_I.fits --table 1128272608_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1088178720_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1088178720_W_bm_1.0_SC_I.fits --table 1088178720_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1088182320_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1088182320_W_bm_1.0_SC_I.fits --table 1088182320_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140781184_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140781184_W_bm_1.0_SC_I.fits --table 1140781184_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1096724728_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1096724728_W_bm_1.0_SC_I.fits --table 1096724728_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124655064_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124655064_W_bm_1.0_SC_I.fits --table 1124655064_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1124624464_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1124624464_W_bm_1.0_SC_I.fits --table 1124624464_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131905512_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131905512_W_bm_1.0_SC_I.fits --table 1131905512_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1140893208_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1140893208_W_bm_1.0_SC_I.fits --table 1140893208_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1131905032_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1131905032_W_bm_1.0_SC_I.fits --table 1131905032_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135608496_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135608496_W_bm_1.0_SC_I.fits --table 1135608496_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1135619536_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1135619536_W_bm_1.0_SC_I.fits --table 1135619536_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138397992_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138397992_W_bm_1.0_SC_I.fits --table 1138397992_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1070393144_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1070393144_W_bm_1.0_SC_I.fits --table 1070393144_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1128260128_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1128260128_W_bm_1.0_SC_I.fits --table 1128260128_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/BANE.py 1138392952_W_bm_1.0_SC_I.fits
python /short/ek6/MWA_Code/Aegean/aegean.py --autoload 1138392952_W_bm_1.0_SC_I.fits --table 1138392952_W_bm_1.0_SC_I.fits
