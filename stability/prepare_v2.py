#!/usr/bin/env python
# Copyright (C) 2016-17 Andy Aschwanden

import itertools
from collections import OrderedDict
import os
try:
    import subprocess32 as sub
except:
    import subprocess as sub
from argparse import ArgumentParser
import sys
sys.path.append('../resources/')
from resources import *

grid_choices = [18000, 9000, 6000, 4500, 3600, 3000, 2400, 1800, 1500, 1200, 900, 600, 450, 300, 150]

# set up the option parser
parser = ArgumentParser()
parser.description = "Generating scripts for warming experiments."
parser.add_argument("FILE", nargs=1,
                    help="Input file to restart from", default=None)
parser.add_argument("-n", '--n_procs', dest="n", type=int,
                    help='''number of cores/processors. default=140.''', default=140)
parser.add_argument("-w", '--wall_time', dest="walltime",
                    help='''walltime. default: 100:00:00.''', default="100:00:00")
parser.add_argument("-q", '--queue', dest="queue", choices=list_queues(),
                    help='''queue. default=long.''', default='long')
parser.add_argument("--climate", dest="climate",
                    choices=['flux'],
                    help="Climate", default='flux')
parser.add_argument("--calving", dest="calving",
                    choices=['float_kill', 'ocean_kill', 'eigen_calving', 'thickness_calving', 'vonmises_calving', 'hybrid_calving'],
                    help="calving", default='ocean_kill')
parser.add_argument("--ocean", dest="ocean",
                    choices=['warming'],
                    help="Ocean coupler", default='const')
parser.add_argument("--ocean_melt", dest="ocean_melt",
                    choices=['x', '10myr_latitudinal', '20myr_latitudinal'],
                    help="Ocean melt type", default='20myr_latitudinal')
parser.add_argument("-d", "--domain", dest="domain",
                    choices=['gris', 'gris_ext'],
                    help="sets the modeling domain", default='gris')
parser.add_argument("--exstep", dest="exstep", type=int,
                    help="Writing interval for spatial time series", default=10)
parser.add_argument("-f", "--o_format", dest="oformat",
                    choices=['netcdf3', 'netcdf4_parallel', 'pnetcdf'],
                    help="output format", default='netcdf4_parallel')
parser.add_argument("-g", "--grid", dest="grid", type=int,
                    choices=grid_choices,
                    help="horizontal grid resolution", default=9000)
parser.add_argument("--o_dir", dest="odir",
                    help="output directory. Default: current directory", default='foo')
parser.add_argument("--o_size", dest="osize",
                    choices=['small', 'medium', 'big', 'big_2d'],
                    help="output size type", default='medium')
parser.add_argument("-s", "--system", dest="system",
                    choices=list_systems(),
                    help="computer system to use.", default='pleiades_broadwell')
parser.add_argument("-b", "--bed_type", dest="bed_type",
                    choices=list_bed_types(),
                    help="output size type", default='ctrl')
parser.add_argument("--bed_deformation", dest="bed_deformation",
                    choices=['off', 'lc', 'iso'],
                    help="Bed deformation model.", default='off')
parser.add_argument("--frontal_melt", dest="frontal_melt", action="store_true",
                    help="Turn on frontal melt", default=False)
parser.add_argument("--forcing_type", dest="forcing_type",
                    choices=['ctrl', 'e_age'],
                    help="output size type", default='ctrl')
parser.add_argument("--hydrology", dest="hydrology",
                    choices=['null', 'diffuse', 'routing'],
                    help="Basal hydrology model.", default='diffuse')
parser.add_argument("-p", "--params", dest="params_list",
                    help="Comma-separated list with params for sensitivity", default=None)
parser.add_argument("--precip", dest="precip",
                    choices=['racmo', 'hirham'],
                    help="Precipitation model", default='racmo')
parser.add_argument("--stable_gl", dest="float_kill_calve_near_grounding_line", action="store_true",
                    help="Stable grounding line", default=False)
parser.add_argument("--stress_balance", dest="stress_balance",
                    choices=['sia', 'ssa+sia', 'ssa'],
                    help="stress balance solver", default='ssa+sia')
parser.add_argument("--dataset_version", dest="version",
                    choices=['2', '3'],
                    help="input data set version", default='2')
parser.add_argument("--vertical_velocity_approximation", dest="vertical_velocity_approximation",
                    choices=['centered', 'upstream'],
                    help="How to approximate vertical velocities", default='upstream')
parser.add_argument("--start_year", dest="start_year", type=int,
                    help="Simulation start year", default=0)
parser.add_argument("--end_year", dest="end_year", type=int,
                    help="Simulation end year", default=100)


options = parser.parse_args()

nn = options.n
odir = options.odir
oformat = options.oformat
osize = options.osize
queue = options.queue
walltime = options.walltime
system = options.system

