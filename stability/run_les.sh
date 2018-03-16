#!/bin/bash

odir=2018_01_les
s=pleiades_ivy
q=long
n=160
grid=1800

./lhs_ensemble.py -e ../latin_hypercube/lhs_samples_20180107.csv --calibrate --o_dir ${odir} --exstep 1 -n ${n} -w 48:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc


for id2 in `seq 0 1`;
do
for id1 in `seq 0 9`;
do
for id in `seq 0 9`;
do
for rcp in 26 45 85;
do
qsub 2018_01_les/run_scripts/lhs_g1800m_v3a_rcp_${rcp}_id_${id2}${id1}${id}_j.sh 
done
done
done
done


odir=2017_12_les
s=chinook
q=t2standard
n=72
grid=3600

./lhs_ensemble.py -e ../latin_hypercube/lhs_samples_20171104.csv --calibrate --o_dir ${odir} --exstep 1 -n ${n} -w 10:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc


for id in `seq 0 9`;
do
for rcp in 26 45 85;
do
sbatch 2017_11_lhs/run_scripts/lhs_g3600m_v3a_rcp_${rcp}_id_00${id}_j.sh;
done
done

for id2 in `seq 0 4`;
do
for id1 in `seq 0 9`;
do
for id in `seq 0 9`;
do
for rcp in 26 45 85;
do
JOBID=$(sbatch 2017_12_les/run_scripts/lhs_g3600m_v3a_rcp_${rcp}_id_${id2}${id1}${id}_j.sh | sed 's/[^0-9]*//g')
sbatch --dependency=afterok:$JOBID 2017_12_les/run_scripts/post_lhs_g3600m_v3a_rcp_${rcp}_id_${id2}${id1}${id}.sh;
done
done
done
done

odir=2018_01_les
s=pleiades_ivy
q=long
n=160
grid=1800

./lhs_ensemble.py -e ../latin_hypercube/lhs_samples_20180107.csv --calibrate --o_dir ${odir} --exstep 1 -n ${n} -w 10:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

odir=2017_12_les
s=pleiades_ivy
q=long
n=80
grid=3600

./lhs_ensemble.py -e ../latin_hypercube/lhs_samples_20171104.csv --calibrate --o_dir ${odir} --exstep 1 -n ${n} -w 10:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc


for id2 in `seq 5 10`;
do
for id1 in `seq 0 9`;
do
for id in `seq 0 9`;
do
for rcp in 26 45 85;
do
qsub 2017_12_les/run_scripts/post_g3600m_v3a_rcp_${rcp}_id_${id2}${id1}${id}.sh 
#qsub -W depend=afterok:$JOBID 2017_12_les/run_scripts/post_lhs_g3600m_v3a_rcp_${rcp}_id_${id2}${id1}${id}.sh;
done
done
done
done

odir=2017_06_vc
s=pleiades_ivy
q=long
n=80
grid=3600

./lhs_ensemble.py -e ../latin_hypercube/lhs_samples_20171104.csv --calibrate --o_dir ${odir} --exstep 1 -n ${n} -w 10:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc


odir=2017_12_ctrl
s=chinook
q=t2small
n=12
grid=18000

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 2:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

odir=2017_12_ctrl
s=chinook
q=t2small
n=24
grid=9000

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 2:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

odir=2017_12_ctrl
s=chinook
q=t2small
n=48
grid=4500

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 6:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

odir=2017_12_ctrl
s=chinook
q=t2standard
n=72
grid=3600

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 10:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc


odir=2017_12_ctrl
s=chinook
q=t2standard
n=144
grid=1800

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 36:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

odir=2017_12_ctrl
s=chinook
q=t2standard
n=360
grid=900

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 168:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 168:00:00 -g ${grid} -s ${s} -q ${q} --step 1000 --duration 5000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc


odir=2017_12_ctrl
s=pleiades_haswell
q=long
n=480
grid=600

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 100:00:00 -g ${grid} -s ${s} -q ${q} --step 200 --duration 1000 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

odir=2017_12_600m
s=chinook
q=t2standard
n=480
grid=600

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 168:00:00 -g ${grid} -s ${s} -q ${q} --step 200 --duration 200 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc

odir=2017_12_450m
s=pleiades_haswell
q=long
n=600
grid=450

