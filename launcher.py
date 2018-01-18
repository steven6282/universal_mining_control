import subprocess
import time
import json
from pprint import pprint
import platform
import common
import os
import sys
import importlib
import inspect

#load pools dynamically from ./pools/
pools = []
for f in os.listdir( './pools' ):
    if os.path.isfile( './pools/' + f ):
        if ( f.endswith( '.py' ) or f.endswith( '.pyc' ) ) and not f.startswith( '__' ):
            mod = importlib.import_module( 'pools.' + f[:f.rfind( '.py' )] )
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass( obj ):
                    pools.append( getattr( mod, name )() )

#print( pools[0].__class__.__name__ )

system = platform.system()

conf = json.load( open( ".\conf\general_settings.conf" ) )
#pool_conf = json.load( open( ".\conf\pools.conf" ) )
miner_conf = json.load( open( ".\conf\miners.conf" ) )
system_algos = miner_conf[ system ]
#need a conf file for GPUs, store the gpus found in the system
# flag for enabled / disabled
# benchmarks
# settings that override pool and general settings

#make pool specific python files that get included with a specific expected function list to call
# for things like balance retrieval and such that will be different for each pool
# (script) setting in pools.conf
# also could consider redoing pools.conf to be loaded by the script instead of here, only the pool name
#  need to be specified in the general_settings (name of script would have to match in pools folder)
# need to figure out a way to incoporate region into the pool and allow auto switching region if one is down
# maybe make pool script responsible for more and have a function that returns the URL, it's internal script decides

#need to make this auto select algo
#get algo list from system_algos, and makesure it exists in pool_conf algos.
#use stratum_urls or maybe have a supported_algos array??
pool = pools[0]
for _pool in pools:
    if _pool.__class__.__name__ == conf[ 'pool' ]:
        pool = _pool

#if pool.getUser() == '':
#    pool.setUser( conf[ 'address' ] + '.' + conf[ 'workerName' ] )

current_algo = pool.getAlgo( system_algos )

#address and workername are in general_settings but can be overridden in pool
#probably expand this with a function to allow any setting in general to be overridden per pool?
#address = conf["address"] if pool["address"] == "" else pool["address"]
#workerName = conf["workerName"] if pool["workerName"] == "" else pool["workerName"]


algo_settings = system_algos[ current_algo ]
args = algo_settings[ "args" ]

for shared_args in system_algos[ 'shared_args' ]:
    if current_algo in shared_args[ 'algos' ]:
        args = { **shared_args[ 'args' ], **args }

#pool miner_args overrule miner args
#might need a way to do system specific pool miner args?
#if 'miner_args' in pool[ 'algos' ][ current_algo ]:
#    args = { **args, **pool[ 'algos' ][ current_algo ][ 'miner_args' ] }

for arg in args:
    if type( args[arg] ) is str:
        vars = args[arg].split( '%' )
        if len( vars ) > 1:
            parsedValue = ''
            for var in vars:
                if var != '':
                    try:
                        #pool_stratum_url = pool[ 'algos' ][ algo ][ 'stratum_url' ]
                        eVar = eval( var )
                        parsedValue += eVar
                    except:
                        parsedValue += var
            args[arg] = parsedValue
    else:
        args[arg] = str( args[ arg ] )

launch_args = [ algo_settings[ 'path' ] ]
for arg in args:
    launch_args += [ arg, args[ arg ] ]
pprint( launch_args )

#proc = subprocess.Popen( launch_args, shell=False, creationflags=subprocess.CREATE_NEW_CONSOLE )

#add timers for checking for things, updating gpu temps, checking for more profitable aglo, recording rates etc.
while True:
    if proc.poll() is not None:
        print( 'Process appears to have died' )
        break

if proc.poll() is not None:
    proc.kill()

'''
proc = subprocess.Popen( args, shell=False, creationflags=subprocess.CREATE_NEW_CONSOLE )

elapsed = 0
start = time.time()
while elapsed < 30:
    time.sleep(5)
    elapsed = time.time() - start
    print( int( elapsed ) )
    if proc.poll() is not None:
        print( 'Process appears to have died' )
        break

if proc.poll() is not None:
    proc.kill()

'''