# Ham Radio program to monitor dx cluster spots
#
# Written by Gordon Macie N4LR 04-03-2012
# Convert to Python 3 06-13-2017
#
# Primary purpose to find new 6 meter grid squares
#
# Synopsis: terminal-based python telnet client
# Usage: ptelnet.py [hostname] [portnumber]
#


# prompt or save call to login in with before distributing
# band stuff.... get band, filter bands of choice
# only show 6 meter optional
# only show neededd grids optional
# format output
# create ini file to save settings
# load countries list
# load worked countries list
# crashes if internet conn lost.. auto restart
# save records to database
# reports on grids, etc  new grids time period
#



import time, sys 
from   telnetlib import Telnet
from   threading import *
from   scanner   import *
from decimal import Decimal
#from ConfigParser import SafeConfigParser

#parser = SafeConfigParser()
#parser.read('lrg.ini')

#print parser.get('user','grid')

# frequencies in kilocycles
ARRL_BAND_PLAN = (
    (Decimal('1800.0'),    Decimal('2000.0'),    '160m'),
    (Decimal('3500.0'),    Decimal('4000.0'),    '80m'),
    (Decimal('7000.0'),    Decimal('7300.0'),    '40m'),
    (Decimal('10100.0'),   Decimal('10150.0'),   '30m'),
    (Decimal('14000.0'),   Decimal('14350.0'),   '20m'),
    (Decimal('18068.0'),   Decimal('18168.0'),   '17m'),
    (Decimal('21000.0'),   Decimal('21450.0'),   '15m'),
    (Decimal('24890.0'),   Decimal('24990.0'),   '12m'),
    (Decimal('28000.0'),   Decimal('29700.0'),   '10m'),
    (Decimal('50000.0'),   Decimal('54000.0'),   '6m'),
)


""" example

CC11^10109.0^EI9JF^10-Apr-2012^0145^29 dB  25 WPM  CQ^KQ8M-30-#^0^5^SK1MMR^
27^14^8^4^^OH^EI^K^IO63^EN92^

"""

spotType           =  0
spotFreq           =  1
spotDXCall         =  2
spotDate           =  3
spotZulu           =  4
spotComment        =  5
spotSpotter        =  6
spotUnk1           =  7
spotUnk2           =  8
spotNode           =  9
spotDXITU          = 10
spotSpotterITU     = 11
spotDXCQ           = 12
spotSpotterCQ      = 13
spotDXState        = 14
spotSpotterState   = 15
spotDXCountry      = 16
spotSpotterCountry = 17
spotDXGrid         = 18
spotSpotterGrid    = 19
spotUnk4           = 20
spotUnk5           = 21
spotIPAddress      = 22
spotUnk6           = 23

#host = 'localhost'
#port = 7300
host = 'www.ve7cc.net'
port = 23
result = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
six_only = 'TRUE'
band_enabled = {'6m': 'TRUE', '10m': 'TRUE', '12m': 'TRUE','15m': 'FALSE'}
allFFMAGrids    = {}
confirmedStates = {}
workedGrids     = {}
dxcc6           = {}

of = open('c:\\python27\\stringsout.txt', 'w', 1)

