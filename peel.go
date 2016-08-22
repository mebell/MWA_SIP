
# Verbatim copy of Natasha's Peel code.

obsnum=$1

# Autoprocess: first check if it's going to do some peeling
/short/ek6/MWA_Code/anoko/mwa-reduce/build_4/autoprocess -noselfcal /short/ek6/MWA_Code/MWA_Tools/gleam_scripts/phase2/bsm_v1.txt ${obsnum}.ms | tee peel_test.txt
if grep -q "Peel out source" peel_test.txt
then
    # Check to see whether it's double sources, first
    if grep -q "Runner-up source" peel_test.txt
    then
	echo "Double sources detected: no peeling, but image size increased to 5000."
	imsize=5000
    else
	src=`grep "Peel out source" peel_test.txt  | awk '{print $NF}'`
	dist=`grep $src peel_test.txt  | grep distance | awk '{print $4}' | awk 'BEGIN {FS="="} {print int($2)}'`
	maxdist=`echo "2200 / $chan" | bc -l | awk '{print int($1)}'`
	if [[ $dist -gt $maxdist ]]
	then
	    /short/ek6/MWA_Code/anoko/mwa-reduce/build_4/autoprocess -noselfcal -go /short/ek6/MWA_Code/MWA_Tools/gleam_scripts/phase2/bsm_v1.txt ${obsnum}.ms
	    caldatacolumn="-datacolumn CORRECTED_DATA"
            #chgcentre -minw -shiftback ${obsnum}.ms
	else
	    echo "Source $src will lie within the imaged field-of-view so doesn't need peeling."
	fi
    fi
fi

chgcentre -minw -shiftback ${obsnum}.ms