bed_deformation = options.bed_deformation
bed_type = options.bed_type
calving = options.calving
climate = options.climate
exstep = options.exstep
float_kill_calve_near_grounding_line = options.float_kill_calve_near_grounding_line
forcing_type = options.forcing_type
frontal_melt = options.frontal_melt
grid = options.grid
hydrology = options.hydrology
ocean = options.ocean
ocean_melt = options.ocean_melt
precip = options.precip
stress_balance = options.stress_balance
vertical_velocity_approximation = options.vertical_velocity_approximation
version = options.version

# Check which parameters are used for sensitivity study
params_list = options.params_list

domain = options.domain
pism_exec = generate_domain(domain)

if options.FILE is None:
    print('Missing input file')
    import sys
    sys.exit()
else:
    input_file = options.FILE[0]

if domain.lower() in ('greenland_ext', 'gris_ext'):
    pism_dataname = '../data_sets/bed_dem/pism_Greenland_ext_{}m_mcb_jpl_v{}_{}.nc'.format(grid, version, bed_type)
else:
    pism_dataname = '../data_sets/bed_dem/pism_Greenland_{}m_mcb_jpl_v{}_{}.nc'.format(grid, version, bed_type)
if precip in ('racmo'):
    precip_file = pism_dataname
elif precip in ('hirham'):
    precip_file = 'DMI-HIRHAM5_GL2_ERAI_1980_2014_PR_TM_EPSG3413_{}m.nc'.format(grid)
else:
    print(('Precip model {} not support. How did we get here?'.format(precip)))

if ocean_melt in ('x'):
    ocean_file = 'ocean_forcing_latitudinal_ctrl.nc'
elif ocean_melt in ('20myr_latitudinal'):
    ocean_file = 'ocean_forcing_latitudinal_20myr_80n.nc'    
else:
    ocean_file = 'ocean_forcing_latitudinal_80n.nc'
    

regridvars = 'litho_temp,enthalpy,age,tillwat,bmelt,Href,thk'

    
pism_config = 'init_config'
pism_config_nc = '.'.join([pism_config, 'nc'])
pism_config_cdl = os.path.join('../config', '.'.join([pism_config, 'cdl']))
# Anaconda libssl problem on chinook
if system in ('chinook'):
    ncgen = '/usr/bin/ncgen'
else:
    ncgen = 'ncgen'
cmd = [ncgen, '-o',
       pism_config_nc, pism_config_cdl]
sub.call(cmd)
if not os.path.isdir(odir):
    os.mkdir(odir)

state_dir = 'state'
scalar_dir = 'scalar'
spatial_dir = 'spatial'
snap_dir = 'snap'
for tsdir in (scalar_dir, spatial_dir, snap_dir, state_dir):
    if not os.path.isdir(os.path.join(odir, tsdir)):
        os.mkdir(os.path.join(odir, tsdir))
odir_tmp = '_'.join([odir, 'tmp'])
if not os.path.isdir(odir_tmp):
    os.mkdir(odir_tmp)

# ########################################################
# set up model initialization
# ########################################################

sia_e = (1.25)
ssa_n = (3.25)
ssa_e = (1.0)


thickness_calving_threshold_vales = [100]
ppq_values = [0.6]
tefo_values = [0.020]
phi_min_values = [5.0]
phi_max_values = [40.]
topg_min_values = [-700]
topg_max_values = [700]
combinations = list(itertools.product(ppq_values,
                                      tefo_values,
                                      phi_min_values,
                                      phi_max_values,
                                      topg_min_values,
                                      topg_max_values))


tsstep = 'yearly'

scripts = []
scripts_post = []

simulation_start_year = options.start_year
simulation_end_year = options.end_year

