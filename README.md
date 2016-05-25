Gethsploit
====

gethsploit is a set of python scripts to enumerate ethereum peers which have rpc-ports enabled.

##Prerequisites

Make sure you have geth installed, preferably the latest version, which has some fixes concerning attaching to other rpc-instances.

##Using Gethsploit

Make sure geth is not running, or getsploit will only run once. 

getsploit iterates until cancelled.

- starts up geth
- waits 60 seconds to populate peers
- enumerates peers and extracts running version
- probes the peer to see if the RPC-instance is running
- kills geth

```
./getsploit
```

##Using Nodesploit

Nodesploit is a quicker variant of getsploit, but might yield lesser results. Instead of enumerating nodes through geth, it pull a list from a public peer-list website.
For each entry in that list, nodesploit will probe for an open rpc-port.

```
./nodesploit
```

###Results

results will be written to **possible_vulnerables.txt** and **possible_vulnerables2.txt**.

###Disclaimer

This was purely written to educate miners who might need to leave their RPC-port open to function in their mining pool.
Somewhere around August 2015, a blogpost was written to warn users not to leave their rpc port open and their account unlocked.

By default, at the time of writing, accounts are locked, but problems arise when a user unlocks his account or opens the mist-wallet.
The mist wallet will unlock the account for 2 seconds when opened. An attacker who continuously sends **eth.sendTransaction()** requests
can use that small window of oppurtunity to steal your precious ether.