./lhs_ensemble.py -e ../latin_hypercube/lhs_control.csv --o_dir ${odir} --exstep 1 -n ${n} -w 100:00:00 -g ${grid} -s ${s} -q ${q} --step 200 --duration 200 ../calibration/2017_06_vc/state/gris_g${grid}m_flux_v3a_no_bath_sia_e_1.25_sia_n_3_ssa_n_3.25_ppq_0.6_tefo_0.02_calving_vonmises_calving_0_100.nc



odir=2017_12_ctrl
grid=900
mkdir -p ${odir}/station_ts
mkdir -p ${odir}/profiles
for rcp in 45 85 26; do
    # extract_profiles.py -v thk,usurf,tempsurf ../../data_sets/GreenlandIceCoreSites/ice-core-sites.shp ${odir}/spatial/ex_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc ${odir}/station_ts/profile_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc
    extract_profiles.py -v velsurf_mag,velbase_mag,thk,usurf,topg ../../gris-outlet-glacier-profiles/gris-outlet-glacier-profiles-100m.shp 2017_12_ctrl/spatial/ex_g900m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc 2017_12_ctrl/profiles/profiles_100m_ex_g900m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc
done


odir=2017_12_ctrl
grid=900
mkdir -p ${odir}/discharge_relative
for rcp in 45 85 26; do
    cdo runmean,11 -expr,d_rel="100*tendency_of_ice_mass_due_to_discharge/(tendency_of_ice_mass_due_to_discharge-surface_runoff_rate/1e12)" ${odir}/scalar/ts_gris_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_1000.nc ${odir}/discharge_relative/ts_gris_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_1000.nc
done


# CMIP forcing
~/base/gris-analysis/plotting/plotting.py  -n 8 -o giss --plot cmip5 --time_bounds 2008 3000 ../data_sets/climate_forcing/tas_Amon_GISS-E2-H_rcp*0-5000.nc ../data_sets/climate_forcing/tas_cmip5_rcp*ensstd**anom*.nc
# Cumulative contribution LES and CTRL
~/base/gris-analysis/plotting/plotting.py  -n 8 -o les18 --time_bounds 2008 3000 --ctrl_file 2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_*_id_CTRL_0_1000.nc --plot rcp_mass 2018_01_les/scalar_ensstat/ens*_0_1000.nc
# Rates of GMSL rise LES and CTRL
~/base/gris-analysis/plotting/plotting.py -n 8 -o les18 --time_bounds 2008 3000 --no_legend --ctrl_file 2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_*_id_CTRL_0_1000.nc --plot rcp_flux 2018_01_les/scalar_ensstat/ens*_0_1000.nc
# Long term evolution
~/base/gris-analysis/plotting/plotting.py  -o ctrl5k --plot ctrl_mass --time_bounds 2008 7000  2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_26_id_CTRL_0_5000.nc 2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_45_id_CTRL_0_5000.nc 2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_85_id_CTRL_0_2000.nc

# Profiles
~/base/gris-analysis/plotting/plotting.py --bounds 0 12000 --time_bounds 2015 2315  -o rcp26 --plot profile_combined 2017_12_ctrl/profiles/profiles_100m_ex_g900m_v3a_rcp_26_id_CTRL_0_3000.nc
~/base/gris-analysis/plotting/plotting.py --bounds 0 12000 --time_bounds 2015 2315  -o rcp45 --plot profile_combined 2017_12_ctrl/profiles/profiles_100m_ex_g900m_v3a_rcp_45_id_CTRL_0_3000.nc
~/base/gris-analysis/plotting/plotting.py --bounds 0 12000 --time_bounds 2015 2315  -o rcp85 --plot profile_combined 2017_12_ctrl/profiles/profiles_100m_ex_g900m_v3a_rcp_85_id_CTRL_0_3000.nc

# Flux Partitioning
~/base/gris-analysis/plotting/plotting.py -n 4 -o ctrl --time_bounds 2008 3000 --no_legend --plot flux_partitioning 2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_*id_CTRL_0_1000.nc 2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_*id_NTRL_0_1000.nc
# Basin Flux Partitioning
~/base/gris-analysis/plotting/plotting.py -n 4 -o ctrl --bounds -850 450 --time_bounds 2008 3000 --no_legend --plot basin_flux_partitioning 2017_12_ctrl/basins/scalar/ts_b_*_ex_g900m_v3a_rcp_*_id_CTRL_0_2000.nc  2017_12_ctrl/basins/scalar/ts_b_*_ex_g3600m_v3a_rcp_*_id_NTRL_0_1000.nc 

