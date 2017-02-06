### =============================================
### Fore3: USB probing (150 pts)
### CTF: AlexCTF 2017
### URL: https://ctf.oddcoder.com/
### CAT: forensics
### =============================================

One of our agents managed to sniff important piece of data transferred transmitted via USB, he told
us that this pcap file contains all what we need to recover the data can you find it ?

fore2.pcap

-------------------------------------------------
## (1) PRELIMINARY ANALYSIS WITH WIRESHARK

We open the pcap file with Wireshark and quickly see that it is the capture of several USB data transfers between a host and what seems to be an USB flash drive.