for n, combination in enumerate(combinations):

    ppq, tefo, phi_min, phi_max, topg_min, topg_max = combination

    ttphi = '{},{},{},{}'.format(phi_min, phi_max, topg_min, topg_max)

    name_options = OrderedDict()
    name_options['calving'] = calving
    if calving in ('thickness_calving', 'eigen_calving', 'vonmises_calving', 'hybrid_calving'):
        name_options['threshold'] = thickness_calving_threshold
    if calving in ('eigen_calving', 'hybrid_calving'):
        name_options['k'] = eigen_calving_k
    
    vversion = 'v' + str(version)
    full_exp_name =  '_'.join([climate, vversion, bed_type, '_'.join(['_'.join([k, str(v)]) for k, v in list(name_options.items())])])
    full_outfile = '{domain}_g{grid}m_{experiment}.nc'.format(domain=domain.lower(), grid=grid, experiment=full_exp_name)
    # All runs in one script file for coarse grids that fit into max walltime
    script = 'prep_{}_g{}m_{}.sh'.format(domain.lower(), grid, full_exp_name)
    with open(script, 'w') as f:

        start = simulation_start_year
        end = simulation_end_year

        experiment =  '_'.join([climate, vversion, bed_type, '_'.join(['_'.join([k, str(v)]) for k, v in list(name_options.items())]), '{}'.format(start), '{}'.format(end)])

        for filename in (script):
            try:
                os.remove(filename)
            except OSError:
                pass

        batch_header, batch_system = make_batch_header(system, nn, walltime, queue)
        f.write(batch_header)

        with open(script, 'w') as f:

            f.write(batch_header)

            outfile = '{domain}_g{grid}m_{experiment}.nc'.format(domain=domain.lower(),grid=grid, experiment=experiment)

            prefix = generate_prefix_str(pism_exec)

            general_params_dict = OrderedDict()
            general_params_dict['bootstrap'] = ''
            general_params_dict['i'] = pism_dataname
            general_params_dict['regrid_file'] = input_file
            general_params_dict['regrid_vars'] = regridvars
            general_params_dict['regrid_special'] = ''
            general_params_dict['ys'] = start
            general_params_dict['ye'] = end
            general_params_dict['o'] = os.path.join(odir, state_dir, outfile)
            general_params_dict['o_format'] = oformat
            general_params_dict['o_size'] = osize
            general_params_dict['config_override'] = pism_config_nc
            general_params_dict['backup_interval'] = 100
            if bed_deformation not in ('off'):
                general_params_dict['bed_def'] = bed_deformation
            if forcing_type in ('e_age'):
                general_params_dict['e_age_coupling'] = ''

            grid_params_dict = generate_grid_description(grid, domain)

            sb_params_dict = OrderedDict()
            sb_params_dict['sia_e'] = sia_e
            sb_params_dict['ssa_e'] = ssa_e
            sb_params_dict['ssa_n'] = ssa_n
            sb_params_dict['pseudo_plastic_q'] = ppq
            sb_params_dict['till_effective_fraction_overburden'] = tefo
            if start == simulation_start_year:
                sb_params_dict['topg_to_phi'] = ttphi
            sb_params_dict['vertical_velocity_approximation'] = vertical_velocity_approximation

            stress_balance_params_dict = generate_stress_balance(stress_balance, sb_params_dict)
            ice_density = 910.
            climate_params_dict = generate_climate(climate,
                                                   force_to_thickness_file=pism_dataname)
            ocean_params_dict = generate_ocean(ocean,
                                               ocean_given_file=ocean_file)
            hydro_params_dict = generate_hydrology(hydrology)
            if start == simulation_start_year:
                calving_params_dict = generate_calving(calving,
                                                       float_kill_calve_near_grounding_line=float_kill_calve_near_grounding_line,
                                                       ocean_kill_file=pism_dataname,
                                                       frontal_melt=frontal_melt)
            else:
                calving_params_dict = generate_calving(calving,
                                                       float_kill_calve_near_grounding_line=float_kill_calve_near_grounding_line,
                                                       ocean_kill_file=regridfile,
                                                       frontal_melt=frontal_melt)

            exvars = default_spatial_ts_vars()
            spatial_ts_dict = generate_spatial_ts(full_outfile, exvars, exstep, odir=odir_tmp, split=True)
            scalar_ts_dict = generate_scalar_ts(outfile, tsstep,
                                                start=simulation_start_year,
                                                end=simulation_end_year,
                                                odir=os.path.join(odir, scalar_dir))

            all_params_dict = merge_dicts(general_params_dict,
                                          grid_params_dict,
                                          stress_balance_params_dict,
                                          climate_params_dict,
                                          ocean_params_dict,
                                          hydro_params_dict,
                                          calving_params_dict,
                                          spatial_ts_dict,
                                          scalar_ts_dict)
            all_params = ' '.join([' '.join(['-' + k, str(v)]) for k, v in list(all_params_dict.items())])

            if system in ('debug'):
                cmd = ' '.join([batch_system['mpido'], prefix, all_params, '2>&1 | tee {outdir}/job.${batch}'.format(outdir=odir, batch=batch_system['job_id'])])
            else:
                cmd = ' '.join([batch_system['mpido'], prefix, all_params, '> {outdir}/job.${batch}  2>&1'.format(outdir=odir, batch=batch_system['job_id'])])


            f.write(cmd)
            f.write('\n\n')


    script_post = 'prep_{}_g{}m_{}_post.sh'.format(domain.lower(), grid, full_exp_name)
    scripts_post.append(script_post)

    post_header = make_batch_post_header(system)

    with open(script_post, 'w') as f:

        f.write(post_header)

        extra_file = spatial_ts_dict['extra_file']
        myfiles = ' '.join(['{}_{}.000.nc'.format(extra_file, k) for k in range(simulation_start_year+exstep, simulation_end_year, exstep)])
        myoutfile = extra_file + '.nc'
        myoutfile = os.path.join(odir, spatial_dir, os.path.split(myoutfile)[-1])
        cmd = ' '.join(['ncrcat -O -6 -h', myfiles, myoutfile, '\n'])
        f.write(cmd)

    
scripts = uniquify_list(scripts)
scripts_post = uniquify_list(scripts_post)
print('\n'.join([script for script in scripts]))
print('\nwritten\n')
print('\n'.join([script for script in scripts_post]))
print('\nwritten\n')

