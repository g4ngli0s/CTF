-----
#### Rabbit Traffic (150 pts)
#### CTF: Fwhibbit CTF 2017
#### URL: https://ctf.followthewhiterabbit.es/
#### CAT: forensics

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

We see that the file 'master.log.0' has been transferred to the server (STOR master.log.0), so now we are interested in extracting this file. Before the transference took place, the user issued the 'PASV' command to activate the passive FTP mode.

Searching again through the packets, we see that the transfer took place precisely in the packet 638 (FTP-DATA), in the TCP stream 35. Using the 'Follow TCP stream' function again reveals the contents of the file transferred:

```
CLIENT_RANDOM 820d4957c16c517b8ff94e4054f134c5e8f7b3542a393a740041052279574176 635614ee4da3a85a9dd7b7d25591728014a240562fa46ef26fd742425c6717fa84a1ae60c460a1f70eeaa63e98ba88c7
CLIENT_RANDOM 475cc1c522b988a53d3e4d56e50e21fa9f045c3efeb8fe94179e6d3d0a7e8ac0 c66df6f11aebd787111e21b90d4fadd69c7689f67a6dbcd07e08a75373d49e682ea7603c334592bdc3f2d1f1e3707e4d
CLIENT_RANDOM 6d3c83ebc21359caa3eb5297a7ab9de6394ed10da9ae6442c7689d818febef48 4206fe6c5a976289f17178fc65a670bf6958ab976c7532dcc1c676d36a14e1ce20e87627a76ab6855a63e8c24464e273
CLIENT_RANDOM cc548a1a586500785c7412de4d4d4f6ae34c8d8ec36da0b3518af3ed6aa61ff0 b6f23c98c786faa1cc56e958b04c6cd64be3115a9a164860229af25ef4733e4ef070f4297c873b5e4153382bd31fd05c
CLIENT_RANDOM c75f58fd9a1a14466f9b8e9b390d2539ad120eb5866f27753d5942a16ed1f70b 5469d9d0676e081a3ce6718fd1a6fd71ca00cf558a200e26b1ef03ca2e74bf63014b35312c42c568b9385a1b3f003e9a
CLIENT_RANDOM b0f58e1e571fb6f23279260be2295a0b44f0853ce1b54e891e88b5beb92504da 9cd1e24ad704f1229157275a80a866c4c31cf4a0df0d3429a1e4e241946d1b5c2757facc58648a419fe3d6fe46fca606
CLIENT_RANDOM a83bce1330ab876cded49622b8bd101cc713166d2381eda34b98a2ccfa8c66a4 0fbbac8d2ef0d8a1b2b9c24ac4d0e9ee048ec672c0ee7bc75e0e430a87a3b0862c9071a90728be23ec5271b437ca4375
CLIENT_RANDOM 03fc4f217a7e2144f9ba969ff9b64ecd17a386eeb5afb153d8d9168ac7effa0b 35b092d1e1469ef50b6917ffd78a0be3bf6330fe29d1a9d3d9da6a87300a0e2cae3dd8d10275df11175d4930d06099b0
CLIENT_RANDOM 5e305cc5c84740fe778f77b0490599065879f0e4fda10c6380a17f4df8265179 800c665b98c6d682d7d9c75aabc9146f747093cf9721e1d26d0198f8a2d00ed0d023e0a4971c7f7824d9968f2e627ed9
CLIENT_RANDOM dc051107581c3461b9451242825ae2ee88407f8b7ada1897ca795607a1a20afd 8bc055e867ced0149fc27d7bca6f89b8765a9959aef67e3cd91da4f3e3b13c8d780fd69238992f69624d597bddfb65e6
CLIENT_RANDOM d9d661fc80d5ada57365e77a7a3c75a1a478feef209d04fc2a709f68ca3c61a6 a16ed93fdde3458eedc0d29e71dd97ddef84212ee47dfc907db1ce0a172e4fb0c49329e93f1ee1ba13ce29d113966e73
CLIENT_RANDOM ec6dfa34e8fe135e854578e3ad585dacb0b1194f05073533a90829f4cbaf03bc ffc56661049581a846de292e0513bc86a04825adfc3fe28f0c7ba772fe9bbef443cb7e2ce8c17d8cf4ac6042de6f09fa
CLIENT_RANDOM 2476a2709f2330ab935e696a3b3c08c91b6e2b225c88c09584a564a9d7276096 865995d65ad706c229ee0e228f0aba88ebda48569bcbdd38c8884ddf4a30510460beb7e6aa3d494b524d60c7ffee50aa
```

Now we perform some OSINT to see what kind of data contains this file and find the following:

https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS/Key_Log_Format

So we conclude that this file is a Mozilla Network Security Services (NSS) Key Log file, with contents of the following kind:

```
CLIENT_RANDOM <space> <64 bytes of hex encoded client_random> <space> <96 bytes of hex encoded master secret>
```

NSS is a develover tool and this file contains the master secret keys used in SSL transmissions, so we wonder whether they may be of use to decypher some TLS traffic also present in other streams our pcap. In order to check that, we configure Wireshark to use those keys we just grabbed. We put the contents of the captured transmission in a file named 'master.txt' and load it in the SSL preferences section of Wireshark:

Edit > Preferences > Protocols > SSL > (Pre)-Master-Secret Log

If we try to see the TCP sequence 32 with 'Follow TCP stream' we just get garbage because it is a TLSv1.2 transmission. However, once the keys have been loaded, we can use 'Follow SSL stream' instead to see the contents. Now we are able to see at least the HTTP headers within the TLS transmission.

In order to extract the contents of the transmission, we select the packet 501 in the main pane:

```
501	11.716022	192.168.10.132	192.168.10.100	HTTP	405	GET / HTTP/1.1 
```

And then use 'Follow HTTP stream' to see its contents:
```
GET / HTTP/1.1
Host: 192.168.10.100
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1

HTTP/1.1 200 OK
Server: nginx/1.10.2
Date: Sat, 10 Dec 2016 20:58:27 GMT
Content-Type: text/html
Last-Modified: Sat, 10 Dec 2016 18:37:37 GMT
Transfer-Encoding: chunked
Connection: keep-alive
ETag: W/"584c4b71-fd"
Content-Encoding: gzip

<!DOCTYPE html>
<html>
<head>
<title>Look Here :)</title>
</head>
<body>
<h1 style="text-align: center;">Your Private Flag</h1>
<p>&nbsp;</p>
<p style="text-align: center;"><strong>fwhibbit{d3c0d3Th1sIfy0uC4n}</strong></p>
<p>&nbsp;</p>
</body>
</html>
GET /favicon.ico HTTP/1.1
Host: 192.168.10.100
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

HTTP/1.1 404 Not Found
Server: nginx/1.10.2
Date: Sat, 10 Dec 2016 20:58:27 GMT
Content-Type: text/html
Transfer-Encoding: chunked
Connection: keep-alive
Content-Encoding: gzip

<html>
<head><title>404 Not Found</title></head>
<body bgcolor="white">
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.10.2</center>
</body>
</html>
```

So the flag is:

fwhibbit{d3c0d3Th1sIfy0uC4n}