class ReaderThread(Thread):
        def __init__(self, telnet):
            self.telnet = telnet
            Thread.__init__(self)
 
        def run(self):
            cc11count = 0
            global allFFMAGrids
            alertTag = ''
            while 1:
                ccStr_tmp = self.telnet.read_until(b"\n")
                ccStr = ccStr_tmp.decode()
                #of.write(ccStr)
                ccStr_first2 = ccStr[0:2]
                ccStr_first3 = ccStr[0:3]
                ccStr_first4 = ccStr[0:4]
                if ccStr_first2 == "To":
                    continue
                if ccStr_first3 == "WCY":
                    continue
                if ccStr_first3 == "WWV":
                    continue
                
                result = ccStr.split('^')
                if result[spotType] != "CC11":
                    print(ccStr)
                else:
                    cc11count = cc11count + 1
                    #print cc11count,
                    #print " " + ccStr
                    this_band = determine_band(result[spotFreq])
                    #print result[spotFreq] + " " + this_band + " " + result[spotZulu]
                    if this_band == '6m':
                        this_grid = result[spotDXGrid]
                        this_dxcc = result[spotDXCountry]
                        this_call = result[spotDXCall]
                        beacon    = this_call[-2:]
                        #print this_dxcc
                        of.write(ccStr)
                        #print this_grid
                        alertTag = ''
                        if this_dxcc in dxcc6:
                            if this_dxcc == "K":
                                pass
                            else:
                                if dxcc6[this_dxcc] == 'N':
                                    alertTag = "DXCC"
                                else:
                                    alertTag = ""
                        else:
                            if this_grid in workedGrids:
                                pass
                            else:
                                if this_grid in allFFMAGrids:
                                    alertTag = "FFMA"
                                else:
                                    alertTag = "NEW GRID"
                        if beacon == "/B":
                                alertTag = "BCN"
                                
                        #print ccStr
                        print("{:<9}".format(alertTag) + " " + \
                              "{:<6}".format(result[spotDXGrid]) + " " + \
                              "{:<2}".format(result[spotDXState]) + " " + \
                              "{:<12}".format(result[spotDXCall]) + " " + \
                              result[spotFreq] + " " + \
                              result[spotZulu] + " " + \
                              "{:<12}".format(result[spotSpotter]) + " " + \
                              "{:<2}".format(result[spotSpotterState])+ " " + \
                              result[spotComment])




                       
def determine_band(value, band_plan=ARRL_BAND_PLAN):
    value = Decimal(str(value))
    for band in band_plan:
        if value > band[0] and value < band[1]:
            return band[2]
    return '?'

def LoadWorkedGrids():
        
    global workedGrids
    with open("gridsworked.txt") as f:
        for line in f:
            (key, val) = line.split()
            workedGrids[key] = val
            #print key + " " + val
        print("Loading Worked Grids ")
        
        #for key in sorted(workedGrids.keys()):
        #  print key, workedGrids[key]

def LoadAllFFMAGrids():

    global allFFMAGrids
    with open("FFMADICT.TXT") as f:
        for line in f:
            (key, val) = line.split(" ")
            allFFMAGrids[key] = val
        print("Loading All FFMA Grids ")
        
        #for key in sorted(allFFMAGrids.keys()):
        #  print key, allFFMAGrids[key]


def Loaddxcc6():

    global dxcc6
    with open("dxcc6.txt") as dx6:
        for line in dx6:
            (key, val) = line.split(" ")
            dxcc6[key] = val
            #print key + " " + val
        print("Loading 6 Meter DXCC ")
        
        #for key in sorted(dxcc6.keys()):
        #  print key, dxcc6[key]

def LoadConfirmedStates():

    global confirmedStates
    with open("states.txt") as cs:
        for line in cs:
            (key, val) = line.split(" ")
            confirmedStates[key] = val
            #print key + " " + val
        print("Loading Confirmed States ")
        
        #for key in sorted(confirmedStates.keys()):
        #  print key, confirmedStates[key] 


def main(host, port):

    Loaddxcc6()
    LoadWorkedGrids()
    LoadConfirmedStates()
    LoadAllFFMAGrids()
    
    telnet = Telnet()
    telnet.open(host, port)
 
    reader = ReaderThread(telnet)
    reader.start()
    telnet.write(b"N4LR\n")
    telnet.write(b"set/filter dxbm/pass 6\n")
    telnet.write(b"set/ve7cc\n")
    telnet.write(b"set/skimmer\n")
    
    
    
      
    while 1:
        # read a line and parse  
        if not reader.isAlive(): break
    telnet.close()
 
if __name__ == '__main__':
    
    try:
        host = sys.argv[1]
    except: pass

    try:
        port = int(sys.argv[2])
    except: pass
    main(host, port)