# Plot fluxes for each basin
for rcp in 26 45 85; do
    ~/base/gris-analysis/plotting/plotting.py -o basins_rcp_${rcp}  --time_bounds 2008 3000 --no_legend --plot basin_mass 2017_12_ctrl/basins/scalar/ts_b_*_ex_g900m_v3a_rcp_${rcp}_id_CTRL_0_2000.nc
done

~/base/gris-analysis/plotting/plotting.py -o ctrl --time_bounds 2008 3000 --no_legend --plot station_usurf 2017_12_ctrl/station_ts/profile_g900m_v3a_rcp_*_id_CTRL_0_1000.nc

~/base/gris-analysis/plotting/plotting.py -o ctrl --time_bounds 2008 3000 --no_legend --plot per_basin_flux 2017_12_ctrl/basins/scalar/ts_b_*_ex_g900m_v3a_rcp_*_id_CTRL_0_2000.nc


# grid resolution
~/base/gris-analysis/plotting/plotting.py  -n 8 -o ctrl --time_bounds 2020 2200 --plot grid_res 2017_12_ctrl/scalar/ts_gris_g600m_v3a_rcp_*_id_CTRL_0_200.nc 2017_12_ctrl/scalar/ts_gris_g900m_v3a_rcp_*_id_CTRL_0_1000.nc 2017_12_ctrl/scalar/ts_gris_g1800m_v3a_rcp_*_id_CTRL_0_1000.nc 2017_12_ctrl/scalar/ts_gris_g3600m_v3a_rcp_*_id_CTRL_0_1000.nc 2017_12_ctrl/scalar/ts_gris_g4500m_v3a_rcp_*_id_CTRL_0_1000.nc 2017_12_ctrl/scalar/ts_gris_g9000m_v3a_rcp_*_id_CTRL_0_1000.nc 2017_12_ctrl/scalar/ts_gris_g18000m_v3a_rcp_*_id_CTRL_0_1000.nc




# NISO-CTRL
odir=2017_11_ctrl
grid=3600
mkdir -p $odir/niso
for rcp in 26 45 85; do
    cdo sub -selvar,topg $odir/state/gris_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_1000.nc -selvar,topg $odir/state/gris_g${grid}m_v3a_rcp_${rcp}_id_NISO_0_1000.nc $odir/niso/topg_CTRL_NISO_gris_g${grid}m_v3a_rcp_${rcp}_0_1000.nc
    gdal_translate $odir/niso/topg_CTRL_NISO_gris_g${grid}m_v3a_rcp_${rcp}_0_1000.nc $odir/niso/topg_CTRL_NISO_gris_g${grid}m_v3a_rcp_${rcp}_0_1000.tif
done

for rcp in 26 45 85; do
    ~/base/gris-analysis/plotting/plotting.py -o basins_rcp_${rcp} --time_bounds 2008 3000 --no_legend --plot basin_d 2017_11_ctrl/basins/scalar/ts_b_*_ex_g1800m_v3a_rcp_${rcp}_id_CTRL_0_1000.nc
done
~/base/gris-analysis/plotting/plotting.py -o ctrl --time_bounds 2008 3000 --no_legend --plot per_basin_flux 2017_12_ctrl/basins/scalar/ts_b_*_ex_g900m_v3a_rcp_*_id_CTRL_0_1000.nc

odir=2017_12_ctrl
grid=900
mkdir -p $odir/final_states
cd $odir/state
for file in gris_g${grid}m*0_1000.nc; do
    cdo aexpr,usurf=topg+thk -selvar,topg,thk,velsurf_mag $file ../final_states/$file
    ncap2 -O -s "where(topg<0) {topg=0.;}; where(thk<10) {velsurf_mag=-2e9; usurf=0.;};" ../final_states/$file ../final_states/$file
    gdal_translate NETCDF:../final_states/$file:velsurf_mag ../final_states/velsurf_mag_$file.tif
    gdal_translate -a_nodata 0 NETCDF:../final_states/$file:usurf ../final_states/usurf_$file.tif
    gdaldem hillshade ../final_states/usurf_$file.tif ../final_states/hs_usurf_$file.tif
    gdal_translate NETCDF:../final_states/$file:topg ../final_states/topg_$file.tif
    gdaldem hillshade ../final_states/topg_$file.tif ../final_states/hs_topg_$file.tif
