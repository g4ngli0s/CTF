-----
**Rabbit Traffic (150 pts)
CTF: Fwhibbit CTF 2017
URL: https://ctf.followthewhiterabbit.es/
CAT: forensics**

-----

Points: 150 
Country: United States 

Attatchment: https://mega.nz/#!40tXFBwB!uB4OR7xRhbJ_2YmJN_dCxK81oCPUq2Wwam0NxcfOoYQ -> capture.pcap

Description: Our research center has evolved during this last time. However, they are having some problems while intercepting communications... Help our investigators to decode the following transmission.

-----

In this challenge, the file 'capture.pcap' is provided. We open it with Wireshark and see lots of traffic between several IP addresses.

There is one traffic wich seems of particular interest starting on packet 590 (tcp.stream eq 33): a passive FTP transfer between 192.168.10.132 and 192.168.10.100.

Filtering out the TCP stream 33 and using the 'Follow TCP stream' on Wireshark reveals the following:

```
noop
200 Zzz...
CWD /
250 OK. Current directory is /
noop
200 Zzz...
CWD /
250 OK. Current directory is /
TYPE A
200 TYPE is now ASCII
PASV
227 Entering Passive Mode (192,168,10,100,246,135)
LIST
150 Accepted data connection
226-Options: -l 
226 0 matches total
noop
200 Zzz...
CWD /
250 OK. Current directory is /
TYPE I
200 TYPE is now 8-bit binary
PASV
227 Entering Passive Mode (192,168,10,100,47,61)
STOR master.log.0
150 Accepted data connection
226-File successfully transferred
226 0.001 seconds (measured here), 3.86 Mbytes per second
```

We see that the file 'master.log.0' has been transferred to the server (STOR master.log.0), so now we are interested in extracting this file.

