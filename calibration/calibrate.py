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
                    choices=['float_kill', 'eigen_calving', 'vonmises_calving', 'hybrid_calving'],
                    help="calving", default='vonmises_calving')
parser.add_argument("-d", "--domain", dest="domain",
                    choices=['gris', 'gris_ext'],
                    help="sets the modeling domain", default='gris')
parser.add_argument("-f", "--o_format", dest="oformat",
                    choices=['netcdf3', 'netcdf4_parallel', 'pnetcdf'],
                    help="output format", default='netcdf4_parallel')
parser.add_argument("-g", "--grid", dest="grid", type=int,
                    choices=grid_choices,
                    help="horizontal grid resolution", default=1500)
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
                    help="output size type", default='no_bath')
parser.add_argument("--frontal_melt", dest="frontal_melt", action="store_true",
                    help="Turn on frontal melt", default=False)
parser.add_argument("--hydrology", dest="hydrology",
                    choices=['null', 'diffuse', 'routing'],
                    help="Basal hydrology model.", default='diffuse')
parser.add_argument("-p", "--params", dest="params_list",
                    help="Comma-separated list with params for sensitivity", default=None)
parser.add_argument("--stress_balance", dest="stress_balance",
                    choices=['sia', 'ssa+sia', 'ssa'],
                    help="stress balance solver", default='ssa+sia')
parser.add_argument("--dataset_version", dest="version",
                    choices=['2', '3', '3a'],
                    help="input data set version", default='3a')
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

bed_type = options.bed_type
calving = options.calving
climate = options.climate
climate_relax = 'pdd'

grid = options.grid
hydrology = options.hydrology
ocean = 'const'
stress_balance = options.stress_balance
vertical_velocity_approximation = options.vertical_velocity_approximation
version = options.version

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
    
climate_file = '../data_sets/climate_forcing/DMI-HIRHAM5_GL2_ERAI_2001_2014_YDM_BIL_EPSG3413_{}m.nc'.format(grid)    

regridvars = 'litho_temp,enthalpy,age,tillwat,bmelt,Href,thk'

pism_config = 'init_config'
pism_config_nc = '.'.join([pism_config, 'nc'])
pism_config_cdl = os.path.join('../config', '.'.join([pism_config, 'cdl']))
ncgen = 'ncgen'
cmd = [ncgen, '-o',
       pism_config_nc, pism_config_cdl]
sub.call(cmd)
if not os.path.isdir(odir):
    os.mkdir(odir)

state_dir = 'state'
scalar_dir = 'scalar'
for tsdir in (scalar_dir, state_dir):
    if not os.path.isdir(os.path.join(odir, tsdir)):
        os.mkdir(os.path.join(odir, tsdir))
odir_tmp = '_'.join([odir, 'tmp'])
if not os.path.isdir(odir_tmp):
    os.mkdir(odir_tmp)


# ########################################################
# set up model initialization
# ########################################################

fsnow = 4
fice = 8
ssa_e = 1

sia_e_values = [1.25]
sia_n_values = [3]
ssa_n_values = [3.25]
ppq_values = [0.3, 0.6, 0.9]
tefo_values = [0.020]

phi_min_values = [5.0]
phi_max_values = [40.]
topg_min_values = [-700]
topg_max_values = [700]
combinations = list(itertools.product(sia_e_values,
                                      sia_n_values,
                                      ssa_n_values,
                                      ppq_values,
                                      tefo_values,
                                      phi_min_values,
                                      phi_max_values,
                                      topg_min_values,
                                      topg_max_values))


tsstep = 'yearly'

scripts = []

simulation_start_year = options.start_year
simulation_end_year = options.end_year

