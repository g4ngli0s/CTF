## ===================================================
## dnscap (500 pts)
## CTF: BSidesSF 2017 CTF
## URL: https://scoreboard.ctf.bsidessf.com/
## CAT: forensics
## ===================================================

Found this packet capture. Pretty sure there's a flag in here. Can you find it!?

dnscap.pcap

----------
## (1) ANALYSIS OF THE PCAP FILE USING Wireshark

On this challenge, a pcap file named 'dnscap.pcap' is presented for analysis. We open it with Wireshark and see that there are lots of DNS queries and responses of the following types: CNAME, TXT and MX. On each of them, the contents of both the queries and the responses contain large hex strings.

We can use the following Wireshark filters to isolate each query/response of interest:

TXT QUERIES:
(dns.qry.type == 16) and not (dns.txt)

TXT RESPONSES:
dns.txt

MX QUERIES:
(dns.qry.type == 15) and not (dns.mx.mail_exchange)

MX RESPONSES:
dns.mx.mail_exchange

CNAME QUERIES:
(dns.qry.type == 5) and not (dns.cname)

CNAME RESPONSES:
dns.cname

Using tshark, we can extract all those packets in separated files:

TXT QUERIES
```
tshark -r dnscap.pcap -Y '(dns.qry.type == 16) and not (dns.txt)' -T fields -e frame.number -e dns.qry.name > queries_TXT.txt
```

TXT RESPONSES
```
tshark -r dnscap.pcap -Y 'dns.txt' -T fields -e frame.number -e dns.txt > responses_TXT.txt
```

MX QUERIES
```
tshark -r dnscap.pcap -Y '(dns.qry.type == 15) and not (dns.mx.mail_exchange)' -T fields -e frame.number -e dns.qry.name > queries_MX.txt
```

MX RESPONSES
```
tshark -r dnscap.pcap -Y 'dns.mx.mail_exchange' -T fields -e frame.number -e dns.mx.mail_exchange > responses_MX.txt
```

CNAME QUERIES
```
tshark -r dnscap.pcap -Y '(dns.qry.type == 5) and not (dns.cname)' -T fields -e frame.number -e dns.qry.name > queries_CNAME.txt
```

CNAME RESPONSES
```
tshark -r dnscap.pcap -Y 'dns.cname' -T fields -e frame.number -e dns.cname > responses_CNAME.txt
```

