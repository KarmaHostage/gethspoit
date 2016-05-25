#!/usr/bin/env python
import subprocess
import yaml
import ipaddr
import telnetlib
import socket;
import os;
import time
import signal

GETH_PROCESS_ID = None

def connectToRpc(theIp):
    print("-----> connecting to: " + theIp)
    with open("possible_vulnerables.txt", "a") as myfile:
        myfile.write(theIp + "\n")

def startEnumerating(execOutput):

    data = yaml.load(execOutput)
    peers = data["peers"]

    for i, val in enumerate(peers):
        networkAddresses = val["network"]
        name = val["name"]
        print("testing.. " + networkAddresses["remoteAddress"] + " with version: " + name)
        ip, separator, port =  networkAddresses["remoteAddress"].rpartition(':')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        if "go" in name:
            print "Found: go service"
            result = sock.connect_ex((ip, 8545))
        if "rust" in name:
            print "Found: rust service"
            result = sock.connect_ex((ip, 8545))
        elif "python" in name:
            print "Found: python service! Default rpc should be on!"
            result = sock.connect_ex((ip, 4000))
        else:
            result = 1

        if result == 0:
            connectToRpc(ip)
        else:
            print "client's port was closed or firewalled"

    if(GETH_PROCESS_ID != None):
        print "killing geth process"
        os.kill(GETH_PROCESS_ID, signal.SIGTERM)
        time.sleep(5)
        initialize()



def initialize():
    adminProcess = subprocess.Popen("geth --exec admin attach", stdout=subprocess.PIPE, shell=True)
    (execOutput, error) = adminProcess.communicate()

    if "Fatal" in execOutput:
        print "Trying to restart the ethereum node..."
        FNULL = open(os.devnull, 'w')
        gethProcess = subprocess.Popen("geth", stdout=FNULL, stderr=subprocess.STDOUT)
        global GETH_PROCESS_ID
        GETH_PROCESS_ID = gethProcess.pid
        print("starting under the pid: (and waiting 60 secs to populate peers) ", gethProcess.pid)
        time.sleep(60)
        initialize()
    else:
        print "starting to enumerate"
        startEnumerating(execOutput)

initialize()