for n, combination in enumerate(combinations):

    sia_e, sia_n, ssa_n, ppq, tefo, phi_min, phi_max, topg_min, topg_max = combination

    ttphi = '{},{},{},{}'.format(phi_min, phi_max, topg_min, topg_max)

    name_options = OrderedDict()
    name_options['sia_e'] = sia_e
    name_options['sia_n'] = sia_n
    name_options['ssa_n'] = ssa_n
    name_options['ppq'] = ppq
    name_options['tefo'] = tefo
    name_options['calving'] = calving
    if calving in ('eigen_calving', 'hybrid_calving'):
        name_options['k'] = eigen_calving_k
        
    vversion = 'v' + str(version)
    full_exp_name =  '_'.join([climate, vversion, bed_type, '_'.join(['_'.join([k, str(v)]) for k, v in list(name_options.items())])])
    full_outfile = '{domain}_g{grid}m_{experiment}.nc'.format(domain=domain.lower(), grid=grid, experiment=full_exp_name)
    full_exp_name_relax =  '_'.join([climate_relax, vversion, bed_type, '_'.join(['_'.join([k, str(v)]) for k, v in list(name_options.items())])])
    full_outfile_relax = '{domain}_g{grid}m_{experiment}.nc'.format(domain=domain.lower(), grid=grid, experiment=full_exp_name_relax)
    
    # All runs in one script file for coarse grids that fit into max walltime
    script = 'calib_{}_g{}m_{}.sh'.format(domain.lower(), grid, full_exp_name)
    for filename in (script):
        try:
            os.remove(filename)
        except OSError:
            pass
    with open(script, 'w') as f:

        start = simulation_start_year
        end = simulation_end_year

        experiment =  '_'.join([climate, vversion, bed_type, '_'.join(['_'.join([k, str(v)]) for k, v in list(name_options.items())]), '{}'.format(start), '{}'.format(end)])

        batch_header, batch_system = make_batch_header(system, nn, walltime, queue)
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
            
        grid_params_dict = generate_grid_description(grid, domain)

        sb_params_dict = OrderedDict()
        sb_params_dict['sia_e'] = sia_e
        sb_params_dict['sia_n'] = sia_n
        sb_params_dict['ssa_e'] = ssa_e
        sb_params_dict['ssa_n'] = ssa_n
        sb_params_dict['pseudo_plastic_q'] = ppq
        sb_params_dict['till_effective_fraction_overburden'] = tefo
        sb_params_dict['topg_to_phi'] = ttphi
        sb_params_dict['vertical_velocity_approximation'] = vertical_velocity_approximation
            
        stress_balance_params_dict = generate_stress_balance(stress_balance, sb_params_dict)
        ice_density = 910.
        climate_params_dict = generate_climate(climate,
                                               force_to_thickness_file=pism_dataname)
        ocean_params_dict = generate_ocean(ocean)
        hydro_params_dict = generate_hydrology(hydrology)
        calving_params_dict = generate_calving(calving + ',ocean_kill',
                                               ocean_kill_file=pism_dataname)
            
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
                                      scalar_ts_dict)
        
        # Remove flow law so this works with different SIA N
        if 'sia_flow_law' in all_params_dict:
            del all_params_dict['sia_flow_law']
        all_params = ' '.join([' '.join(['-' + k, str(v)]) for k, v in list(all_params_dict.items())])

        
        if system in ('debug'):
            cmd = ' '.join([batch_system['mpido'], prefix, all_params, '2>&1 | tee {outdir}/job_1.${batch}'.format(outdir=odir, batch=batch_system['job_id'])])
        else:
            cmd = ' '.join([batch_system['mpido'], prefix, all_params, '> {outdir}/job_1.${batch}  2>&1'.format(outdir=odir, batch=batch_system['job_id'])])

        f.write(cmd)
        f.write('\n\n')

        infile = os.path.join(odir, state_dir, outfile)

        relax_start = 0
        relax_end = 25
        experiment =  '_'.join([climate_relax, vversion, bed_type, '_'.join(['_'.join([k, str(v)]) for k, v in list(name_options.items())]), '{}'.format(relax_start), '{}'.format(relax_end)])

        outfile = '{domain}_g{grid}m_{experiment}.nc'.format(domain=domain.lower(),grid=grid, experiment=experiment)
        general_params_dict = OrderedDict()
        general_params_dict['i'] = infile
        general_params_dict['ys'] = relax_start
        general_params_dict['ye'] = relax_end
        general_params_dict['o'] = os.path.join(odir, state_dir, outfile)
        general_params_dict['o_format'] = oformat
        general_params_dict['o_size'] = osize
        general_params_dict['config_override'] = pism_config_nc
        general_params_dict['backup_interval'] = 100
            
        grid_params_dict = generate_grid_description(grid, domain)
        
        sb_params_dict = OrderedDict()
        sb_params_dict['sia_e'] = sia_e
        sb_params_dict['sia_n'] = sia_n
        sb_params_dict['ssa_e'] = ssa_e
        sb_params_dict['ssa_n'] = ssa_n
        sb_params_dict['pseudo_plastic_q'] = ppq
        sb_params_dict['till_effective_fraction_overburden'] = tefo
        sb_params_dict['topg_to_phi'] = ttphi
        sb_params_dict['vertical_velocity_approximation'] = vertical_velocity_approximation

        stress_balance_params_dict = generate_stress_balance(stress_balance, sb_params_dict)
        ice_density = 910.
        climate_params_dict = generate_climate(climate_relax,
                                               **{'surface.pdd.factor_ice': (fice / ice_density),
                                                  'surface.pdd.factor_snow': (fsnow / ice_density),
                                                  'atmosphere_given_file': climate_file,
                                                  'atmosphere_given_period': 1})
        ocean_params_dict = generate_ocean(ocean,
                                           ocean_given_file=ocean_file)
        hydro_params_dict = generate_hydrology(hydrology)
        calving_params_dict = generate_calving(calving + ',ocean_kill',
                                               ocean_kill_file=pism_dataname)


        exvars = default_spatial_ts_vars()
        spatial_ts_dict = generate_spatial_ts(full_outfile_relax, exvars, 1, odir=odir_tmp, split=True)

        all_params_dict = merge_dicts(general_params_dict,
                                      grid_params_dict,
                                      stress_balance_params_dict,
                                      climate_params_dict,
                                      ocean_params_dict,
                                      hydro_params_dict,
                                      calving_params_dict,
                                      spatial_ts_dict)
        if 'sia_flow_law' in all_params_dict:
            del all_params_dict['sia_flow_law']
        all_params = ' '.join([' '.join(['-' + k, str(v)]) for k, v in list(all_params_dict.items())])

        if system in ('debug'):
            cmd = ' '.join([batch_system['mpido'], prefix, all_params, '2>&1 | tee {outdir}/job_2.${batch}'.format(outdir=odir, batch=batch_system['job_id'])])
        else:
            cmd = ' '.join([batch_system['mpido'], prefix, all_params, '> {outdir}/job_2.${batch}  2>&1'.format(outdir=odir, batch=batch_system['job_id'])])


        f.write(cmd)

        f.write('\n\n')

        scripts.append(script)

scripts = uniquify_list(scripts)
print('\n'.join([script for script in scripts]))
print('\nwritten\n')

