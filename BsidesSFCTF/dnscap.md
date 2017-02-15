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
# tshark -r dnscap.pcap -Y '(dns.qry.type == 16) and not (dns.txt)' -T fields -e frame.number -e dns.qry.name > queries_TXT.txt
```

TXT RESPONSES
```
# tshark -r dnscap.pcap -Y 'dns.txt' -T fields -e frame.number -e dns.txt > responses_TXT.txt
```

MX QUERIES
```
# tshark -r dnscap.pcap -Y '(dns.qry.type == 15) and not (dns.mx.mail_exchange)' -T fields -e frame.number -e dns.qry.name > queries_MX.txt
```

MX RESPONSES
```
# tshark -r dnscap.pcap -Y 'dns.mx.mail_exchange' -T fields -e frame.number -e dns.mx.mail_exchange > responses_MX.txt
```

CNAME QUERIES
```
# tshark -r dnscap.pcap -Y '(dns.qry.type == 5) and not (dns.cname)' -T fields -e frame.number -e dns.qry.name > queries_CNAME.txt
```

CNAME RESPONSES
```
# tshark -r dnscap.pcap -Y 'dns.cname' -T fields -e frame.number -e dns.cname > responses_CNAME.txt
```

Note that for each capture we include the frame number, just in case it is necessary for any purpose.

Then we merge all the files in a single one:
```
# cat queries_CNAME.txt queries_MX.txt queries_TXT.txt responses_CNAME.txt responses_MX.txt responses_TXT.txt > fusion.txt
```

And generate a new merged file with all the packets ordered by frame number (first column in the file):
```
# sort -k1n,3 fusion.txt > fusion_ordenado.txt
```

Here is how this new file looks like:
```
1       05e100a621c3620001636f6e736f6c65202873697276696d65732900.skullseclabs.org
2       958700a621c3620001636f6e736f6c65202873697276696d65732900.skullseclabs.org
3       634f00a621010a0000.skullseclabs.org
4       7cd501a621c362010a.skullseclabs.org
5       96b201a621010ac362
6       b11c01a621c362010a.skullseclabs.org
7       e14001a621010ac362
8       0ab801a621c362010a.skullseclabs.org
9       0e3d01a621010ac362.skullseclabs.org
10      772301a621c362010a.skullseclabs.org
11      d01b01a621010ac362.skullseclabs.org
12      b73f01a621c362010a57656c636f6d6520746f20646e7363617021205468.6520666c61672069732062656c6f772c20686176652066756e21210a.skullseclabs.org
13      aeb101a621010ac393.skullseclabs.org
/....../
```
------
## (2) ANALYSIS OF THE CAPTURED DATA

In order to analyze the data we have just extracted, we use the following Perl script named 'bsidessf17_dnscap_script1.pl' (yeah, there is life beyond Python!):

```
#!/usr/bin/perl
#
# bsidessf17 - dnscap
#
# script de analisis inicial
#
# fusion_ordenado.txt tiene el formato: <paquete>\t<datos>
#
# Rev.20170212 by sn4fu

use strict;
use warnings;
use 5.016;

my $fichero = 'fusion_ordenado.txt';
open(my $fh,$fichero)
or die "No se ha encontrado el fichero '$fichero' $!";

while (my $linea = <$fh>) {
 chomp $linea;                                          # quitar CR
 my ($paquete, $datos) = split /\t/, $linea;            # parsear usando TAB como separador
 print "$paquete\n";                                    # imprimir numero de paquete
 print "$datos\n";                                      # imprimir datos del paquete
 my @cadenas = split /\./, $datos;                      # parsear las partes de la cadena de datos separadas con '.'
 my $cadena_sobrante1 = 'org';                          # las cadenas 'org' no nos interesan
 @cadenas = grep {!/$cadena_sobrante1/} @cadenas;
 my $cadena_sobrante2 = 'skullseclabs';                 # las cadenas 'skullseclabs' no no sinteresan
 @cadenas = grep {!/$cadena_sobrante2/} @cadenas;
 foreach (@cadenas)
   {
      print "$_\n";                                     # imprimir la cadena HEX
      say (pack "H*",$_);                               # traducir la cadena a ASCII
   }
}
```
This script reads each line (packet) of the file, parses the frame number and the payload and parses the payload as well in order to extract the strings separated by '.'. Then it deletes all the strings 'org' and 'skullseclabs' (we are interested just in the hex strings) and converts the hex strings to ASCII.



