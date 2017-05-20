#!/usr/bin/env python3
#
#==============================================================================
# Copyright 2017 Marco Bellaccini - marco.bellaccini[at!]gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#==============================================================================

#==============================================================================
# iloChecker
#
# iloChecker is a script that helps you performing a bulk health check on a
# list of HP ProLiant servers by using their HP iLO
# (Hewlett Packard Integrated Lights-Out management).
# Give it a file with a list of systems as argument and it will 
# get all the dirty job done for you.
# NOTE:
# this script is only compatible with HP ProLiant iLO 4
# with firmware version >= 2.00
#
#==============================================================================

import argparse
import getpass
import requests
import json
from sys import exit

# iLO system class
class IloSys:
    # constructor
    def __init__(self, baseurl, username, password, verifyCert):
        # setup variables
        self.baseurl = baseurl
        self.username = username
        self.password = password
        self.verifyCert = verifyCert
        self.headers = {'Content-type': 'application/json'}
        # suppress warnings if certificate verification was disabled
        if verifyCert == False:
            requests.packages.urllib3.disable_warnings()
        # authenticate
        self.authenticate()
    
    # authentication method
    def authenticate(self):
        # prepare request body
        data = {"UserName": self.username, "Password": self.password}
        data_json = json.dumps(data)
        response = requests.post(self.baseurl + "/rest/v1/Sessions", headers=self.headers, data=data_json, verify=self.verifyCert)
        # check status code
        if response.status_code != 201:
            raise ValueError("Error authenticating")
        # get auth token
        self.token = response.headers['X-Auth-Token']
        # insert authentication token in the header
        self.headers['X-Auth-Token'] = self.token
        # get session url suffix
        self.sess_url = response.headers['Location']

    # obtain system status method
    def getstatus(self):
        # get system state
        response = requests.get(self.baseurl + "/rest/v1/Systems/1", headers=self.headers, verify=self.verifyCert)
        # check status code
        if response.status_code != 200:
            raise ValueError("Error getting system health")
        # parse json
        rjs = response.json()
        # get hostname
        self.hostname = rjs['HostCorrelation']['HostName']
        # get health
        self.health = rjs['Status']['Health']
        # get power status
        self.power = rjs['Power']

    # logout function
    def logout(self):
        # logout
        response = requests.delete(self.sess_url, headers=self.headers, verify=self.verifyCert)
        # check status code
        if response.status_code != 200:
            raise ValueError("Error logging out")
            
            

# parse command line arguments
parser = argparse.ArgumentParser(description=("Check health status of a list of systems through iLO"))
parser.add_argument("filename", type=str, help="list of iLO hostnames/ip")
parser.add_argument("-c", "--certs", action="store_true", help="verify https certificates")
args = parser.parse_args()

# read file
try:
    f = open(args.filename, "r")
    syslist = f.read().splitlines()
    f.close()
except IOError:
    exit("Error: cannot read \"" + args.filename + "\".")

# toss comment and empty lines
syslist = [nm for nm in syslist if ((not nm.startswith("#")) and nm.strip())]

# print warning if certificate validation is disabled
if not args.certs:
    print("Beware: certificate validation is disabled")
    
# get username
username = str(input("Enter iLO Username:"))

# get password
password = str(getpass.getpass("Enter iLO Password:"))

# iterate over list, getting and printing status
print("\nSYSTEMS SUMMARY:\n")
print("TARGET" + "\t\t" + "HOSTNAME" + "\t" + "HEALTH" + "\t" + "POWER")
healthc = 0
powerc = 0
for nm in syslist:
    try:
        cis = IloSys("https://" + nm, username, password, args.certs)
        cis.getstatus()
        cis.logout()
        if cis.health == "OK":
            healthc += 1
        if cis.power == "On":
            powerc += 1
        print(nm + "\t" + cis.hostname + "\t" + cis.health + "\t" + cis.power)
    except (ValueError, requests.exceptions.ConnectionError):
        print(nm + "\t" + "CONNECTION ERROR")

# print footer
sl = len(syslist)
print("\nScanned " + str(sl) + " system(s):")
print(str(healthc) + "/" + str(sl) + " healthy")
print(str(powerc) + "/" + str(sl) + " powered on")