done
cd ../../


odir=2017_12_ctrl
grid=900
mkdir -p $odir/spatial_processed
mkdir -p $odir/ice_extend
for rcp in 26 45 85; do
    cdo -L selvar,mask -selyear,2008,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000 $odir/spatial/ex_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc $odir/spatial_processed/ex_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc
    extract_interface.py -t grounding_line -o $odir/ice_extend/gl_ex_g900m_v3a_rcp_${rcp}_id_CTRL.shp $odir/spatial_processed/ex_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc
done


odir=2017_12_ctrl
grid=900
mkdir -p $odir/foo
for rcp in 26 45 85; do
    cdo selvar,mask -selyear,2008,2100,2200,2300,2400,2500 $odir/spatial/ex_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc $odir/foo/ex_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc
done


odir=2017_12_ctrl
grid=900
mkdir -p $odir/ice_extend
for rcp in 26 45 85; do
    extract_interface.py -t grounding_line -o $odir/ice_extend/gl_ex_g900m_v3a_rcp_${rcp}_id_CTRL.shp ${odir}/spatial/ex_g${grid}m_v3a_rcp_${rcp}_id_CTRL_0_3000.nc
done



odir=2017_12_ctrl
mkdir -p $odir/dgmsl
for rcp in 26 45 85; do
    for year in 2100 2200 2500 3000; do
        for run in NTRL; do
            
            cdo divc,365 -divc,1e15 -selvar,limnsw -sub -selyear,$year $odir/scalar/ts_gris_g3600m_v3a_rcp_${rcp}_id_${run}_0_1000.nc -selyear,2008 $odir/scalar/ts_gris_g3600m_v3a_rcp_${rcp}_id_${run}_0_1000.nc $odir/dgmsl/dgms_g3600m_rcp_${rcp}_${run}_${year}.nc
        done
    done
done

odir=2017_11_ctrl
mkdir -p $odir/dgmsl
for rcp in 26 45 85; do
    for year in 2100 2200 2500 3000; do
        for run in CTRL; do
            cdo divc,365 -divc,1e15 -selvar,limnsw -sub -selyear,$year $odir/scalar/ts_gris_g1800m_v3a_rcp_${rcp}_id_${run}_0_1000.nc -selyear,2008 $odir/scalar/ts_gris_g1800m_v3a_rcp_${rcp}_id_${run}_0_1000.nc $odir/dgmsl/dgms_g1800m_rcp_${rcp}_${run}_${year}.nc
        done
    done
done

odir=2017_12_ctrl
mkdir -p $odir/dgmsl
for rcp in 26 45 85; do
    for year in 2100 2200 2500 3000; do
        for run in CTRL; do
            cdo divc,365 -divc,1e15 -selvar,limnsw -sub -selyear,$year $odir/scalar/ts_gris_g900m_v3a_rcp_${rcp}_id_${run}_0_1000.nc -selyear,2008 $odir/scalar/ts_gris_g900m_v3a_rcp_${rcp}_id_${run}_0_1000.nc $odir/dgmsl/dgms_g900m_rcp_${rcp}_${run}_${year}.nc
        done
    done
done

odir=2017_12_les
grid=3600
mkdir -p $odir/sftgif
mkdir -p $odir/sftgif_pctl
cd $odir/state
for file in gris_g${grid}m*id_*0_1000.nc; do
    if [ ! -f "../sftgif/$file" ]; then
    cdo selvar,sftgif $file ../sftgif/$file
    fi
done
cd ../../
for rcp in 26 45 85; do
    cdo -O -P 12 enssum $odir/sftgif/gris_g${grid}m_v3a_rcp_${rcp}_id_*_0_1000.nc $odir/sftgif_pctl/sum_gris_g${grid}m_v3a_rcp_${rcp}_0_1000.nc
    cdo divc,9.89 $odir/sftgif_pctl/sum_gris_g${grid}m_v3a_rcp_${rcp}_0_1000.nc $odir/sftgif_pctl/percent_gris_g${grid}m_v3a_rcp_${rcp}_0_1000.nc
done 


