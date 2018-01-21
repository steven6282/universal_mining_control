import json
import requests
import os

class Nicehash:
    conf = {}
    region = ""
    conf_file = os.path.join( '.', 'pools', 'Nicehash.conf' )
    api_url = 'https://api.nicehash.com/api?method='
    def __init__( self ):
        self.conf = json.load( open( self.conf_file ) )
        self.region = self.conf["default_region"]
        if not len( self.conf['algos'] ):
            self.updateAlgos()

    def apiRequest( self, requestString ):
        #add api caching here with a time limit before making another actual request
        response = requests.post( self.api_url + requestString )
        return response.json()

    #Finds the most profitable algo in the given algoList.  If no list provided, will use all enabled algos for the pool.
    #this needs a way to factor in the benchmarked GPU hash rates, which could be different per GPU.. perhaps a single call for each GPU then group GPUs by results?
    #if no hashrate provided it will just default to the most profitable pool
    def getAlgo( self, algoList=[], hashrate=1 ):
        newAlgo = ''
        if not len( algoList ) :
            algoList = self.conf[ 'algos' ]

        #will need to query api data, it should be cached to not query multiple times in rapid succession
        #maybe store in the conf file the api cache time
        if len( algoList ) > 0:
            for algo in algoList:
                if algo in self.conf[ 'algos' ] and self.conf[ 'algos' ][ algo ][ 'enabled' ]:
                    #check profitability
                    newAlgo = algo
                    break
        return newAlgo

    def getUrl( self, algo ):
        return "stratum+tcp://" + algo + "." + self.region + ".nicehash.com:" + str( self.conf["algos"][algo]["port"] )

    def getUser( self ):
        return self.conf[ 'user' ]

    def setUser( self, userString ):
        self.conf[ 'user' ] = userString
        self.writeConf()

    def updateAlgos( self ):
        #get algo list using simplemultialgo api method
        for algoInfo in self.apiRequest( 'simplemultialgo.info' )[ 'result' ][ 'simplemultialgo' ]:
            enabled = 1
            if algoInfo['name'] in self.conf['algos']:
                enabled = self.conf['algos'][ algoInfo['name'] ][ 'enabled' ]
            self.conf['algos'][algoInfo['name']] = { 'enabled': enabled, 'port': algoInfo['port'], 'algo': algoInfo['algo'] }
        self.writeConf()
    
    def writeConf( self ):
        with open( self.conf_file, 'w' ) as confFile:
            confFile.write( json.dumps( self.conf, indent=4 ) )