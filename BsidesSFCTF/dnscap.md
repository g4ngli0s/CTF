## ===================================================
## dnscap (500 pts)
## CTF: BSidesSF 2017 CTF
## URL: https://scoreboard.ctf.bsidessf.com/
## CAT: forensics
## ===================================================

Found this packet capture. Pretty sure there's a flag in here. Can you find it!?

dnscap.pcap

----------
## (1) ANALISYS OF THE PCAP FILE USING Wireshark

On this challenge, a pcap file named 'dnscap.pcap' is presented for analisys. We open it with Wireshark and see that there are lots of DNS queries and responses of the following types: CNAME, TXT and MX. On each of them, the contents of both the queries and the responses contain large hex strings.

We can use the following Wireshark filters to isolate each query/response of interest:

